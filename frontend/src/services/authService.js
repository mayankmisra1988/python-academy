import api from "./api";

export const registerUser = async (data) => {
  const response = await api.post("/auth/register/", data);
  return response.data;
};

export const loginUser = async (data) => {
  const response = await api.post("/auth/login/", data);

  localStorage.setItem("access", response.data.access);
  localStorage.setItem("refresh", response.data.refresh);
  localStorage.setItem("user", JSON.stringify(response.data.user));

  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("user");
};

export const isAuthenticated = () => {
  return !!localStorage.getItem("access");
};

// 👇 Ye function add karo
export const changePassword = async (data) => {
  const response = await api.post("/auth/change-password/", data);
  return response.data;
};  