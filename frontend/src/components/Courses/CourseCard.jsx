// import { Link } from "react-router-dom";
// import "./Courses.css";

// export default function CourseCard({ course }) {
//   return (
//     <div className="home-course-card">

//       <div className="course-image">
//         <img
//           src={course.thumbnail}
//           alt={course.title}
//         />
//       </div>

//       <div className="course-content">

//         <span className="course-badge">
//           {course.level.toUpperCase()}
//         </span>

//         <h3 title={course.title}>
//           {course.title}
//         </h3>

//         <p title={course.short_description}>
//           {course.short_description}
//         </p>

//         <div className="course-meta">
//           <span>📂 {course.category?.name}</span>
//         </div>

//         <div className="course-footer">

//           <h4>
//             {course.is_free ? "FREE" : `₹${course.price}`}
//           </h4>

//           <Link to={`/courses/${course.slug}`}>
//             <button>
//               View Course
//             </button>
//           </Link>

//         </div>

//       </div>

//     </div>
//   );
// }










import { Link } from "react-router-dom";
import "./Courses.css";

export default function CourseCard({ course }) {
  // Agar course passed nai hai toh crash hone se bachayein
  if (!course) return null;

  return (
    <div className="home-course-card">

      <div className="course-image">
        <img
          src={course.thumbnail || "https://via.placeholder.com/300x200?text=No+Image"}
          alt={course.title || "Course Image"}
        />
      </div>

      <div className="course-content">

        <span className="course-badge">
          {/* ✅ Safe Check: level string hai ya nahi */}
          {course.level ? String(course.level).toUpperCase() : "BEGINNER"}
        </span>

        <h3 title={course.title || ""}>
          {course.title || "Untitled Course"}
        </h3>

        <p title={course.short_description || ""}>
          {course.short_description || "No description available"}
        </p>

        <div className="course-meta">
          <span>📂 {course.category?.name || "General"}</span>
        </div>

        <div className="course-footer">

          <h4>
            {course.is_free ? "FREE" : `₹${course.price || 0}`}
          </h4>

          <Link to={`/courses/${course.slug || course.id}`}>
            <button>
              View Course
            </button>
          </Link>

        </div>

      </div>

    </div>
  );
}