// import "./Features.css";

// export default function Features() {
//   const features = [
//     {
//       icon: "🤖",
//       title: "AI Tutor",
//       description:
//         "Get instant answers to your Python questions with our AI-powered tutor.",
//     },
//     {
//       icon: "💻",
//       title: "AI Code Review",
//       description:
//         "Get AI feedback on your code and improve your coding skills faster.",
//     },
//     {
//       icon: "📝",
//       title: "AI Quiz Generator",
//       description:
//         "Generate quizzes on any topic and test your knowledge instantly.",
//     },
//     {
//       icon: "📁",
//       title: "Hands-on Projects",
//       description:
//         "Build real-world projects and create an impressive portfolio.",
//     },
//   ];

//   return (
//     <section className="features-section">
//       <div className="section-header">
//         <h2>Why Learn with Python Academy?</h2>
//         <p>
//           We combine powerful learning tools with AI to give you the best
//           learning experience.
//         </p>
//       </div>

//       <div className="features-grid">
//         {features.map((feature, index) => (
//           <div className="feature-card" key={index}>
//             <div className="feature-icon">{feature.icon}</div>

//             <h3>{feature.title}</h3>

//             <p>{feature.description}</p>
//           </div>
//         ))}
//       </div>
//     </section>
//   );
// }





import "./Features.css";

export default function Features() {
  const features = [
    {
      icon: "🤖",
      title: "AI Tutor",
      description:
        "Get instant answers to your Python questions with our AI-powered tutor.",
    },
    {
      icon: "💻",
      title: "AI Code Review",
      description:
        "Get AI feedback on your code and improve your coding skills faster.",
    },
    {
      icon: "📝",
      title: "AI Quiz Generator",
      description:
        "Generate quizzes on any topic and test your knowledge instantly.",
    },
    {
      icon: "📁",
      title: "Hands-on Projects",
      description:
        "Build real-world projects and create an impressive portfolio.",
    },
  ];

  return (
    <section className="features-section">
      <div className="section-header">
        <h2>Why Learn with Python Academy?</h2>
        <p>
          We combine powerful learning tools with AI to give you the best
          learning experience.
        </p>
      </div>

      <div className="features-grid">
        {(Array.isArray(features) ? features : []).map((feature, index) => (
          <div className="feature-card" key={index}>
            <div className="feature-icon">{feature.icon}</div>

            <h3>{feature.title}</h3>

            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}