# Import modules and functions
from Quote import Quote
from Subscriber import Subscriber
import wv_config
from zipcode_to_latlong import zipcode_to_latlong
from get_short_forecast import get_short_forecast
from forecast_to_quote import forecast_to_quote
from send_weathergram import send_weathergram

# Define hardcoded subscriber for now
main_recipient = Subscriber()
main_recipient.email,main_recipient.zipcode = wv_config.default_subscriber
print('Recipient e-mail/zip: ',main_recipient)

#Get a quotation for hardcoded subscriber
quotation = Quote()
quotation.body, quotation.author = forecast_to_quote(get_short_forecast(main_recipient.zipcode))
print('Sending quotation:\n',quotation)

#Send quotation
send_weathergram(main_recipient.email,quotation)