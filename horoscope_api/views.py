# views.py
import asyncio
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import scrape_horoscope

# Root URL view (home)
def home(request):
    """Handle GET request for the root URL (/)"""
    return HttpResponse("Welcome to the MoonSign Horoscope API!")

class HoroscopeAPIView(APIView):
    """ DRF API View to return horoscope data """

    def get(self, request):
        """Handles GET request for horoscope data"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(scrape_horoscope())  # Scrape horoscope data
        return Response({
            'message': 'Horoscope fetched successfully',
            'data': result  # You can change how the data is returned or modify the response
        })
