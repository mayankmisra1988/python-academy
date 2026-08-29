import { useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Curriculum.css";


export default function Curriculum({
  curriculum = [],
  slug,
  course,
}) {

  const navigate = useNavigate();


  const [openSections, setOpenSections] =
    useState(() => {

      const initialState = {};

      curriculum.forEach((section, index) => {
        initialState[section.id] = index === 0;
      });

      return initialState;

    });


  const toggleSection = (sectionId) => {

    setOpenSections((previous) => ({
      ...previous,
      [sectionId]: !previous[sectionId],
    }));

  };


  const handleLessonClick = (lesson) => {

    /*
      Preview lessons can be opened
      even if student is not enrolled.
    */

    if (
      !course?.enrolled &&
      !lesson.is_preview
    ) {
      return;
    }


    navigate(
      `/courses/${slug}/lesson/${lesson.id}`
    );

  };


  if (!curriculum.length) {

    return (

      <section className="curriculum-section">

        <div className="curriculum-empty">

          <div className="empty-icon">
            📚
          </div>

          <h3>
            Course Curriculum Coming Soon
          </h3>

          <p>
            Lessons will be added to this course soon.
          </p>

        </div>

      </section>

    );

  }


  const totalLessons = curriculum.reduce(
    (total, section) =>
      total + (section.lessons?.length || 0),
    0
  );


  return (

    <section className="curriculum-section">

      {/* =====================================
          HEADER
      ===================================== */}

      <div className="curriculum-header">

        <div>

          <span className="curriculum-label">
            COURSE CONTENT
          </span>

          <h2>
            Course Curriculum
          </h2>

          <p>
            Learn step by step and build your Python skills.
          </p>

        </div>


        <div className="curriculum-count">

          {curriculum.length}{" "}
          {curriculum.length === 1
            ? "Section"
            : "Sections"}

        </div>

      </div>


      {/* =====================================
          SECTIONS
      ===================================== */}

      <div className="curriculum-list">

        {curriculum.map(
          (section, sectionIndex) => {

            const isOpen =
              openSections[section.id];


            return (

              <div
                className="curriculum-section-card"
                key={section.id}
              >

                {/* =================================
                    SECTION HEADER
                ================================= */}

                <button
                  className="section-header"
                  onClick={() =>
                    toggleSection(section.id)
                  }
                  type="button"
                >

                  <div className="section-left">

                    <div className="section-number">
                      {sectionIndex + 1}
                    </div>


                    <div className="section-info">

                      <h3>
                        {section.title}
                      </h3>

                      {section.description && (

                        <p>
                          {section.description}
                        </p>

                      )}

                    </div>

                  </div>


                  <div className="section-right">

                    <span className="section-lessons">

                      {section.lessons?.length || 0}{" "}

                      {section.lessons?.length === 1
                        ? "Lesson"
                        : "Lessons"}

                    </span>


                    <span
                      className={`section-arrow ${
                        isOpen ? "open" : ""
                      }`}
                    >
                      ▼
                    </span>

                  </div>

                </button>


                {/* =================================
                    LESSONS
                ================================= */}

                {isOpen && (

                  <div className="lesson-list">

                    {section.lessons?.length ? (

                      section.lessons.map(
                        (lesson, lessonIndex) => {

                          const locked =
                            !course?.enrolled &&
                            !lesson.is_preview;


                          const completed =
                            lesson.completed === true;


                          return (

                            <div
                              className={`lesson-item ${
                                completed
                                  ? "completed"
                                  : ""
                              } ${
                                locked
                                  ? "locked"
                                  : ""
                              }`}
                              key={lesson.id}
                            >

                              {/* Lesson Icon */}

                              <div className="lesson-icon">

                                {completed
                                  ? "✓"
                                  : locked
                                  ? "🔒"
                                  : "📚"}

                              </div>


                              {/* Lesson Information */}

                              <div className="lesson-info">

                                <h4>

                                  {lessonIndex + 1}.{" "}

                                  {lesson.title}

                                </h4>


                                {lesson.description && (

                                  <p>
                                    {lesson.description}
                                  </p>

                                )}


                                <div className="lesson-meta">

                                  {lesson.duration > 0 && (

                                    <span>
                                      ⏱ {lesson.duration} min
                                    </span>

                                  )}


                                  {lesson.is_preview && (

                                    <span className="preview-badge">
                                      👁 Preview
                                    </span>

                                  )}


                                  {completed && (

                                    <span className="completed-badge">
                                      ✓ Completed
                                    </span>

                                  )}

                                </div>

                              </div>


                              {/* Lesson Action */}

                              <button
                                type="button"
                                className={`lesson-action ${
                                  locked
                                    ? "locked-button"
                                    : completed
                                    ? "completed-button"
                                    : ""
                                }`}
                                disabled={locked}
                                onClick={() =>
                                  handleLessonClick(
                                    lesson
                                  )
                                }
                              >

                                {locked
                                  ? "🔒 Locked"
                                  : completed
                                  ? "Review →"
                                  : "Start →"}

                              </button>

                            </div>

                          );

                        }

                      )

                    ) : (

                      <div className="no-lessons">

                        No lessons available
                        in this section.

                      </div>

                    )}

                  </div>

                )}

              </div>

            );

          }
        )}

      </div>


      {/* =====================================
          SUMMARY
      ===================================== */}

      <div className="curriculum-summary">

        <span>
          📚 {totalLessons}{" "}
          {totalLessons === 1
            ? "Lesson"
            : "Lessons"}
        </span>

        <span>
          📂 {curriculum.length}{" "}
          {curriculum.length === 1
            ? "Section"
            : "Sections"}
        </span>

      </div>

    </section>

  );

}