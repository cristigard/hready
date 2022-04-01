from django.shortcuts import render
from .forms import UploadFileForm, ReservationForm, CityForm
from .models import Reservation, City
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.contrib import messages
import csv, io
from django.urls import reverse_lazy


class CreateCityView(CreateView):
    model = City
    template_name = 'hosts/city.html'
    form_class = CityForm
    success_url = reverse_lazy('list-cities')


class ListCityView(ListView):
    model = City
    context_object_name ='cities'  
    template_name = 'hosts/cities.html'


class UpdateCityView(UpdateView):
    model = City
    template_name = 'hosts/update-city.html'
    fields = ['name','rate']
    success_url = reverse_lazy('list-cities')


class DeleteCityView(DeleteView):
    model = City
    template_name = 'hosts/delete-city.html'
    context_object_name ='city' 
    success_url = reverse_lazy('list-cities')


class ListReservationView(ListView):
    model = Reservation
    context_object_name ='reservations'  
    template_name = 'hosts/reservations.html'


class ListCommisionsMonthView(ListView):
    model = Reservation
    template_name = 'hosts/commission-per-month.html'
    context_object_name = 'commissions'

    def get_queryset(self,*args, **kwargs):
        q={}
        queryset = super().get_queryset()
        years ={date.year for date in queryset.dates("checkin", "year")}
        months = {date.month for date in queryset.dates("checkin", "month")}
        for year in years:
            for month in months:
                q[str(year)+"/"+str(month)]=Reservation.objects.filter(checkin__year = year, 
                                            checkin__month = month).aggregate(Sum("commission"))['commission__sum']
        for k,v in list(q.items()):
            if v is None:
                del q[k]
        return q


class ListCommisionsByCityView(ListView):
    model = Reservation
    template_name = 'hosts/commission-per-city.html'
    context_object_name = 'commisions'

    def get_queryset(self,*args, **kwargs):
        q={}
        queryset = super().get_queryset()
        cities = City.objects.all()
        for city in cities:
            q[str(city)]=Reservation.objects.filter(city = city).aggregate(Sum("commission"))['commission__sum']
        return q


def upload_view(request):
    pass
    upload_form = UploadFileForm()
    register_form = ReservationForm()
    register_form_errors=[]
    message=""
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            message = "Updated successfully"
            csv_file = request.FILES['select_file'] #get uploaded file
            data_set = csv_file.read().decode('UTF-8')
            io_string  = io.StringIO(data_set)
            next(io_string) #exclude first row   
            for element in csv.reader(io_string, delimiter = ',' ):
                number = element[0] #get reservation from dataset
                checkin = element[1]#get checkin from dataset
                checkout = element[2]#get checkout from dataset
                flat = element[3]#get flat from dataset
                income = float(element[5])#get income from dataset
                city = element[4].upper()#get city from dataset
                City.objects.filter(name=city).first() #instanta
                data = {'number':number, 'checkin':checkin, 'city':city,
                        'checkout': checkout, 'flat': flat, 'income':income }
                register_form = ReservationForm(data)
                if register_form.is_valid():
                    register_form.save()
                else:
                   register_form_errors.append(register_form.errors)
    return render(request, 'hosts/upload_file.html', {'upload_form':upload_form , "errors":register_form_errors, "message": message})
