from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from useraccount.models import User

from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertyDetailsSerializer, ReservationListSerializer

class PropertiesListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):

        try:
            token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
            token = AccessToken(token)
            user_id = token.payload['user_id']
            user = User.objects.get(pk=user_id)
        except Exception as e:
            user = None

        favourites = []
        properties_list_instance = Property.objects.all()

        landlord_id = request.GET.get('landlord_id', '')
        is_favourites = request.GET.get('is_favourites', '')
        country = request.GET.get('country', '')
        category = request.GET.get('category', '')
        checkin_date = request.GET.get('checkIn', '')
        checkout_date = request.GET.get('checkOut', '')
        bedrooms = request.GET.get('numBedrooms', '')
        guests = request.GET.get('numGuests', '')
        bathrooms = request.GET.get('numBathrooms', '')

        if checkin_date and checkout_date:
            exact_matches = Reservation.objects.filter(start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
            overlap_matches = Reservation.objects.filter(start_date__lte=checkout_date, end_date__gte=checkin_date)
            all_matches = []
            for reservation in exact_matches | overlap_matches:
                all_matches.append(reservation)
            properties_list_instance = properties_list_instance.exclude(id__in=all_matches)

        if landlord_id:
            properties_list_instance = properties_list_instance.filter(landlord=landlord_id)

        if is_favourites:
            properties_list_instance = properties_list_instance.filter(favorited__in=[user])

        if guests:
            properties_list_instance = properties_list_instance.filter(guests__gte=guests)

        if bedrooms:
            properties_list_instance = properties_list_instance.filter(bedrooms__gte=bedrooms)

        if bathrooms:
            properties_list_instance = properties_list_instance.filter(bathrooms__gte=bathrooms)
        
        if country:
            properties_list_instance = properties_list_instance.filter(country=country)

        if category and category != 'undefined':
            properties_list_instance = properties_list_instance.filter(category=category)

        if user:
            for property in properties_list_instance:
                if user in property.favorited.all():
                    favourites.append(property.id)

        properties_list_serializer = PropertiesListSerializer(properties_list_instance, many=True)
        return Response({ "data": properties_list_serializer.data, 'favourites': favourites })

class CreateProperty(APIView):
    def post(self, request):
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.landlord = request.user
            property.save()
            return Response({"success": True})
        print(form.errors, form.non_field_errors)
        return Response({"msg": "Something went wrong", "errors": form.errors.as_json()}, status=400)


class PropertiesDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        properties_detail_instance = Property.objects.get(pk=pk)
        properties_detail_serializer = PropertyDetailsSerializer(properties_detail_instance, many=False)
        return Response({ "data": properties_detail_serializer.data })

class BookProperty(APIView):
    def post(self, request, pk):
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            number_of_nights = request.POST.get('number_of_nights', '')
            total_price = request.POST.get('total_price', '')
            guests = request.POST.get('guests', '')

            property = Property.objects.get(pk=pk)

            Reservation.objects.create(
                property=property,
                start_date=start_date,
                end_date=end_date,
                number_of_nights=number_of_nights,
                total_price=total_price,
                guests=guests,
                created_by=request.user
            )
            return Response({ "success": True })

        except Exception as e:
            print(e)
            return Response({ "success": False }, status=400)

class ReservationsListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        property = Property.objects.get(pk=pk)
        reservations = property.reservations.all()
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)

class UserReservationsListView(APIView):
    def get(self, request):
        reservations = request.user.reservations.all()
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)

class ToggleFavourite(APIView):
    def post(self, request, pk):
        property = Property.objects.get(pk=pk)
        if request.user in property.favorited.all():
            property.favorited.remove(request.user)
            return Response({"is_favourite": False})
        else: 
            property.favorited.add(request.user)
            return Response({"is_favourite": True})