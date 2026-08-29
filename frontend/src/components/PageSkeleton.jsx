import "./PageSkeleton.css";

function SkeletonCard({ count = 4 }) {
  return (
    <div className="skeleton-grid">
      {Array.from({ length: count }).map((_, index) => (
        <div className="skeleton-card" key={index}>
          <div className="skeleton-image"></div>
          <div className="skeleton-content">
            <div className="skeleton-line title"></div>
            <div className="skeleton-line"></div>
            <div className="skeleton-line short"></div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SkeletonCard;