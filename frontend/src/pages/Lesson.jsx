import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import LessonSidebar from "../components/Lesson/LessonSidebar";
import LessonPlayer from "../components/Lesson/LessonPlayer";
import LessonNavigation from "../components/Lesson/LessonNavigation";
import LessonResources from "../components/Lesson/LessonResources";
import ProgressBar from "../components/Lesson/ProgressBar";

import { getLesson } from "../services/lessonService";
import { getCurriculum } from "../services/courseService";

import "../components/Lesson/Lesson.css";

function Lesson() {
  const { lessonId } = useParams();

  const [lesson, setLesson] = useState(null);
  const [curriculum, setCurriculum] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLesson() {
      try {
        const data = await getLesson(lessonId);
        setLesson(data);

        const curriculumData = await getCurriculum(data.course_id);
        setCurriculum(curriculumData);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchLesson();
  }, [lessonId]);

  if (loading) {
    return <h2>Loading...</h2>;
  }

  if (!lesson) {
    return <h2>Lesson not found.</h2>;
  }

  return (
    <div className="lesson-page">
      <aside className="lesson-sidebar">
        <LessonSidebar curriculum={curriculum} lesson={lesson} />
      </aside>

      <main className="lesson-content">
        <LessonPlayer lesson={lesson} />

        <LessonResources lesson={lesson} />

        <ProgressBar lesson={lesson} />

        <LessonNavigation lesson={lesson} curriculum={curriculum} />
      </main>
    </div>
  );
}

export default Lesson;
