from rest_framework import generics, status
from .models import Certificate
from .serializers import CertificateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from courses.models import Course
from enrollments.models import Enrollment

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .utils import generate_certificate_pdf 

from django.http import FileResponse

class CertificateListView(generics.ListAPIView):

    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return (
            Certificate.objects.filter(
                user=self.request.user
            )
            .select_related("course")
        )

class CertificateDetailView(generics.RetrieveAPIView):

    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return (
            Certificate.objects.filter(
                user=self.request.user
            )
            .select_related("course")
        )

class GenerateCertificateView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CertificateSerializer

    def post(self, request, course_id):

        course = get_object_or_404(
            Course,
            id=course_id,
            is_published=True,
        )

        enrollment = Enrollment.objects.filter(
            user=request.user,
            course=course,
            is_active=True,
        ).first()

        if not enrollment:
            return Response(
                {
                    "error": "You are not enrolled in this course."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not enrollment.completed:
            return Response(
                {
                    "error": "Complete the course first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        certificate = Certificate.objects.filter(
            user=request.user,
            course=course,
        ).first()

        if certificate:

            if not certificate.pdf:
                generate_certificate_pdf(certificate)

            serializer = CertificateSerializer(
                certificate,
                context={"request": request},
            )

            return Response(serializer.data)

        certificate = Certificate.objects.create(
            user=request.user,
            course=course,
        )
        generate_certificate_pdf(certificate)

        serializer = CertificateSerializer(
            certificate,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class DownloadCertificateView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CertificateSerializer

    def get(self, request, pk):

        certificate = get_object_or_404(
            Certificate,
            pk=pk,
            user=request.user,
        )
        if not certificate.pdf:
            return Response(
                {"detail": "Certificate not generated yet."},
                status=400
            )

        return FileResponse(
            certificate.pdf.open("rb"),
            as_attachment=True,
            filename=f"{certificate.certificate_id}.pdf",
        )
class VerifyCertificateView(APIView):

    permission_classes = [AllowAny]
    serializer_class = CertificateSerializer

    def get(self, request, certificate_id):
        certificate = get_object_or_404(
            Certificate,
            certificate_id=certificate_id,
        )

        serializer = CertificateSerializer(
            certificate,
            context={"request": request},
        )

        data = serializer.data

        data["student"] = (
            certificate.user.get_full_name()
            or certificate.user.username
        )

        data["valid"] = True

        return Response(data)