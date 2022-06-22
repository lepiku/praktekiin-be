from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['POST'])
def logout(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    request.session.flush()
    return Response({'detail': 'Logout success'})
