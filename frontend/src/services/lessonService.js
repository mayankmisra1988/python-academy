import api from "./api";

// Get single lesson details
export const getLesson = async (lessonId) => {
  const response = await api.get(`/lessons/${lessonId}/`);
  return response.data;
};

// Get current user's lesson progress
export const getLessonProgress = async () => {
  const response = await api.get("/lessons/progress/");
  return response.data;
};

// Create lesson progress
export const createLessonProgress = async (data) => {
  const response = await api.post("/lessons/progress/", data);
  return response.data;
};

// Update lesson progress
export const updateLessonProgress = async (id, data) => {
  const response = await api.patch(`/lessons/progress/${id}/`, data);
  return response.data;
};