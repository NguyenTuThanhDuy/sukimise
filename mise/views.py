from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):

    def get(self, request: HttpRequest) -> Response:
        return Response({"status": 200})
