from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import UserDetailSerializer
from .models import User

class GetLandlordView(APIView):
    authentication_classes =[]
    permission_classes = []

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user_serializer = UserDetailSerializer(user, many=False)
        return Response(user_serializer.data)



