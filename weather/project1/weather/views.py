import pdfkit
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from .models import WeatherData
import requests

def index(request):
    wikipedia_url = "https://en.wikipedia.org/wiki/Django_(web_framework)"
    wikipedia_title = ""
    wikipedia_description = ""
    weather_data = {}

    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = '4ba5c659252cce49627398f212f71f56'
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'country_code': data['sys']['country'],
                'longitude': data['coord']['lon'],
                'latitude': data['coord']['lat'],
                'temp': data['main']['temp'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'main': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }

            # Save the weather data to the database
            WeatherData.objects.create(
                city=weather_data['city'],
                country_code=weather_data['country_code'],
                coordinate=f"{weather_data['longitude']} {weather_data['latitude']}",
                temperature=weather_data['temp'],
                pressure=weather_data['pressure'],
                humidity=weather_data['humidity'],
                main=weather_data['main'],
                description=weather_data['description'],
                icon=weather_data['icon'],
            )

            # Fetch Wikipedia summary for the city
            wikipedia_api_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{city}'
            wikipedia_response = requests.get(wikipedia_api_url)
            wikipedia_data = wikipedia_response.json()

            if wikipedia_response.status_code == 200:
                wikipedia_title = wikipedia_data.get('title', 'No title available.')
                wikipedia_description = wikipedia_data.get('extract', 'No description available.')

            # Check if the "Download PDF" button was clicked
            if 'download_pdf' in request.POST:
                # Render the HTML template to a string
                html_string = render_to_string('index.html', {
                    **weather_data,
                    'wikipedia_title': wikipedia_title,
                    'wikipedia_description': wikipedia_description,
                    'wikipedia_url': wikipedia_url
                })

                # Configuration for wkhtmltopdf
                config = pdfkit.configuration(wkhtmltopdf=r'C:\path\to\wkhtmltopdf.exe')

                # Convert the HTML string to a PDF
                pdf = pdfkit.from_string(html_string, False, configuration=config)

                # Return the PDF as a response
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="weather_report.pdf"'
                return response

            # Render the page with weather data and Wikipedia summary
            return render(request, 'index.html', {
                **weather_data,
                'wikipedia_title': wikipedia_title,
                'wikipedia_description': wikipedia_description,
                'wikipedia_url': wikipedia_url
            })
        else:
            # City not found error
            return render(request, 'index.html', {'error': 'City not found', 'wikipedia_url': wikipedia_url})

    # Initial page load or GET request
    return render(request, 'index.html', {'wikipedia_url': wikipedia_url})
