from django.shortcuts import render
from django.views import View
from django.conf import settings

# Import json data to load JSON Data to Python Dictonary
import json

# To make request to API
import urllib.request

# Create your views here.
class IndexView(View):
    template_name = "converter/index.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Get Amount
        amount = float(request.POST['amount'])
        # Get From country code 
        from_country = request.POST['from_country']
        # Get From country flag code using from_country variable
        from_country_flag_code = from_country[:-1]
        # Get To country code
        to_country = request.POST['to_country']
        # Get To country flag code using to_country variable
        to_country_flag_code = to_country[:-1]

        try:
            # Get JSON data from API
            api_url = str("https://v6.exchangerate-api.com/v6/"+settings.CONVERTER_API_KEY+"/pair/"+from_country+"/"+to_country+"")
            source_data = urllib.request.urlopen(api_url).read()

            # Convert JSON data to a Python Dictonary
            list_of_data = json.loads(source_data)

            # Get Conversion Rate
            conversion_rate = float(list_of_data["conversion_rate"])

            # Calculate the Amount with Conversion Rate
            conversion_amount = round(amount * conversion_rate, 4)
            
            # Get requied data from list_of_data
            converter_data = {
                "amount":amount,
                "conversion_amount":conversion_amount,
                "from_country":from_country,
                "to_country":to_country
            }

            # Flag codes for countries 
            flag_code = {
                "from_country_flag_code":from_country_flag_code,
                "to_country_flag_code":to_country_flag_code
            }

            context = {
                "converter_data":converter_data,
                "flag_code":flag_code
            }

        except:
            # Error in conversion calculation
            print("error found")

            converter_data = {
                "error":"conversion error"
            }

            context = {
                "converter_data":converter_data
            }

        return render(request, self.template_name, context)