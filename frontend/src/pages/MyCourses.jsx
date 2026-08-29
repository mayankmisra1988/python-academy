import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getMyCourses } from "../services/enrollmentService";
import "./MyCourses.css";

import PageSkeleton from "../components/PageSkeleton";

export default function MyCourses() {
  const navigate = useNavigate();

  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  // =====================================================
  // LOAD MY COURSES
  // =====================================================

  useEffect(() => {
    const loadCourses = async () => {
      try {
        const data = await getMyCourses();

        console.log("My Courses:", data);

        setCourses(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error(
          "My Courses loading error:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadCourses();
  }, []);

  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {
    return <PageSkeleton />;
  }

  // =====================================================
  // MY COURSES
  // =====================================================

  return (
    <div className="my-courses page-fade-in">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="my-courses-header">

        <div>
          <span className="my-courses-eyebrow">
            PYTHON ACADEMY
          </span>

          <h1>
            📚 My Courses
          </h1>

          <p>
            Continue learning from where you left off.
          </p>
        </div>

        <div className="course-count">

          <strong>
            {courses.length}
          </strong>

          <span>
            {courses.length === 1
              ? "Course"
              : "Courses"}
          </span>

        </div>

      </header>

      {/* =================================================
          EMPTY STATE
      ================================================= */}

      {courses.length === 0 ? (

        <div className="no-courses-card">

          <div className="no-courses-icon">
            📚
          </div>

          <h2>
            No Courses Yet
          </h2>

          <p>
            You have not enrolled in any course yet.
          </p>

          <button
            className="browse-courses-btn"
            onClick={() => navigate("/courses")}
          >
            Browse Courses →
          </button>

        </div>

      ) : (

        /* =================================================
           COURSE GRID
        ================================================= */

        <div className="course-grid">

          {courses.map((course) => {

            const progress = Math.min(
              100,
              Math.max(
                0,
                Number(course.progress) || 0
              )
            );

            return (

              <article
                className="my-course-card"
                key={course.id}
              >

                {/* =================================================
                    THUMBNAIL
                ================================================= */}

                <div className="my-course-image-wrapper">

                  {course.thumbnail ? (

                    <img
                      src={course.thumbnail}
                      alt={course.course_title}
                    />

                  ) : (

                    <div className="course-image-placeholder">
                      🐍
                    </div>

                  )}

                  {/* STATUS BADGE */}

                  <span
                    className={
                      course.completed
                        ? "course-status-badge completed"
                        : "course-status-badge progress"
                    }
                  >

                    {course.completed
                      ? "✓ Completed"
                      : "▶ In Progress"}

                  </span>

                </div>

                {/* =================================================
                    CARD BODY
                ================================================= */}

                <div className="my-course-card-body">

                  <span className="course-card-label">
                    MY COURSE
                  </span>

                  <h3>
                    {course.course_title}
                  </h3>

                  {/* =================================================
                      STATUS
                  ================================================= */}

                  <div className="course-status-row">

                    <span>
                      Status
                    </span>

                    <strong
                      className={
                        course.completed
                          ? "status-complete"
                          : "status-progress"
                      }
                    >

                      {course.completed
                        ? "Completed"
                        : "In Progress"}

                    </strong>

                  </div>

                  {/* =================================================
                      PROGRESS
                  ================================================= */}

                  <div className="my-course-progress">

                    <div className="my-course-progress-info">

                      <span>
                        Progress
                      </span>

                      <strong>
                        {progress}%
                      </strong>

                    </div>

                    <div
                      className="my-course-progress-bar"
                      aria-label={`Course progress ${progress}%`}
                    >

                      <div
                        className="my-course-progress-fill"
                        style={{
                          width: `${progress}%`,
                        }}
                      />

                    </div>

                  </div>

                  {/* =================================================
                      ACTION
                  ================================================= */}

                  <button
                    className="my-course-btn"
                    onClick={() => {

                      if (!course.course_slug) {

                        console.error(
                          "Course slug missing:",
                          course
                        );

                        return;
                      }

                      navigate(
                        `/courses/${course.course_slug}`
                      );
                    }}
                  >

                    <span>

                      {course.completed
                        ? "🏆 View Course"
                        : "▶ Continue Learning"}

                    </span>

                    <span className="btn-arrow">
                      →
                    </span>

                  </button>

                </div>

              </article>

            );
          })}

        </div>
      )}

    </div>
  );
}