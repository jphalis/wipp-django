from rest_framework import permissions

from api.permissions import IsOwnerOrReadOnly


class AuthorizedMixin(object):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class DeviceViewSetMixin(object):
    lookup_field = "registration_id"

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user)
        return super(DeviceViewSetMixin, self).perform_create(serializer)
