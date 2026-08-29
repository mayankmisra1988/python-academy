from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollmentListCreateView(generics.ListCreateAPIView):

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Enrollment.objects.filter(user=self.request.user).select_related("course","course__category",
                "course__instructor",
            )
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EnrollmentDetailView(generics.RetrieveAPIView):

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            user=self.request.user
        ).select_related("course")