import os
from django.http import HttpResponsePermanentRedirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


def api_response(
    status=status.HTTP_200_OK,
    message="Request completed successfully",
    data=None,
):
    """
    A utility function to standardize API responses.
    """
    return Response({"status": status, "message": message, "data": data}, status=status)


class CustomRedirect(HttpResponsePermanentRedirect):
    permission_classes = [AllowAny]
    allowed_schemes = [os.environ.get("APP_SCHEME"), "http", "https"]

