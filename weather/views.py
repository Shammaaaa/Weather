from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    appid = '72b757872627ac8581621d091461c1b3'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()

                if res['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Такого города не существует'

            else:
                err_msg = 'Город уже существует в базе данных'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Город добавлен'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temp': res['main']['temp'],
            'description': res['weather'][0]['description'],
            'icon': res['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form,
               'message': message,
               'message_class': message_class

               }

    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
