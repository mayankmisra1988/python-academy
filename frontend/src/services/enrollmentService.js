import api from "./api";

// My Enrolled Courses
export const getMyCourses = async () => {
  const response = await api.get("/enrollments/");
  return response.data;
};

// Enroll in a Course
export const enrollCourse = async (courseId) => {
  const response = await api.post("/enrollments/", {
    course: courseId,
  });

  return response.data;
};

// Get Single Enrollment
export const getEnrollment = async (id) => {
  const response = await api.get(`/enrollments/${id}/`);
  return response.data;
};