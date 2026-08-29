import { Link } from "react-router-dom";
import "./Courses.css";

export default function CourseCard({ course }) {
  return (
    <div className="home-course-card">

      <div className="course-image">
        <img
          src={course.thumbnail}
          alt={course.title}
        />
      </div>

      <div className="course-content">

        <span className="course-badge">
          {course.level.toUpperCase()}
        </span>

        <h3 title={course.title}>
          {course.title}
        </h3>

        <p title={course.short_description}>
          {course.short_description}
        </p>

        <div className="course-meta">
          <span>📂 {course.category?.name}</span>
        </div>

        <div className="course-footer">

          <h4>
            {course.is_free ? "FREE" : `₹${course.price}`}
          </h4>

          <Link to={`/courses/${course.slug}`}>
            <button>
              View Course
            </button>
          </Link>

        </div>

      </div>

    </div>
  );
}