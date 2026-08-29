from django.urls import path

from .views import (
    CertificateListView,
    CertificateDetailView,
    GenerateCertificateView,
    DownloadCertificateView,
    VerifyCertificateView,
)

urlpatterns = [
    path(
        "",
        CertificateListView.as_view(),
        name="certificate-list",
    ),

    path(
        "<int:pk>/",
        CertificateDetailView.as_view(),
        name="certificate-detail",
    ),

    path(
        "generate/<int:course_id>/",
        GenerateCertificateView.as_view(),
        name="certificate-generate",
    ),

    path(
        "download/<int:pk>/",
        DownloadCertificateView.as_view(),
        name="certificate-download",
    ),

    path(
        "verify/<str:certificate_id>/",
        VerifyCertificateView.as_view(),
        name="certificate-verify",
    ),
]