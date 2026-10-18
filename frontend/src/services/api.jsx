import axios from "axios";

const getBaseUrl = () => {
  const envUrl = process.env.REACT_APP_API_URL?.trim();

  if (envUrl) {
    let url = envUrl.replace(/\/+$/, "");

    if (!/^https?:\/\//i.test(url)) {
      url = `https://${url}`;
    }

    return url.endsWith("/api") ? url : `${url}/api`;
  }

  const hostname = window.location.hostname;

  const isLocalhost =
    hostname === "localhost" ||
    hostname === "127.0.0.1" ||
    hostname.startsWith("192.168.");

  return isLocalhost
    ? "http://127.0.0.1:8000/api"
    : "https://python-academy-backend.onrender.com/api";
};

const BASE_URL = getBaseUrl();

console.log("API BASE URL:", BASE_URL);

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Attach access token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Refresh expired access token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      originalRequest.url?.includes("/auth/token/refresh/")
    ) {
      return Promise.reject(error);
    }

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
        { refresh: refreshToken },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const newAccessToken = response.data.access;

      localStorage.setItem("access", newAccessToken);

      originalRequest.headers =
        originalRequest.headers || {};

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
);

export default api;