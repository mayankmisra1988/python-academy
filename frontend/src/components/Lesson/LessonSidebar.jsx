import { Link } from "react-router-dom";

import "./Lesson.css";


export default function LessonSidebar({
  curriculum = [],
  currentLessonId,
  courseSlug,
}) {

  console.log("CURRICULUM:", curriculum);
  console.log("CURRENT LESSON ID:", currentLessonId);


  return (

    <aside className="lesson-sidebar">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="sidebar-header">

        <h3>
          Course Curriculum
        </h3>

      </div>


      {/* =====================================================
          CONTENT
      ===================================================== */}

      <div className="sidebar-content">

        {curriculum.length === 0 ? (

          <p className="empty-curriculum">
            No lessons available.
          </p>

        ) : (

          curriculum
            .filter(Boolean)
            .map((section) => {

              const lessons =
                Array.isArray(section.lessons)
                  ? section.lessons.filter(
                    (lesson) =>
                      lesson &&
                      lesson.id
                  )
                  : [];


              return (

                <div
                  className="sidebar-section"
                  key={section.id}
                >


                  {/* =================================================
                      SECTION TITLE
                  ================================================= */}

                  <div className="section-title">

                    <span className="section-number">
                      {section.order}.
                    </span>

                    <strong>
                      {section.title}
                    </strong>

                  </div>


                  {/* =================================================
                      LESSONS
                  ================================================= */}

                  <div className="sidebar-lessons">

                    {lessons.length === 0 ? (

                      <p className="empty-lessons">
                        No lessons
                      </p>

                    ) : (

                      lessons.map((lesson) => {

                        const isActive =
                          Number(lesson.id) ===
                          Number(currentLessonId);


                        const isCompleted =
                          lesson.completed === true;


                        /*
                         * Completed lesson gets
                         * priority over active icon.
                         */

                        let statusIcon = "○";

                        if (isCompleted) {

                          statusIcon = "✓";

                        } else if (isActive) {

                          statusIcon = "▶";

                        }


                        return (

                          <Link

                            key={lesson.id}

                            to={
                              courseSlug
                                ? `/courses/${courseSlug}/lesson/${lesson.id}`
                                : "#"
                            }

                            className={[
                              "sidebar-lesson",

                              isActive
                                ? "active"
                                : "",

                              isCompleted
                                ? "completed"
                                : "",
                            ]
                              .filter(Boolean)
                              .join(" ")}

                            onClick={(event) => {

                              if (!courseSlug) {

                                event.preventDefault();

                                console.error(
                                  "Course slug is missing."
                                );

                              }

                            }}

                          >


                            {/* =================================================
                                STATUS ICON
                            ================================================= */}
                            <span
                              className={`lesson-status ${isCompleted
                                ? "completed-status"
                                : isActive
                                  ? "active-status"
                                  : ""
                                }`}
                            >
                              {statusIcon}
                            </span>
                            {/* =================================================
                                LESSON TITLE
                            ================================================= */}
                            <span className="sidebar-lesson-title">
                              {lesson.title}
                            </span>
                            {/* =================================================
                                CURRENT LABEL
                            ================================================= */}
                            {isActive &&
                              !isCompleted && (
                                <span className="current-label">
                                  Current
                                </span>
                              )}
                          </Link>
                        );
                      })
                    )}
                  </div>
                </div>
              );
            })
        )}
      </div>
    </aside>
  );
}