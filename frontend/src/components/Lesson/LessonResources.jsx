import './LessonResources.css';
function LessonResources({ lesson }) {
  if (!lesson) return null;

  return (
    <div className="lesson-resources">
      <h3>Lesson Resources</h3>

      <p>
        No additional resources available for this lesson.
      </p>
    </div>
  );
}

export default LessonResources;