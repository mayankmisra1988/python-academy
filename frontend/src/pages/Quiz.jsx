import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getQuiz, submitQuiz } from "../services/quizService";
import { downloadCertificate } from "../services/certificateService";


import "./Quiz.css";

function Quiz() {
  const { lessonId } = useParams();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);

  const [answers, setAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [timeLeft, setTimeLeft] = useState(null);
  const [downloadingCertificate, setDownloadingCertificate] =
    useState(false);

  // =====================================================
  // LOAD QUIZ
  // =====================================================

  useEffect(() => {
    async function loadQuiz() {
      try {
        setLoading(true);
        setError("");

        console.log("🔥 LOAD QUIZ - LESSON ID:", lessonId);

        const data = await getQuiz(lessonId);

        console.log("🔥 QUIZ DATA:", data);

        setQuiz(data);
        if (data.time_limit) {
          setTimeLeft(Number(data.time_limit) * 60);
        } else {
          setTimeLeft(null);
        }
      } catch (err) {
        console.error("🔥 QUIZ LOADING ERROR:", err);
        console.error(
          "🔥 LOAD ERROR RESPONSE:",
          err?.response?.data
        );

        setError(
          err?.response?.data?.detail ||
          "Unable to load quiz. Please try again."
        );
      } finally {
        setLoading(false);
      }
    }

    if (lessonId) {
      loadQuiz();
    }
  }, [lessonId]);

  // =====================================================
  // SELECT ANSWER
  // =====================================================

  const handleOptionChange = (questionId, optionId) => {
    console.log(
      "🔥 ANSWER SELECTED:",
      questionId,
      optionId
    );

    setAnswers((previous) => ({
      ...previous,
      [questionId]: optionId,
    }));

    setError("");
  };

  // =====================================================
  // SUBMIT QUIZ
  // =====================================================

  const handleSubmit = useCallback(async (isAutoSubmit = false) => {
    console.log("🔥 SUBMIT BUTTON CLICKED");

    // ---------------------------------------------------
    // QUIZ CHECK
    // ---------------------------------------------------

    if (!quiz?.id) {
      console.log("❌ QUIZ ID MISSING");

      setError("Quiz information is missing.");
      return;
    }

    const questions = quiz.questions || [];

    console.log("🔥 QUIZ ID:", quiz.id);
    console.log("🔥 QUESTIONS:", questions);
    console.log("🔥 CURRENT ANSWERS:", answers);

    // ---------------------------------------------------
    // CHECK UNANSWERED
    // ---------------------------------------------------

    const unansweredQuestions = questions.filter(
      (question) =>
        answers[question.id] === undefined
    );

    console.log(
      "🔥 UNANSWERED QUESTIONS:",
      unansweredQuestions
    );

    if (unansweredQuestions.length > 0 && !isAutoSubmit) {
      console.log("❌ SOME QUESTIONS ARE UNANSWERED");

      setError(
        "Please answer all questions before submitting."
      );

      return;
    }

    try {
      setSubmitting(true);
      setError("");

      if (isAutoSubmit) {
        console.log("⏰ TIME UP - AUTO SUBMITTING QUIZ");
      }

      console.log("🔥 STEP 1 - TRY BLOCK");

      // -------------------------------------------------
      // FORMAT ANSWERS
      // -------------------------------------------------

      const formattedAnswers =
        Object.entries(answers).map(
          ([question, option]) => ({
            question: Number(question),
            option: Number(option),
          })
        );

      console.log(
        "🔥 STEP 2 - FORMATTED ANSWERS:",
        formattedAnswers
      );

      console.log(
        "🔥 STEP 3 - SENDING QUIZ ID:",
        quiz.id
      );

      console.log(
        "🔥 STEP 3 - API URL:",
        `/lessons/quizzes/${quiz.id}/submit/`
      );

      // -------------------------------------------------
      // API CALL
      // -------------------------------------------------

      console.log(
        "🔥 STEP 4 - CALLING submitQuiz()"
      );

      const response = await submitQuiz(
        quiz.id,
        formattedAnswers
      );

      // -------------------------------------------------
      // API RESPONSE
      // -------------------------------------------------

      console.log(
        "🔥 STEP 5 - QUIZ RESULT:",
        response
      );

      console.log(
        "🔥 STEP 5 - RESPONSE TYPE:",
        typeof response
      );

      setResult(response);

      console.log(
        "✅ QUIZ RESULT SET SUCCESSFULLY"
      );

    } catch (error) {

      console.error(
        "❌ QUIZ SUBMIT ERROR:",
        error
      );

      console.error(
        "❌ ERROR MESSAGE:",
        error?.message
      );

      console.error(
        "❌ BACKEND STATUS:",
        error?.response?.status
      );

      console.error(
        "❌ BACKEND ERROR:",
        error?.response?.data
      );

      setError(
        error?.response?.data?.answers
          ? "Please check your answers and try again."
          : error?.response?.data?.detail ||
          "Unable to submit quiz. Please try again."
      );

    } finally {

      console.log(
        "🔥 STEP 6 - SUBMIT FINISHED"
      );

      setSubmitting(false);
    }
  }, [quiz, answers]);

  // =====================================================
  // QUIZ TIMER
  // =====================================================

  useEffect(() => {
    if (timeLeft === null || result || submitting) {
      return;
    }

    if (timeLeft <= 0) {
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((previous) => {
        if (previous <= 1) {
          clearInterval(timer);
          return 0;
        }

        return previous - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, result, submitting]);
  useEffect(() => {
    if (timeLeft === 0 && !result && !submitting) {
      handleSubmit(true);
    }
  }, [timeLeft, result, submitting, handleSubmit]);
  // =====================================================
  // TIME FORMAT
  // =====================================================

  const formatTime = (seconds) => {
    if (seconds === null) return "";

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    return `${String(minutes).padStart(2, "0")}:${String(
      remainingSeconds
    ).padStart(2, "0")}`;
  };

  // =====================================================
  // DOWNLOAD CERTIFICATE
  // =====================================================

  const handleDownloadCertificate = async () => {
    const certificateId =
      result?.certificate?.id;

    if (!certificateId) {
      setError(
        "Certificate is not available yet."
      );
      return;
    }

    try {
      setDownloadingCertificate(true);
      setError("");

      await downloadCertificate(
        certificateId
      );

    } catch (err) {

      console.error(
        "Certificate download error:",
        err
      );

      setError(
        "Certificate could not be downloaded. Please try again."
      );

    } finally {
      setDownloadingCertificate(false);
    }
  };

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return (
      <div className="quiz-page">
        <div className="quiz-card">
          <h2>Loading Quiz...</h2>
        </div>
      </div>
    );
  }

  // =====================================================
  // QUIZ NOT FOUND
  // =====================================================

  if (!quiz) {
    return (
      <div className="quiz-page">
        <div className="quiz-card">

          <h2>No Quiz Found</h2>

          <p>
            {error ||
              "This lesson does not have a quiz yet."}
          </p>

          <button
            className="submit-quiz-btn"
            onClick={() => navigate(-1)}
          >
            ← Back to Lesson
          </button>

        </div>
      </div>
    );
  }

  const questions = quiz.questions || [];

  const answeredCount =
    Object.keys(answers).length;

  const isSubmitDisabled =
    submitting ||
    answeredCount !== questions.length;

  // =====================================================
  // MAIN
  // =====================================================

  return (
    <div className="quiz-page">

      <div className="quiz-card">

        {/* =================================================
            QUIZ HEADER
        ================================================= */}

        <div className="quiz-header">

          <span className="quiz-label">
            📝 QUIZ
          </span>

          <h1>
            {quiz.title}
          </h1>

          {quiz.description && (
            <p>
              {quiz.description}
            </p>
          )}

          <div className="quiz-meta">

            <span>
              📋 {questions.length} Questions
            </span>

            {quiz.time_limit && timeLeft !== null && (
              <span
                className={
                  timeLeft <= 60
                    ? "timer-warning"
                    : "quiz-timer"
                }
              >
                ⏱ Time Left: {formatTime(timeLeft)}
              </span>
            )}

            {quiz.passing_score !== undefined && (
              <span>
                🎯 Passing Score:{" "}
                {quiz.passing_score}%
              </span>
            )}

          </div>

        </div>

        {/* =================================================
            ERROR
        ================================================= */}

        {error && (
          <div className="quiz-error">
            ⚠️ {error}
          </div>
        )}

        {/* =================================================
            RESULT
        ================================================= */}

        {result && (
          <div className="quiz-result-card">

            <h2>
              🎉 Quiz Completed
            </h2>

            <div className="result-stats">

              <p>
                <strong>
                  Correct Answers:
                </strong>{" "}
                {result.correct_answers}
              </p>

              <p>
                <strong>
                  Total Questions:
                </strong>{" "}
                {result.total_questions}
              </p>

              <p>
                <strong>
                  Percentage:
                </strong>{" "}
                {result.percentage}%
              </p>

            </div>

            <h3
              className={
                result.passed
                  ? "quiz-passed"
                  : "quiz-failed"
              }
            >
              {result.passed
                ? "✅ Passed"
                : "❌ Failed"}
            </h3>

            {/* PASSED */}

            {result.passed && (
              <div className="quiz-success">

                <p>
                  Congratulations! You passed
                  the quiz.
                </p>

                <button
                  className="submit-quiz-btn"
                  onClick={() =>
                    navigate(-1)
                  }
                >
                  ← Back to Lesson
                </button>

                {result.certificate?.id && (
                  <button
                    className="submit-quiz-btn"
                    onClick={
                      handleDownloadCertificate
                    }
                    disabled={
                      downloadingCertificate
                    }
                  >
                    {downloadingCertificate
                      ? "Downloading..."
                      : "🏆 Download Certificate"}
                  </button>
                )}

              </div>
            )}

            {/* FAILED */}

            {!result.passed && (
              <div className="quiz-failed-box">

                <p>
                  You did not pass this time.
                  You can review the lesson
                  and try again.
                </p>

                <button
                  className="submit-quiz-btn"
                  onClick={() =>
                    window.location.reload()
                  }
                >
                  🔄 Try Again
                </button>

              </div>
            )}

          </div>
        )}

        {/* =================================================
            QUESTIONS
        ================================================= */}

        {!result && (
          <div className="quiz-questions">

            {questions.map(
              (question, index) => (

                <div
                  key={question.id}
                  className="quiz-question"
                >

                  <h3>
                    {index + 1}.{" "}
                    {question.question}
                  </h3>

                  <div className="quiz-options">

                    {(question.options || []).map(
                      (option) => {

                        const isSelected =
                          answers[
                          question.id
                          ] === option.id;

                        return (

                          <label
                            key={option.id}
                            className={
                              isSelected
                                ? "quiz-option selected"
                                : "quiz-option"
                            }
                          >

                            <input
                              type="radio"
                              name={`question-${question.id}`}
                              value={option.id}
                              checked={
                                isSelected
                              }
                              onChange={() =>
                                handleOptionChange(
                                  question.id,
                                  option.id
                                )
                              }
                            />

                            <span>
                              {option.option_text}
                            </span>

                          </label>

                        );

                      }
                    )}

                  </div>

                </div>

              )
            )}

            {/* =================================================
                SUBMIT
            ================================================= */}

            <div className="quiz-submit-area">

              <p>
                {answeredCount}
                {" / "}
                {questions.length}
                {" questions answered"}
              </p>

              <button
                type="button"
                className="submit-quiz-btn"
                onClick={handleSubmit}
                disabled={isSubmitDisabled}
              >
                {submitting
                  ? "Submitting..."
                  : "Submit Quiz →"}
              </button>

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default Quiz;