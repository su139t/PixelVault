import { useState, useEffect, useRef, useCallback } from "react";
import { addFavorite, addTagToImage, createTag, deleteImage, downloadImage, getFavorites, getImageTags, getImageUrl, getImages, removeFavorite, removeTagFromImage, updateImage } from "../services/imageService";
import { ImageGrid } from "../components/gallery/ImageGrid";
import { UploadButton } from "../components/gallery/UploadButton";
import { useAuth } from "../context/AuthContext";
import { ArrowLeft, ArrowRight, ArrowUpRight, Camera, CheckSquare, Download, Heart, Save, Sparkles, Tag, Trash2, X } from "lucide-react";

const formatFileSize = (bytes) => {
  if (!bytes) return "Unknown";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const formatUploadDate = (date) => {
  if (!date) return "Unknown";
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(date));
};

const IMAGE_PAGE_SIZE = 24;

export default function PhotosPage() {
  const { user } = useAuth();
  const [images, setImages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [description, setDescription] = useState("");
  const [tagName, setTagName] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isAddingTag, setIsAddingTag] = useState(false);
  const [selectionMode, setSelectionMode] = useState(false);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [isDeleting, setIsDeleting] = useState(false);
  const [favoriteIds, setFavoriteIds] = useState(new Set());
  const [isFavoriteUpdating, setIsFavoriteUpdating] = useState(false);
  const touchStartX = useRef(null);
  const loadMoreRef = useRef(null);
  const [hasMoreImages, setHasMoreImages] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [nextOffset, setNextOffset] = useState(0);

  const loadImagePage = useCallback(async (offset, reset = false) => {
    if (!user?.user_id) return;
    try {
      if (reset) setIsLoading(true);
      else setIsLoadingMore(true);
      const data = await getImages(user.user_id, { limit: IMAGE_PAGE_SIZE, offset });
      const pageImages = data.images || [];
      setImages((currentImages) => reset ? pageImages : [...currentImages, ...pageImages]);
      setHasMoreImages(Boolean(data.has_more));
      setNextOffset(offset + pageImages.length);
    } catch (error) {
      console.error("Failed to fetch images:", error);
    } finally {
      if (reset) setIsLoading(false);
      else setIsLoadingMore(false);
    }
  }, [user]);

  const fetchImages = useCallback(() => loadImagePage(0, true), [loadImagePage]);

  useEffect(() => {
    if (!user?.user_id) return;
    // The loader synchronizes the page with the remote image collection.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadImagePage(0, true);
  }, [user?.user_id, loadImagePage]);

  useEffect(() => {
    const loadMoreTarget = loadMoreRef.current;
    if (!loadMoreTarget) return undefined;
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasMoreImages && !isLoading && !isLoadingMore) {
        loadImagePage(nextOffset);
      }
    }, { rootMargin: "500px" });
    observer.observe(loadMoreTarget);
    return () => observer.disconnect();
  }, [hasMoreImages, isLoading, isLoadingMore, loadImagePage, nextOffset]);

  useEffect(() => {
    if (!user?.user_id) return;
    getFavorites(user.user_id)
      .then((data) => setFavoriteIds(new Set((data.favorites || []).map((image) => image.image_id))))
      .catch((error) => console.error("Failed to fetch favorites:", error));
  }, [user?.user_id]);

  const selectImage = useCallback((image) => {
    setSelectedImage(image);
    setDescription(image.description || "");
    setTagName("");
    setSelectedTags([]);
    getImageTags(image.image_id)
      .then((data) => setSelectedTags(data.data?.tags || []))
      .catch((error) => console.error("Failed to fetch image tags:", error));
  }, []);

  const handleImageClick = (image) => selectImage(image);

  const closeViewer = () => setSelectedImage(null);

  const handleToggleFavorite = async (image) => {
    const isFavorite = favoriteIds.has(image.image_id);
    try {
      if (isFavorite) await removeFavorite(user.user_id, image.image_id);
      else await addFavorite(user.user_id, image.image_id);
      setFavoriteIds((currentIds) => {
        const nextIds = new Set(currentIds);
        if (isFavorite) nextIds.delete(image.image_id);
        else nextIds.add(image.image_id);
        return nextIds;
      });
    } catch (error) {
      console.error("Failed to update favorite:", error);
    }
  };

  const handleToggleViewerFavorite = async () => {
    if (!selectedImage || isFavoriteUpdating) return;
    setIsFavoriteUpdating(true);
    await handleToggleFavorite(selectedImage);
    setIsFavoriteUpdating(false);
  };

  const navigateViewer = useCallback((direction) => {
    if (!selectedImage || !images.length) return;
    const currentIndex = images.findIndex((image) => image.image_id === selectedImage.image_id);
    const nextIndex = (currentIndex + direction + images.length) % images.length;
    selectImage(images[nextIndex]);
  }, [images, selectImage, selectedImage]);

  useEffect(() => {
    if (!selectedImage) return undefined;
    const handleKeyDown = (event) => {
      if (event.key === "Escape") closeViewer();
      if (event.key === "ArrowLeft") navigateViewer(-1);
      if (event.key === "ArrowRight") navigateViewer(1);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [navigateViewer, selectedImage]);

  const handlePreviewTouchStart = (event) => {
    touchStartX.current = event.touches[0].clientX;
  };

  const handlePreviewTouchEnd = (event) => {
    if (touchStartX.current === null) return;
    const distance = event.changedTouches[0].clientX - touchStartX.current;
    touchStartX.current = null;
    if (Math.abs(distance) < 45) return;
    navigateViewer(distance < 0 ? 1 : -1);
  };

  const toggleSelection = (image) => {
    setSelectedIds((currentIds) => {
      const nextIds = new Set(currentIds);
      if (nextIds.has(image.image_id)) nextIds.delete(image.image_id);
      else nextIds.add(image.image_id);
      return nextIds;
    });
  };

  const toggleSelectionMode = () => {
    setSelectionMode((currentMode) => !currentMode);
    setSelectedIds(new Set());
  };

  const handleDeleteSelected = async () => {
    if (!selectedIds.size || !window.confirm(`Delete ${selectedIds.size} selected photo${selectedIds.size === 1 ? "" : "s"}?`)) return;
    setIsDeleting(true);
    try {
      await Promise.all([...selectedIds].map((imageId) => deleteImage(imageId)));
      setImages((currentImages) => currentImages.filter((image) => !selectedIds.has(image.image_id)));
      setSelectedIds(new Set());
      setSelectionMode(false);
    } catch (error) {
      console.error("Failed to delete selected photos:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDeleteImage = async () => {
    if (!selectedImage || !window.confirm("Delete this photo permanently?")) return;
    setIsDeleting(true);
    try {
      await deleteImage(selectedImage.image_id);
      setImages((currentImages) => currentImages.filter((image) => image.image_id !== selectedImage.image_id));
      closeViewer();
    } catch (error) {
      console.error("Failed to delete photo:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleSaveDescription = async () => {
    setIsSaving(true);
    try {
      const data = await updateImage(selectedImage.image_id, { description });
      const updatedImage = data.data?.image || { ...selectedImage, description };
      setSelectedImage(updatedImage);
      setImages((currentImages) => currentImages.map((image) => image.image_id === updatedImage.image_id ? updatedImage : image));
    } catch (error) {
      console.error("Failed to save description:", error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleAddTag = async (event) => {
    event.preventDefault();
    const trimmedName = tagName.trim();
    if (!trimmedName || isAddingTag) return;

    setIsAddingTag(true);
    try {
      const tagData = await createTag(user.user_id, trimmedName);
      const tag = tagData.data?.tag;
      if (tag) {
        await addTagToImage(selectedImage.image_id, tag.tag_id);
        setSelectedTags((currentTags) => [...currentTags, tag]);
      }
      setTagName("");
    } catch (error) {
      console.error("Failed to add tag:", error);
    } finally {
      setIsAddingTag(false);
    }
  };

  const handleRemoveTag = async (tag) => {
    try {
      await removeTagFromImage(selectedImage.image_id, tag.tag_id);
      setSelectedTags((currentTags) => currentTags.filter((currentTag) => currentTag.tag_id !== tag.tag_id));
    } catch (error) {
      console.error("Failed to remove tag:", error);
    }
  };

  const handleDownload = async (image) => {
    const blob = await downloadImage(image.image_id);
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = image.file_name || `pixelvault-${image.image_id}.jpg`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="photos-page">
      <section className="welcome-banner">
        <div className="welcome-copy">
          <p className="eyebrow"><Sparkles className="h-3.5 w-3.5" /> Your private visual archive</p>
          <h1>Good to see you, {user?.name?.split(" ")[0] || "there"}.</h1>
          <p className="welcome-description">Keep the moments that matter close, beautifully organized and ready to rediscover.</p>
          <div className="welcome-actions">
            <UploadButton onUploadSuccess={fetchImages} />
            <span className="storage-note"><Camera className="h-4 w-4" /> Stored securely in your vault</span>
          </div>
        </div>
        <div className="welcome-mark" aria-hidden="true">
          <div className="welcome-frame frame-back" />
          <div className="welcome-frame frame-front"><Camera className="h-10 w-10" /><span>make room<br />for wonder</span></div>
          <ArrowUpRight className="welcome-arrow" />
        </div>
      </section>

      <div className="page-header photos-toolbar">
        <div>
          <p className="section-kicker">Your collection</p>
          <h2 className="page-title page-title-gradient">All photos <span>{images.length}</span></h2>
        </div>
        <div className="photos-toolbar-actions">
          {selectionMode && selectedIds.size > 0 && <button className="batch-delete-button" type="button" onClick={handleDeleteSelected} disabled={isDeleting}><Trash2 className="h-4 w-4" /> {isDeleting ? "Deleting..." : `Delete ${selectedIds.size}`}</button>}
          <button className={`select-photos-button ${selectionMode ? "active" : ""}`} type="button" onClick={toggleSelectionMode}><CheckSquare className="h-4 w-4" /> {selectionMode ? "Cancel" : "Select"}</button>
          <button className="view-toggle" type="button" aria-label="Current grid view">
            <span className="view-toggle-dot active" /><span className="view-toggle-dot" /><span className="view-toggle-dot" />
          </button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <div className="spinner" />
        </div>
      ) : (
        <ImageGrid images={images} onImageClick={handleImageClick} onDownload={handleDownload} selectionMode={selectionMode} selectedIds={selectedIds} onToggleSelect={toggleSelection} favoriteIds={favoriteIds} onToggleFavorite={handleToggleFavorite} />
      )}
      {!isLoading && images.length > 0 && (
        <div ref={loadMoreRef} className="load-more-status" aria-live="polite">
          {isLoadingMore && <><div className="spinner small-spinner" /> Loading more photos...</>}
          {!isLoadingMore && !hasMoreImages && <span>All photos loaded</span>}
        </div>
      )}
      {selectedImage && (
        <div className="image-viewer" role="dialog" aria-modal="true" onClick={closeViewer}>
          <div className="image-viewer-panel" onClick={(event) => event.stopPropagation()}>
            <button className="image-viewer-close" type="button" onClick={closeViewer} aria-label="Close image"><X className="h-4 w-4" /></button>
            <div className="image-viewer-content">
              <div className="image-viewer-preview" onTouchStart={handlePreviewTouchStart} onTouchEnd={handlePreviewTouchEnd}>
                <button className="image-viewer-nav image-viewer-nav-previous" type="button" onClick={() => navigateViewer(-1)} aria-label="Previous photo"><ArrowLeft className="h-5 w-5" /></button>
                <img src={getImageUrl(selectedImage.image_id)} alt={selectedImage.title || selectedImage.file_name} />
                <button className="image-viewer-nav image-viewer-nav-next" type="button" onClick={() => navigateViewer(1)} aria-label="Next photo"><ArrowRight className="h-5 w-5" /></button>
              </div>
              <aside className="image-viewer-details">
                <div className="image-viewer-heading">
                  <p className="section-kicker">Photo details</p>
                  <h2>{selectedImage.title || selectedImage.file_name}</h2>
                </div>
                <div className="image-meta-grid">
                  <div><span>Dimensions</span><strong>{selectedImage.width || "?"} × {selectedImage.height || "?"} px</strong></div>
                  <div><span>File size</span><strong>{formatFileSize(selectedImage.file_size)}</strong></div>
                  <div><span>Uploaded</span><strong>{formatUploadDate(selectedImage.upload_date)}</strong></div>
                  <div><span>File type</span><strong>{selectedImage.mime_type || "Image"}</strong></div>
                </div>
                <button className={`favorite-button ${favoriteIds.has(selectedImage.image_id) ? "active" : ""}`} type="button" onClick={handleToggleViewerFavorite} disabled={isFavoriteUpdating}>
                  <Heart className="h-4 w-4" fill={favoriteIds.has(selectedImage.image_id) ? "currentColor" : "none"} /> {favoriteIds.has(selectedImage.image_id) ? "Remove from favorites" : "Add to favorites"}
                </button>
                <label className="detail-label" htmlFor="image-description">Description</label>
                <textarea id="image-description" value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Write something about this moment..." rows="4" />
                <button className="btn-primary detail-save" type="button" onClick={handleSaveDescription} disabled={isSaving}>
                  <Save className="h-4 w-4" /> {isSaving ? "Saving..." : "Save description"}
                </button>
                <div className="detail-tags">
                  <label className="detail-label"><Tag className="h-3.5 w-3.5" /> Tags</label>
                  <div className="tag-list">
                    {selectedTags.map((tag) => <span className="tag-chip" key={tag.tag_id}>{tag.tag_name}<button type="button" onClick={() => handleRemoveTag(tag)} aria-label={`Remove ${tag.tag_name}`}><X className="h-3 w-3" /></button></span>)}
                    {!selectedTags.length && <span className="detail-empty">No tags yet</span>}
                  </div>
                  <form className="tag-form" onSubmit={handleAddTag}>
                    <input value={tagName} onChange={(event) => setTagName(event.target.value)} placeholder="Add a tag" aria-label="New tag" />
                    <button type="submit" disabled={!tagName.trim() || isAddingTag}>Add</button>
                  </form>
                </div>
                <div className="detail-actions">
                  <button className="detail-download" type="button" onClick={() => handleDownload(selectedImage)}><Download className="h-4 w-4" /> Download original</button>
                  <button className="detail-delete" type="button" onClick={handleDeleteImage} disabled={isDeleting}><Trash2 className="h-4 w-4" /> {isDeleting ? "Deleting..." : "Delete photo"}</button>
                </div>
              </aside>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
