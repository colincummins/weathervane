def forecast_to_quote(forecast):
    #Takes in a short forecast string and returns tuple of quote and author
    import requests, re, json
    import wv_config
    
    try:
        url_template = "https://quotes.rest/quote/search?minlength=100&maxlength=300&query={}&private=false&language=en&limit=1&sfw=false"
        search_headers = wv_config.search_headers
        search_keys = wv_config.search_keys

        pattern = '|'.join(search_keys)
        pattern = re.compile(pattern)
        regex_key = re.search(pattern,forecast).group()

        raw_report = requests.get(url_template.format(regex_key),headers=search_headers)

        body = raw_report.json()['contents']['quotes'][0]['quote']
        author = raw_report.json()['contents']['quotes'][0]['author']

        return (body, author)
    
    except Exception as e:
        print('forecast_to_quote failed. Exception :',e)