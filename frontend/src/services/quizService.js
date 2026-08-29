import api from "./api";

// =====================================================
// GET QUIZ
// =====================================================

export const getQuiz = async (lessonId) => {
  const response = await api.get(
    `/lessons/${lessonId}/quiz/`
  );

  return response.data;
};


// =====================================================
// SUBMIT QUIZ
// =====================================================

export const submitQuiz = async (quizId, answers) => {
  const response = await api.post(
    `/lessons/quizzes/${quizId}/submit/`,
    {
      answers,
    }
  );

  return response.data;
};