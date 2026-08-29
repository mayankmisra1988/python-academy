import { Link } from "react-router-dom";
import "./LessonNavigation.css";

export default function LessonNavigation({
  lesson,
  curriculum = [],
}) {

  // =====================================================
  // SAFETY CHECK
  // =====================================================

  if (!lesson) {
    return null;
  }


  // =====================================================
  // CREATE FLAT LESSON LIST
  // =====================================================

  const lessons = curriculum.flatMap((section) => {

    if (!section || !Array.isArray(section.lessons)) {
      return [];
    }

    return section.lessons.filter(
      (item) => item && item.id
    );

  });


  // =====================================================
  // FIND CURRENT LESSON
  // =====================================================

  const currentIndex = lessons.findIndex(
    (item) =>
      Number(item.id) === Number(lesson.id)
  );


  // =====================================================
  // PREVIOUS / NEXT
  // =====================================================

  const previousLesson =
    currentIndex > 0
      ? lessons[currentIndex - 1]
      : null;

  const nextLesson =
    currentIndex >= 0 &&
    currentIndex < lessons.length - 1
      ? lessons[currentIndex + 1]
      : null;


  // =====================================================
  // COURSE SLUG
  // =====================================================

  const courseSlug =
    lesson.course_slug || "";


  return (

    <div className="lesson-navigation">

      {/* ================= PREVIOUS ================= */}

      {previousLesson && courseSlug ? (

        <Link
          to={`/courses/${courseSlug}/lesson/${previousLesson.id}`}
          className="nav-btn previous-btn"
        >
          ← Previous
        </Link>

      ) : (

        <button
          className="nav-btn previous-btn"
          disabled
        >
          ← Previous
        </button>

      )}


      {/* ================= NEXT ================= */}

      {nextLesson && courseSlug ? (

        <Link
          to={`/courses/${courseSlug}/lesson/${nextLesson.id}`}
          className="nav-btn next-btn"
        >
          Next →
        </Link>

      ) : (

        <button
          className="nav-btn next-btn"
          disabled
        >
          Next →
        </button>

      )}

    </div>

  );
}