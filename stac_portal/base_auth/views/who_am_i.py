from rest_framework import generics,permissions

from base_auth.serializers.user import UserSerializer


class WhoAmIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
