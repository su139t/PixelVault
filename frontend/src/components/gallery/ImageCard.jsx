import { getImageUrl } from "../../services/imageService";
import { Download, Expand } from "lucide-react";

export function ImageCard({ image, onClick, onDownload, selectionMode = false, isSelected = false, onToggleSelect }) {
  const handleCardClick = () => {
    if (selectionMode) {
      onToggleSelect(image);
      return;
    }
    onClick(image);
  };

  return (
    <div
      className={`image-card ${isSelected ? "is-selected" : ""}`}
      onClick={handleCardClick}
    >
      <img
        src={getImageUrl(image.image_id)}
        alt={image.title || image.file_name}
        loading="lazy"
      />

      {/* Hover overlay */}
      <div className="image-card-overlay" />

      {selectionMode && (
        <button className={`image-card-select ${isSelected ? "selected" : ""}`} type="button" onClick={(event) => { event.stopPropagation(); onToggleSelect(image); }} aria-label={isSelected ? "Deselect image" : "Select image"}>
          {isSelected && <span>✓</span>}
        </button>
      )}

      {/* Info on hover */}
      <div className="image-card-info">
        <p className="text-white font-medium truncate text-sm">
          {image.title || image.file_name}
        </p>
        {image.ai_description && (
          <p className="text-white/60 text-xs line-clamp-1 mt-0.5">
            {image.ai_description}
          </p>
        )}
      </div>
      <div className="image-card-actions">
        <button type="button" aria-label="Open image" title="Open image" onClick={(event) => { event.stopPropagation(); onClick(image); }}>
          <Expand className="h-4 w-4" />
        </button>
        <button type="button" aria-label="Download image" title="Download image" onClick={(event) => { event.stopPropagation(); onDownload(image); }}>
          <Download className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
