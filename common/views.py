from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        created_by=self.request.user,
                        modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)