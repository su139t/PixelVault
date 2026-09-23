import { ImageCard } from "./ImageCard";
import { Image as ImageIcon } from "lucide-react";

export function ImageGrid({ images, onImageClick, onDownload, selectionMode, selectedIds, onToggleSelect }) {
  if (!images || images.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">
          <ImageIcon className="w-7 h-7 text-accent-violet" />
        </div>
        <p className="empty-state-title">No photos yet</p>
        <p className="empty-state-text">Upload your first photo to get started</p>
      </div>
    );
  }

  return (
    <div className="image-grid">
      {images.map((image, i) => (
        <div
          key={image.image_id}
          style={{ animationDelay: `${i * 0.04}s` }}
          className="animate-[fade-in_0.4s_ease_both]"
        >
          <ImageCard
            image={image}
            onClick={onImageClick}
            onDownload={onDownload}
            selectionMode={selectionMode}
            isSelected={selectedIds?.has(image.image_id)}
            onToggleSelect={onToggleSelect}
          />
        </div>
      ))}
    </div>
  );
}
