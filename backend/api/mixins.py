from rest_framework import mixins, viewsets


class ViewSet(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    pass

