import api from "./api";

// Register
export const registerUser = async (data) => {
  const response = await api.post("/auth/register/", data);
  return response.data;
};

// Login
export const loginUser = async (data) => {
  const response = await api.post("/auth/login/", data);

  localStorage.setItem("access", response.data.access);
  localStorage.setItem("refresh", response.data.refresh);
  localStorage.setItem("user", JSON.stringify(response.data.user));

  return response.data;
};

// Logout
export const logoutUser = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("user");
};

// Authentication
export const isAuthenticated = () => {
  return !!localStorage.getItem("access");
};

// Change Password
export const changePassword = async (data) => {
  const response = await api.post("/auth/change-password/", data);
  return response.data;
};

// Get Profile
export const getProfile = async () => {
  const response = await api.get("/auth/profile/");
  return response.data;
};

// Update Profile
export const updateProfile = async (data) => {
  const response = await api.put("/auth/profile/", data);
  return response.data;
};

// Forgot Password
export const forgotPassword = async (email) => {
  const response = await api.post("/auth/forgot-password/", { email });
  return response.data;
};

// Reset Password
export const resetPassword = async (data) => {
  const response = await api.post("/auth/reset-password/", data);
  return response.data;
};
