import { useNavigate } from "react-router-dom";

export default function LessonCard({ lesson, slug }) {
  const navigate = useNavigate();

  const handleStartLesson = () => {
    navigate(`/courses/${slug}/lesson/${lesson.id}`);
  };

  return (
    <div className="lesson-card">
      <div>
        <h4>{lesson.title}</h4>
        <p>{lesson.description}</p>
      </div>

      <div className="lesson-actions">
        {lesson.notes && (
          <a
            href={lesson.notes}
            target="_blank"
            rel="noreferrer"
          >
            📄 Notes
          </a>
        )}

        {lesson.quiz && (
          <button>
            📝 Quiz
          </button>
        )}

        <button onClick={handleStartLesson}>
          ▶ Start
        </button>
      </div>
    </div>
  );
}