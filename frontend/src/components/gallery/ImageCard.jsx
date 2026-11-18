import { useState } from "react";
import { getImageUrl } from "../../services/imageService";
import { Download, Expand, Heart } from "lucide-react";

export function ImageCard({ image, onClick, onDownload, selectionMode = false, isSelected = false, onToggleSelect, isFavorite = false, onToggleFavorite }) {
  const [imageUrl, setImageUrl] = useState(() => getImageUrl(image.image_id));
  const [imageFailed, setImageFailed] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  const handleImageError = () => {
    if (retryCount >= 1) {
      setImageFailed(true);
      return;
    }
    setRetryCount(1);
    setImageUrl(`${getImageUrl(image.image_id)}?retry=${Date.now()}`);
  };

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
      {imageFailed ? (
        <div className="image-card-fallback" role="img" aria-label={`${image.title || image.file_name} unavailable`}>
          <span>Image unavailable</span>
          <button type="button" onClick={(event) => { event.stopPropagation(); setImageFailed(false); setRetryCount(0); setImageUrl(`${getImageUrl(image.image_id)}?retry=${Date.now()}`); }}>Retry</button>
        </div>
      ) : (
        <img src={imageUrl} alt={image.title || image.file_name} loading="lazy" onError={handleImageError} />
      )}

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
        {onToggleFavorite && (
          <button type="button" className={isFavorite ? "is-favorite" : ""} aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"} title={isFavorite ? "Remove from favorites" : "Add to favorites"} onClick={(event) => { event.stopPropagation(); onToggleFavorite(image); }}>
            <Heart className="h-4 w-4" fill={isFavorite ? "currentColor" : "none"} />
          </button>
        )}
      </div>
    </div>
  );
}
