import axios from "axios";

// Base URL ko Environment Variable se connect kiya gaya hai
const BASE_URL = process.env.REACT_APP_API_URL
  ? `${process.env.REACT_APP_API_URL}/api`
  : "https://python-academy-backend.onrender.com/api";

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
        // Here also dynamic BASE_URL is used instead of hardcoded 127.0.0.1
        const response = await axios.post(
          `${BASE_URL}/auth/token/refresh/`,
          {
            refresh: refreshToken,
          }
        );

        const newAccessToken = response.data.access;

        localStorage.setItem("access", newAccessToken);

        originalRequest.headers.Authorization =
          `Bearer ${newAccessToken}`;

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