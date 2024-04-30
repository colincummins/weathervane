def get_short_forecast(zipcode):

    #Takes in a zipcode and returns a short forecast as text string
    
    import requests, json, wv_config
    from zipcode_to_latlong import zipcode_to_latlong
    
    latlong_url_template = 'https://api.weather.gov/points/{},{}'
    authentication_header = wv_config.authentication_header
    
    lat,long = zipcode_to_latlong(zipcode)
    points_page = requests.get(latlong_url_template.format(lat,long),headers=authentication_header)
    points_data = points_page.json()
    forecast_url = points_data['properties']['forecast']
    forecast_page = requests.get(forecast_url,headers=authentication_header)
    forecast_data = forecast_page.json()
    return forecast_data['properties']['periods'][0]['shortForecast'].lower()