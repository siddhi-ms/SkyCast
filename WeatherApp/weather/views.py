from django.shortcuts import render
import requests
import datetime

# ✅ API keys
OPENWEATHER_API_KEY = 'ae25ea68cd44f627d854efd69a0287f1'  # Update with a valid key
GOOGLE_API_KEY = 'AIzaSyBBzaFI-ARStXtrfgJ5CsYV-rvEnVDgdBo'  # Ensure this is valid
SEARCH_ENGINE_ID = '54c0767105ce44dc5'  # Ensure this is valid

def home(request):
    if request.method == 'POST' and 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'mumbai'

    # ✅ Weather API call
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()

        # Weather API error check
        if weather_data.get('cod') != 200:
            context = {
                'error': weather_data.get('message', 'City not found.'),
            }
        else:
            description = weather_data['weather'][0]['description']
            icon = weather_data['weather'][0]['icon']
            temp = weather_data['main']['temp']
            day = datetime.date.today()

            # ✅ Google Custom Search - image
            search_url = 'https://www.googleapis.com/customsearch/v1'
            search_params = {
                'key': GOOGLE_API_KEY,
                'cx': SEARCH_ENGINE_ID,
                'q': city,
                'start': 1,
                'searchType': 'image'
            }

            try:
                search_response = requests.get(search_url, params=search_params)
                search_data = search_response.json()
                search_items = search_data.get('items', [])
                image_url = search_items[0]['link'] if search_items else None  # Use the first item
            except Exception as e:
                image_url = None
                print(f"Image search error: {e}")

            # ✅ Final context
            context = {
                'weather': {
                    'city': city,
                    'temperature': temp,
                    'condition': description,
                    'icon': icon,
                    'day': day,
                    'image': image_url,
                }
            }

    except Exception as e:
        context = {
            'error': f'An error occurred while fetching the weather data: {e}'
        }

    return render(request, 'weather/index.html', context)
