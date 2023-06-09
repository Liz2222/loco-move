from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework import status
from .models import *

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def user_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print("one")

    user = authenticate(request, username=username, password=password)
    print("weny")

    if user is not None:
        print("9")
        # Authentication successful
        users=User.objects.get(username=username)
        refresh = RefreshToken.for_user(user)

        # Return the user's details, refresh token, and access token in the response
        return Response({
            'Success': True,
            'Code': 200,
            'Details': {
                'email': users.email,
                'first_name': users.first_name,
                'last_name': users.last_name,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=HTTP_200_OK)
    else:
        # Authentication failed
        return Response({
            'Success': False,
            'Code': 401,
            'message': 'Invalid email or password.'
        }, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def driver_signup_view(request):
    serializer = DriverSerializer(data=request.data)
    User = get_user_model()

    if serializer.is_valid():
         if serializer.is_valid():
            email = request.data['email']

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                return Response({'Success': False, 'Code': 400, 'message': 'Email already exists.'}, status=HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(
            email=request.data['email'],
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            username=request.data.get('username'), 

            is_driver=True,
        )

            driver = serializer.save(user=user)

            return Response({'Success': True, 'Code': 200, 'message': 'Driver created successfully.'}, status=HTTP_201_CREATED)
    else:
        return Response({'Success': False, 'Code': 400, 'message': serializer.errors}, status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def mover_signup_view(request):
    #serializer = MoverSerializer(data=request.data)

#
    try:
        User = get_user_model()
        user = User.objects.create_user(
            email=request.data.get('email'),
            password=request.data.get('password'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            username=request.data.get('username'),
            is_mover=True,
        )


        return Response({'Success': True, 'Code': 201, 'message': 'Mover created successfully.'}, status=HTTP_201_CREATED)
    except:
        return Response({'Success': False, 'Code': 400, 'message': 'Invalid username or email'}, status=HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
def profile_list(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#