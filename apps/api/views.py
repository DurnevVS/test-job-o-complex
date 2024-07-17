from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Count

from apps.main.models import SearchHistory

# from .serializers import SearchHistorySerializer


class SearchHistoryAPIView(APIView):

    def get(self, request):
        city_counts = SearchHistory.objects.values(
            'city').annotate(count=Count('city')).order_by('-count')
        return Response(city_counts, status=status.HTTP_200_OK)
