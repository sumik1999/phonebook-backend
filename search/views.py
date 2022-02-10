from rest_framework import views

from core.models import GlobalContact, User
from rest_framework import response, authentication, permissions
from user.serializers import GlobalContactSerializer, UserSerializer


class SearchNameApiView(views.APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("query")
        results = GlobalContact.objects.filter(name__startswith=query).union(
            GlobalContact.objects.filter(name__icontains=query)
        )
        return response.Response(
            {"data": GlobalContactSerializer(results, many=True).data}
        )


class SearchNumberApiView(views.APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("query")
        user = User.objects.filter(phone_number=query).first()
        if user:
            return response.Response(
                {
                    "data": [UserSerializer(user).data],
                    "message": "User existed from before!",
                }
            )
        results = GlobalContact.objects.filter(phone_number__icontains=query)

        return response.Response(
            {
                "data": GlobalContactSerializer(results, many=True).data,
                "message: ": "User has been created!",
            }
        )
