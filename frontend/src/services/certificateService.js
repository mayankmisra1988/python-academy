// import api from "./api";

// // Get all certificates of logged-in user
// export const getCertificates = async () => {
//   const response = await api.get("/certificates/");
//   return response.data;
// };

// // Generate certificate
// export const generateCertificate = async (courseId) => {
//   const response = await api.post(
//     `/certificates/generate/${courseId}/`
//   );

//   return response.data;
// };

// // Download certificate
// export const downloadCertificate = async (certificateId) => {
//   const response = await api.get(
//     `/certificates/download/${certificateId}/`,
//     {
//       responseType: "blob",
//     }
//   );

//   const url = window.URL.createObjectURL(
//     new Blob([response.data])
//   );

//   const link = document.createElement("a");

//   link.href = url;

//   link.setAttribute(
//     "download",
//     `certificate-${certificateId}.pdf`
//   );

//   document.body.appendChild(link);

//   link.click();

//   link.remove();
// };






import api from "./api";
export const getCertificates = async () => {
  try {
    const response = await api.get("/certificates/");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch certificates:", error);
    throw error;
  }
};

/**
 * Generate a new certificate for a specific course
 */
export const generateCertificate = async (courseId) => {
  try {
    const response = await api.post(`/certificates/generate/${courseId}/`);
    return response.data;
  } catch (error) {
    console.error(`Failed to generate certificate for course ${courseId}:`, error);
    throw error;
  }
};

/**
 * Download a certificate PDF
 */
export const downloadCertificate = async (certificateId) => {
  try {
    const response = await api.get(`/certificates/download/${certificateId}/`, {
      responseType: "blob",
    });

    // Extract filename from Header if available, otherwise use default
    const disposition = response.headers["content-disposition"];
    let filename = `certificate-${certificateId}.pdf`;

    if (disposition && disposition.includes("filename=")) {
      const match = disposition.match(/filename="?([^"]+)"?/);
      if (match && match[1]) {
        filename = match[1];
      }
    }

    // Create temporary download URL
    const blob = new Blob([response.data], { type: response.headers["content-type"] || "application/pdf" });
    const url = window.URL.createObjectURL(blob);

    // Create invisible anchor link to trigger download
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();

    // Cleanup DOM and free memory
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(`Failed to download certificate ${certificateId}:`, error);
    throw error;
  }
};