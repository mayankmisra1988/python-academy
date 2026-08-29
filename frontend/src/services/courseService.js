import api from "./api";

// Get All Courses
export const getCourses = async () => {
  const response = await api.get("/courses/");
  return response.data;
};

// Get Course Details
export const getCourseDetails = async (slug) => {
  const response = await api.get(`/courses/${slug}/`);
  return response.data;
};

// Get Curriculum
export const getCurriculum = async (courseId) => {
  const response = await api.get(
    `/lessons/courses/${courseId}/curriculum/`
  );
  return response.data;
};