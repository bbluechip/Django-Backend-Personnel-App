from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.response import Response
from rest_framework import generics, status


class DeparmentView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated, IsStafforReadOnly]


class PersonnelListCreateView(generics.ListCreateAPIView):
    serializer_class = PersonnelSerializer
    queryset = Personnel.objects.all()
    # permission_classes = [IsAuthenticated, IsStafforReadOnly]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.request.user.is_staff:
            personnel = self.perform_create(serializer)
            data = {
                'message': f'Personnel {personnel.first_name} saved successfully',
                'personnel': serializer.data
            }
        else:
            data = {
                'message': 'You are not authorized to perform this operation'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        person = serializer.save()
        person.create_user = self.request.user
        person.save()
        return person


class PersonalGetUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [IsAuthenticated, IsOwnerAndStaffOrReadOnly]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff and (instance.create_user == self.request.user):
            return self.update(request, *args, **kwargs)
        else:
            data = {
                'message': 'Your are not authorizated to perform this action'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        else:
            data = {
                'message': 'You are not authorizated to perform this action'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
