from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Manage Tag In The Database
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # so this above line requires that token authentication is used and the
    # user is authenticated to use the API.
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """
        Return objects for the current authenticated user only.
        :return:
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')
