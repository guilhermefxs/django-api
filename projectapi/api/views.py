from itertools import chain
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, JsonResponse

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status

from .pagination import PersonalizedPagination

from .models import Profile, Team

from .serializers import ProfileSerializer, TeamSerializer
from rest_framework.generics import ListAPIView


@api_view(['GET'])
def apiOverview(request):
    return JsonResponse("API BASE POINT", safe=False)

@api_view(['GET'])
def profileList(request):
	profiles = Profile.objects.all().order_by('-id')
	serializer = ProfileSerializer(profiles, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def createProfile(request):
    try:
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
            return Response("The user info is not valid", status=400)
    except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            return Response("The user info is not valid", status=400)
    
@api_view(['GET'])
def getUserAgreement(request):
    return FileResponse(open('./media_root/user-agreement.pdf', 'rb'), as_attachment=True, filename='user-agreement.pdf')
    

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = Profile.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['POST'])
def createTeam(request):
    for obj in request.data:
        serializer = TeamSerializer(data=obj)
        
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            return Response(serializer.data, status=400)
    return Response(serializer.data, status=201)

class teamDetailView(ListAPIView):
    serializer_class = TeamSerializer
    pagination_class = PersonalizedPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
            qs = Team.objects.all()
            search = self.request.query_params.get("search")
            
            if search is not None:
                teamsByColor = qs.filter(cores__icontains = search)
                teamsByCity = qs.filter(localizacao__icontains = search)
                teamsByName = qs.filter(nome__icontains = search)
                qs = list(chain(teamsByColor, teamsByCity, teamsByName))
            isOnSerieA = self.request.query_params.get("isOnSerieA")
            if isOnSerieA is not None:
                qs = qs.filter(isOnSerieA = isOnSerieA)
            
            ordering = self.request.query_params.get("orderBy")
            if ordering is not None:
                qs = qs.order_by(ordering)
            return qs