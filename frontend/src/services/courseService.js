// import api from "./api";

// // Get All Courses
// export const getCourses = async () => {
//   const response = await api.get("/courses/");
//   return response.data;
// };

// // Get Course Details
// export const getCourseDetails = async (slug) => {
//   const response = await api.get(`/courses/${slug}/`);
//   return response.data;
// };

// // Get Curriculum
// export const getCurriculum = async (courseId) => {
//   const response = await api.get(
//     `/lessons/courses/${courseId}/curriculum/`
//   );
//   return response.data;
// };



import api from "./api";

// Get All Courses
export const getCourses = async () => {
  try {
    const response = await api.get("/courses/");
    
    // Check if response data is an Array or Django REST Paginated ({ results: [] })
    if (Array.isArray(response.data)) {
      return response.data;
    } else if (response.data && Array.isArray(response.data.results)) {
      return response.data.results;
    }
    
    return []; // Return empty array if backend response format is unexpected
  } catch (error) {
    console.error("Error fetching courses:", error);
    return []; // Fallback empty array on network/CORS failure
  }
};

// Get Course Details
export const getCourseDetails = async (slug) => {
  try {
    const response = await api.get(`/courses/${slug}/`);
    return response.data || null;
  } catch (error) {
    console.error(`Error fetching course details for ${slug}:`, error);
    return null;
  }
};

// Get Curriculum
export const getCurriculum = async (courseId) => {
  try {
    const response = await api.get(
      `/lessons/courses/${courseId}/curriculum/`
    );
    
    if (Array.isArray(response.data)) {
      return response.data;
    } else if (response.data && Array.isArray(response.data.results)) {
      return response.data.results;
    }
    
    return [];
  } catch (error) {
    console.error(`Error fetching curriculum for course ${courseId}:`, error);
    return [];
  }
};


