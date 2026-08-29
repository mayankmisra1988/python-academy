import { useEffect, useState } from "react";

import {
  getCertificates,
  downloadCertificate,
} from "../services/certificateService";

import "./Certificates.css";
import PageSkeleton from "../components/PageSkeleton";

function Certificates() {
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState(null);
  const [error, setError] = useState("");

  // =====================================================
  // LOAD CERTIFICATES
  // =====================================================

  useEffect(() => {
    let mounted = true;

    const loadCertificates = async () => {
      try {
        setLoading(true);
        setError("");

        console.log("🔥 LOADING CERTIFICATES...");

        const data = await getCertificates();

        console.log("🏆 CERTIFICATES API RESPONSE:", data);

        if (mounted) {
          setCertificates(
            Array.isArray(data) ? data : []
          );
        }
      } catch (error) {
        console.error(
          "❌ Certificates loading error:",
          error
        );

        console.error(
          "❌ Backend response:",
          error?.response?.data
        );

        if (mounted) {
          setError(
            "Unable to load certificates. Please try again."
          );
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadCertificates();

    return () => {
      mounted = false;
    };
  }, []);

  // =====================================================
  // DOWNLOAD CERTIFICATE
  // =====================================================

  const handleDownload = async (certificateId) => {
    try {
      setDownloadingId(certificateId);
      setError("");

      console.log(
        "📄 DOWNLOADING CERTIFICATE:",
        certificateId
      );

      await downloadCertificate(certificateId);

      console.log(
        "✅ CERTIFICATE DOWNLOAD SUCCESS"
      );
    } catch (error) {
      console.error(
        "❌ Certificate download error:",
        error
      );

      console.error(
        "❌ Backend response:",
        error?.response?.data
      );

      setError(
        "Unable to download certificate. Please try again."
      );
    } finally {
      setDownloadingId(null);
    }
  };

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return <PageSkeleton />;
  }

  // =====================================================
  // PAGE
  // =====================================================

  return (
    <div className="certificates-page page-fade-in">

      {/* HEADER */}

      <div className="certificates-header">

        <span className="certificates-eyebrow">
          PYTHON ACADEMY
        </span>

        <h1>
          🏆 My Certificates
        </h1>

        <p>
          Certificates you have earned from
          Python Academy.
        </p>

        {certificates.length > 0 && (
          <div className="certificate-count">
            {certificates.length}{" "}
            {certificates.length === 1
              ? "Certificate"
              : "Certificates"} Earned
          </div>
        )}

      </div>

      {/* ERROR */}

      {error && (
        <div className="certificate-error">
          ⚠️ {error}
        </div>
      )}

      {/* EMPTY */}

      {!error && certificates.length === 0 && (
        <div className="certificate-empty">

          <div className="certificate-empty-icon">
            🏆
          </div>

          <h2>
            No Certificates Yet
          </h2>

          <p>
            Complete your courses and pass the
            required quizzes to earn certificates.
          </p>

        </div>
      )}

      {/* CERTIFICATES */}

      {certificates.length > 0 && (
        <div className="certificate-grid">

          {certificates.map((certificate) => (
            <article
              key={certificate.id}
              className="certificate-card"
            >

              {/* THUMBNAIL */}

              <div className="certificate-image-wrapper">

                {certificate.thumbnail ? (
                  <img
                    src={certificate.thumbnail}
                    alt={
                      certificate.course_title ||
                      "Course Certificate"
                    }
                    className="certificate-thumbnail"
                  />
                ) : (
                  <div className="certificate-thumbnail-placeholder">
                    🏆
                  </div>
                )}

                <div className="certificate-earned-badge">
                  ✓ Earned
                </div>

              </div>

              {/* CONTENT */}

              <div className="certificate-card-content">

                <span className="certificate-label">
                  COURSE CERTIFICATE
                </span>

                <h2>
                  {certificate.course_title ||
                    "Course Certificate"}
                </h2>

                {/* INFO */}

                <div className="certificate-details">

                  <div className="certificate-info">
                    <span>
                      Certificate ID
                    </span>

                    <strong>
                      {certificate.certificate_id ||
                        "N/A"}
                    </strong>
                  </div>

                  <div className="certificate-info">
                    <span>
                      Issued On
                    </span>

                    <strong>
                      {certificate.issued_at
                        ? new Date(
                            certificate.issued_at
                          ).toLocaleDateString(
                            "en-IN",
                            {
                              day: "2-digit",
                              month: "short",
                              year: "numeric",
                            }
                          )
                        : "N/A"}
                    </strong>
                  </div>

                </div>

                {/* ACTIONS */}

                <div className="certificate-actions">

                  <button
                    type="button"
                    className="download-btn"
                    onClick={() =>
                      handleDownload(
                        certificate.id
                      )
                    }
                    disabled={
                      downloadingId ===
                      certificate.id
                    }
                  >
                    {downloadingId ===
                    certificate.id
                      ? "⏳ Downloading..."
                      : "📄 Download"}
                  </button>

                  {certificate.pdf ? (
                    <a
                      href={certificate.pdf}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="view-btn"
                    >
                      👁 View
                    </a>
                  ) : (
                    <button
                      type="button"
                      className="view-btn disabled"
                      disabled
                    >
                      👁 View Unavailable
                    </button>
                  )}

                </div>

              </div>

            </article>
          ))}

        </div>
      )}

    </div>
  );
}

export default Certificates;