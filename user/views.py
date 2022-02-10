
from core.models import GlobalContact
from rest_framework import generics, mixins, authentication, permissions, viewsets, views, response
from rest_framework.decorators import action

from .serializers import GlobalContactSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import AuthTokenSerializer, UserSerializer
from user import serializers


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        contact = GlobalContact.objects.create(
            name=serializer.name,
            phone_number=serializer.phone_number,
            email=serializer.email,
            owner=user,
        )
        contact.save()


class UpdateUserView(viewsets.ModelViewSet):
    serializer_class = UserUpdateSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserSerializer
        return UserUpdateSerializer

class AddContactView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        # contacts = GlobalContactSerializer(data=request.data, many=True)
        for contact in request.data:
            contact_object = GlobalContactSerializer(data=contact)
            # contact_object.owner = request.user 
            
            if contact_object.is_valid():
                contact_object.save(owner=request.user)

            else:
                print("EEEEEEEEEEEEEEEEEEEE Error")
                print(contact_object.errors)
            print(contact_object)
        return response.Response({"Message": "Added"})

    

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class GlobalContactViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GlobalContactSerializer
    queryset = GlobalContact.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    # @action(detail=True)
    # def mark_spam(self,request,pk=None):
    #     phone_number = self.queryset.get(pk=pk).phone_number
    #     print("numberrr",phone_number)
    #     self.queryset.filter(phone_number=phone_number).update(is_spam = True)
    #     return response.Response({"message":"Done!"})

class MarkSpamApiView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,number):
        contacts = GlobalContact.objects.filter(phone_number=number)
        if contacts:
            contacts.update(is_spam = True)
        else:
            contact = GlobalContactSerializer(data={"phone_number":number,"is_spam":True})
            if contact.is_valid():
                contact.save(owner=self.request.user)
            else:
                print("errrosssss",contact.errors)
                return response.Response({"Error": contact.errors})

        return response.Response({"message":"Done!"})
