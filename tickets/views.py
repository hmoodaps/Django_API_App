from django.http import JsonResponse
from rest_framework import status, mixins, generics, viewsets, filters, permissions
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from .serializer import *


# without rest frame work . just with model
def no_rest_yes_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'age', 'set_num')),
    }
    return JsonResponse(response)


# whit rest framework and model >> using functions  >> function based views ... FBV
@api_view(['GET', 'POST'])
def fbv_list(request):
    # GET
    if request.method == 'GET':
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)

    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def fbv_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET request
    if request.method == 'GET':
        serializer = GuestSerializer(guest)  # Corrected here
        return Response(serializer.data)

    # PUT request
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV CLASS BASED VIEW

class cbv_list(APIView):
    def get(self, request):
        # الحصول على قيمة 'name' من معلمات الاستعلام (query params) إذا كانت موجودة
        name = request.query_params.get('name', None)

        # تصفية الضيوف بناءً على الاسم إذا كان موجوداً
        if name:
            guests = Guest.objects.filter(name__icontains=name)
        else:
            guests = Guest.objects.all()

        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CBV WITH PK >>
class cbv_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CBV WITH MIXIN
# get (multi) and post(create)
class cbv_mx(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# get (single) put(update) delete(destroy)
class cbv_mx_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


# Generics
# get (multi) and post(create)
class gen(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# get (single) put(update) delete(destroy)
class gen_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# Viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name' , 'age', 'set_num']
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]



class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title' , 'hall' ,'date' , 'movie_time', 'available_sets' , 'all_sets']
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        movie_data = request.data.get('movie')
        guest_data = request.data.get('guest')

        # Check if the movie already exists
        movie_qs = Movie.objects.filter(
            title=movie_data['title'],
            hall=movie_data['hall'],
            date=movie_data['date']
        )

        if movie_qs.exists():
            movie = movie_qs.first()  # Use existing movie
        else:
            movie = Movie.objects.create(**movie_data)  # Create new movie

        # Check if the guest already exists
        guest_qs = Guest.objects.filter(
            name=guest_data['name'],
            age=guest_data['age'],
            set_num=guest_data['set_num']
        )

        if guest_qs.exists():
            guest = guest_qs.first()  # Use existing guest
        else:
            guest = Guest.objects.create(**guest_data)  # Create new guest

        # Check if the reservation already exists
        reservation_qs = Reservation.objects.filter(movie=movie, guest=guest)
        if reservation_qs.exists():
            return Response({"detail": "Reservation already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Reservation instance
        reservation = Reservation.objects.create(movie=movie, guest=guest)

        # Serialize the reservation and return the response
        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#create superuser by username and password
@api_view(['POST'])
def create_superuser(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_superuser(username=username, password=password)
        # إنشاء التوكن للمستخدم
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "User created successfully",
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
