import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getDashboard } from "../services/dashboardService";

import PageSkeleton from "../components/PageSkeleton";

import "./Dashboard.css";


function Dashboard() {

  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);


  // =====================================================
  // LOAD DASHBOARD
  // =====================================================

  useEffect(() => {

    const loadDashboard = async () => {

      try {

        const data = await getDashboard();

        setDashboard(data);

      } catch (error) {

        console.error(
          "Dashboard Error:",
          error
        );

      } finally {

        setLoading(false);

      }

    };


    loadDashboard();

  }, []);


  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return <PageSkeleton />;

  }


  // =====================================================
  // ERROR
  // =====================================================

  if (!dashboard) {

    return (

      <div className="dashboard-empty">

        <div className="dashboard-empty-icon">
          ⚠️
        </div>

        <h2>
          Unable to load dashboard
        </h2>

        <p>
          Please refresh the page and try again.
        </p>

      </div>

    );

  }


  const continueLearning =
    dashboard.continue_learning || [];


  // =====================================================
  // DASHBOARD
  // =====================================================

  return (

    <div className="content page-fade-in">


      {/* =================================================
          HEADER
      ================================================= */}

      <header className="dashboard-header">

        <div>

          <span className="dashboard-eyebrow">
            PYTHON ACADEMY
          </span>

          <h1>
            Welcome,{" "}
            {dashboard.user?.first_name ||
              dashboard.user?.username ||
              "Student"} 👋
          </h1>

          <p>
            Keep learning and continue building
            your Python skills.
          </p>

        </div>

      </header>


      {/* =================================================
          STATISTICS
      ================================================= */}

      <section className="stats">


        {/* ENROLLED */}

        <div className="dashboard-stat-card">

          <div className="stat-icon">
            📚
          </div>

          <div>

            <h2>
              {dashboard.total_courses ?? 0}
            </h2>

            <p>
              Enrolled Courses
            </p>

          </div>

        </div>


        {/* LESSONS */}

        <div className="dashboard-stat-card">

          <div className="stat-icon">
            ✅
          </div>

          <div>

            <h2>
              {dashboard.completed_lessons ?? 0}
            </h2>

            <p>
              Completed Lessons
            </p>

          </div>

        </div>


        {/* COURSES */}

        <div className="dashboard-stat-card">

          <div className="stat-icon">
            🎓
          </div>

          <div>

            <h2>
              {dashboard.completed_courses ?? 0}
            </h2>

            <p>
              Completed Courses
            </p>

          </div>

        </div>


        {/* PROGRESS */}

        <div className="dashboard-stat-card">

          <div className="stat-icon">
            📈
          </div>

          <div>

            <h2>
              {dashboard.overall_progress ?? 0}%
            </h2>

            <p>
              Overall Progress
            </p>

          </div>

        </div>

      </section>


      {/* =================================================
          CONTINUE LEARNING
      ================================================= */}

      <section className="dashboard-section">


        <div className="section-heading">

          <div>

            <h2 className="section-title">
              Continue Learning
            </h2>

            <p>
              Pick up where you left off.
            </p>

          </div>

          <Link
            to="/my-courses"
            className="view-all-link"
          >
            View My Courses →
          </Link>

        </div>


        {continueLearning.length === 0 ? (

          <div className="dashboard-empty-card">

            <div className="empty-icon">
              📚
            </div>

            <h3>
              No courses to continue
            </h3>

            <p>
              Enroll in a course and start
              learning today.
            </p>

            <Link
              to="/courses"
              className="browse-courses-btn"
            >
              Browse Courses
            </Link>

          </div>

        ) : (

          <div className="dashboard-courses-grid">

            {continueLearning.map(
              (course) => {

                const progress =
                  Math.min(
                    100,
                    Math.max(
                      0,
                      Number(course.progress) || 0
                    )
                  );


                return (

                  <Link
                    key={course.course_id}
                    to={`/courses/${course.course_slug}/lesson/${course.lesson_id}`}
                    className="dashboard-course-card"
                  >


                    {/* IMAGE */}

                    <div className="course-image-wrapper">

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

                    </div>


                    {/* CONTENT */}

                    <div className="course-card-content">

                      {course.course_completed ? (
                        <span className="course-label completed-label">
                          COURSE COMPLETED
                        </span>
                      ) : (
                        <span className="course-label">
                          CONTINUE LEARNING
                        </span>
                      )}

                      <h3>
                        {course.course_title}
                      </h3>

                      <div className="course-progress-info">

                        <span>
                          {course.course_completed
                            ? "Completed"
                            : "Progress"}
                        </span>

                        <strong>
                          {progress}%
                        </strong>

                      </div>

                      <div
                        className="progress-bar"
                        aria-label={`Course progress ${progress}%`}
                      >
                        <div
                          className="progress-fill"
                          style={{
                            width: `${progress}%`,
                          }}
                        />
                      </div>

                      {course.course_completed ? (

                        <div className="continue-btn completed-btn">
                          🏆 Course Completed
                        </div>

                      ) : (

                        <div className="continue-btn">
                          Continue Learning
                          <span>→</span>
                        </div>

                      )}

                    </div>

                  </Link>

                );

              }
            )}

          </div>

        )}

      </section>


      {/* =================================================
          QUICK ACTIONS
      ================================================= */}

      <section className="quick-actions-section">

        <h2 className="section-title">
          Quick Actions
        </h2>

        <div className="quick-actions">


          <Link
            to="/courses"
            className="quick-action-card"
          >

            <span className="quick-action-icon">
              🔎
            </span>

            <div>

              <h3>
                Explore Courses
              </h3>

              <p>
                Find your next Python course.
              </p>

            </div>

            <span className="quick-action-arrow">
              →
            </span>

          </Link>


          <Link
            to="/certificates"
            className="quick-action-card"
          >

            <span className="quick-action-icon">
              🏆
            </span>

            <div>

              <h3>
                My Certificates
              </h3>

              <p>
                View your earned certificates.
              </p>

            </div>

            <span className="quick-action-arrow">
              →
            </span>

          </Link>


          <Link
            to="/profile"
            className="quick-action-card"
          >

            <span className="quick-action-icon">
              👤
            </span>

            <div>

              <h3>
                My Profile
              </h3>

              <p>
                Manage your profile information.
              </p>

            </div>

            <span className="quick-action-arrow">
              →
            </span>

          </Link>

        </div>

      </section>


    </div>

  );

}


export default Dashboard;