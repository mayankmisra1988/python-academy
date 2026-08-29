// import axios from "axios";

// const api = axios.create({
//   baseURL: "http://127.0.0.1:8000/api",
//   headers: {
//     "Content-Type": "application/json",
//   },
// });

// // Add access token to every request
// api.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem("access");

//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }

//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// // Refresh access token when it expires
// api.interceptors.response.use(
//   (response) => response,

//   async (error) => {
//     const originalRequest = error.config;

//     if (
//       error.response?.status === 401 &&
//       !originalRequest._retry
//     ) {
//       originalRequest._retry = true;

//       const refreshToken = localStorage.getItem("refresh");

//       if (!refreshToken) {
//         localStorage.removeItem("access");
//         localStorage.removeItem("refresh");
//         localStorage.removeItem("user");

//         window.location.href = "/login";

//         return Promise.reject(error);
//       }

//       try {
//         const response = await axios.post(
//           "http://127.0.0.1:8000/api/auth/token/refresh/",
//           {
//             refresh: refreshToken,
//           }
//         );

//         const newAccessToken = response.data.access;

//         localStorage.setItem("access", newAccessToken);

//         originalRequest.headers.Authorization =
//           `Bearer ${newAccessToken}`;

//         return api(originalRequest);
//       } catch (refreshError) {
//         localStorage.removeItem("access");
//         localStorage.removeItem("refresh");
//         localStorage.removeItem("user");

//         window.location.href = "/login";

//         return Promise.reject(refreshError);
//       }
//     }

//     return Promise.reject(error);
//   }
// );

// export default api;








import axios from "axios";

// Environment detection logic for Local vs Production
const getBaseUrl = () => {
  // 1. Check if explicitly defined in .env file
  if (process.env.REACT_APP_API_URL) {
    const cleanUrl = process.env.REACT_APP_API_URL.replace(/\/+$/, "");
    return cleanUrl.endsWith("/api") ? cleanUrl : `${cleanUrl}/api`;
  }

  // 2. Auto-detect if running on local development machine
  const isLocalhost = Boolean(
    window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1" ||
      window.location.hostname.startsWith("192.168.")
  );

  if (isLocalhost) {
    return "http://127.0.0.1:8000/api";
  }

  // 3. Fallback to production backend
  return "https://python-academy-backend.onrender.com/api";
};

const BASE_URL = getBaseUrl();

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add access token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Refresh access token when it expires
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh");

      if (!refreshToken) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");

        window.location.href = "/login";

        return Promise.reject(error);
      }

      try {
        const response = await axios.post(
          `${BASE_URL}/auth/token/refresh/`,
          {
            refresh: refreshToken,
          }
        );

        const newAccessToken = response.data.access;

        localStorage.setItem("access", newAccessToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user");

        window.location.href = "/login";

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;