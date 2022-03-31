from django.shortcuts import render
from .forms import UploadFileForm, ReservationModelForm
from .models import ReservationModel, CityModel
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from django.contrib import messages
import csv, io
from django.urls import reverse_lazy


class CreateCityView(CreateView):
    model = CityModel
    template_name = 'hosts/city.html'
    form_class = CityModelForm
    success_url = reverse_lazy('list-cities')


class ListCityView(ListView):
    model = CityModel
    context_object_name ='cities'  
    template_name = 'hosts/cities.html'


class UpdateCityView(UpdateView):
    model = CityModel
    template_name = 'hosts/update-city.html'
    fields = ['city','commission_percent']
    success_url = reverse_lazy('list-cities')


class DeleteCityView(DeleteView):
    model = CityModel
    template_name = 'hosts/delete-city.html'
    context_object_name ='city' 
    success_url = reverse_lazy('list-cities')


class ListReservationView(ListView):
    model = ReservationModel
    context_object_name ='reservations'  
    template_name = 'hosts/reservations.html'


class ListCommisionsMonthView(ListView):
    model = ReservationModel
    template_name = 'hosts/commission-per-month.html'
    context_object_name = 'commissions'

    def get_queryset(self,*args, **kwargs):
        q={}
        queryset = super().get_queryset()
        years ={year.year for year in queryset.dates("checkin", "year")}
        months = {month.month for month in queryset.dates("checkin", "month")}
        for year in years:
            for month in months:
                q[str(year)+"/"+str(month)]=ReservationModel.objects.filter(checkin__year = year, 
                                            checkin__month = month).aggregate(Sum("commission"))['commission__sum']
        for k,v in list(q.items()):
            if v is None:
                del q[k]
        return q


class ListCommisionsByCityView(ListView):
    model = ReservationModel
    template_name = 'hosts/commission-per-city.html'
    context_object_name = 'commisions'

    def get_queryset(self,*args, **kwargs):
        q={}
        queryset = super().get_queryset()
        cities = CityModel.objects.all()
        for city in cities:
            q[str(city)]=ReservationModel.objects.filter(city = city).aggregate(Sum("commission"))['commission__sum']
        return q


def upload_view(request):
    form = UploadFileForm()
    form_1 = ReservationModelForm()
    form_1_errors=[]
    message=""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            message = "Updated successfully"
            csv_file = request.FILES['select_file'] #get uploaded file
            data_set = csv_file.read().decode('UTF-8')
            io_string  = io.StringIO(data_set)
            next(io_string) #exclude first row   
            for element in csv.reader(io_string, delimiter = ',' ):
                reservation = element[0] #get reservation from dataset
                checkin = element[1]#get checkin from dataset
                checkout = element[2]#get checkout from dataset
                flat = element[3]#get flat from dataset
                income = float(element[5])#get income from dataset
                city = element[4].upper()#get city from dataset
                data = {'reservation':reservation, 'checkin':checkin, 'city':city,
                        'checkout': checkout, 'flat': flat, 'income':income }
                form_1 = ReservationModelForm(data)
                if form_1.is_valid():
                    form_1.save()
                else:
                   form_1_errors.append(form_1.errors)
    return render(request, 'hosts/upload_file.html', {'form':form ,'errors':form_1_errors, "message": message})
