import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getLesson,
  getLessonProgress,
  createLessonProgress,
  updateLessonProgress,
} from "../../services/lessonService";

import LessonSidebar from "./LessonSidebar";
import LessonPlayer from "./LessonPlayer";
import ProgressBar from "./ProgressBar";
import LessonNavigation from "./LessonNavigation";
import LessonResources from "./LessonResources";
import "./Lesson.css";

function Lesson() {
  const { lessonId } = useParams();

  const [lesson, setLesson] = useState(null);
  const [curriculum, setCurriculum] = useState([]);
  const [progress, setProgress] = useState({
    id: null,
    completed: false,
    watched_percentage: 0,
  });
  const [loading, setLoading] = useState(true);

  const lastSavedProgress = useRef(0);
  const savingProgress = useRef(false);

  useEffect(() => {
    let mounted = true;

    const loadLessonData = async () => {
      try {
        setLoading(true);

        const lessonData = await getLesson(lessonId);
        if (!mounted) return;
        setLesson(lessonData);

        if (lessonData?.course_id) {
          const response = await fetch(
            `http://127.0.0.1:8000/api/lessons/courses/${lessonData.course_id}/curriculum/`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
              },
            }
          );

          if (!response.ok) throw new Error(`Curriculum error: ${response.status}`);

          const data = await response.json();
          if (mounted) setCurriculum(Array.isArray(data) ? data : []);
        }

        const progressData = await getLessonProgress();
        if (!mounted) return;

        if (Array.isArray(progressData)) {
          const saved = progressData.find(
            (item) => Number(item.lesson) === Number(lessonId)
          );

          if (saved) {
            const watched = Math.min(
              100,
              Math.max(0, Number(saved.watched_percentage) || 0)
            );

            setProgress({
              id: saved.id,
              completed: Boolean(saved.completed) || watched >= 100,
              watched_percentage: watched,
            });

            lastSavedProgress.current = watched;
            console.log("⏩ Saved progress loaded:", watched + "%");
          } else {
            lastSavedProgress.current = 0;
          }
        }
      } catch (error) {
        console.error("❌ Lesson loading error:", error);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    loadLessonData();

    return () => { mounted = false; };
  }, [lessonId]);

  const saveProgress = async (watchedPercentage, completed = false) => {
    const percentage = Math.min(
      100,
      Math.max(0, Math.round(Number(watchedPercentage) || 0))
    );

    if (savingProgress.current) return;

    const shouldBeCompleted = completed || percentage >= 95;
    const finalPercentage = Math.max(percentage, lastSavedProgress.current);

    if (
      finalPercentage === lastSavedProgress.current &&
      shouldBeCompleted === progress.completed
    ) return;

    savingProgress.current = true;

    try {
      let response;

      if (!progress.id) {
        response = await createLessonProgress({
          lesson: Number(lessonId),
          watched_percentage: finalPercentage,
          completed: shouldBeCompleted,
        });
      } else {
        response = await updateLessonProgress(progress.id, {
          watched_percentage: finalPercentage,
          completed: shouldBeCompleted,
        });
      }

      const saved = response?.data || response;

      setProgress((previous) => ({
        id: saved?.id || previous.id,
        watched_percentage:
          Number(saved?.watched_percentage) || finalPercentage,
        completed: saved?.completed ?? shouldBeCompleted,
      }));

      lastSavedProgress.current = Math.max(
        lastSavedProgress.current,
        finalPercentage
      );

      console.log("✅ Progress Saved:", {
        lesson: lessonId,
        watched_percentage: finalPercentage,
        completed: shouldBeCompleted,
      });
    } catch (error) {
      console.error("❌ Progress save error:", error);
    } finally {
      savingProgress.current = false;
    }
  };

  const handleVideoProgress = (percentage) => {
    const current = Math.min(100, Math.max(0, Number(percentage) || 0));

    setProgress((previous) => ({
      ...previous,
      watched_percentage: Math.max(previous.watched_percentage || 0, current),
    }));

    if (current >= lastSavedProgress.current + 5) {
      saveProgress(current, current >= 95);
    }

    if (current >= 100) saveProgress(100, true);
  };

  const handleComplete = async () => {
    await saveProgress(100, true);
  };

  if (loading) {
    return <div className="lesson-loading">Loading lesson...</div>;
  }

  if (!lesson) {
    return <div className="lesson-error">Lesson not found.</div>;
  }

  return (
    <div className="lesson-page">
      <LessonSidebar
        curriculum={curriculum}
        currentLessonId={Number(lessonId)}
      />

      <main className="lesson-main">
        <LessonPlayer
          lesson={lesson}
          progress={progress.watched_percentage}
          onProgress={handleVideoProgress}
          onComplete={handleComplete}
        />

        <ProgressBar
          progress={progress.watched_percentage}
          completed={progress.completed}
          onComplete={handleComplete}
        />

        <LessonResources lesson={lesson} />

        <LessonNavigation
          curriculum={curriculum}
          currentLessonId={Number(lessonId)}
        />
      </main>
    </div>
  );
}

export default Lesson;