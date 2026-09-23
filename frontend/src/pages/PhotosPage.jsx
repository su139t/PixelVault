import { useState, useEffect } from "react";
import { addTagToImage, createTag, deleteImage, downloadImage, getImageTags, getImageUrl, getImages, removeTagFromImage, updateImage } from "../services/imageService";
import { ImageGrid } from "../components/gallery/ImageGrid";
import { UploadButton } from "../components/gallery/UploadButton";
import { useAuth } from "../context/AuthContext";
import { ArrowUpRight, Camera, CheckSquare, Download, Save, Sparkles, Tag, Trash2, X } from "lucide-react";

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

  const fetchImages = async () => {
    try {
      setIsLoading(true);
      const data = await getImages(user?.user_id);
      setImages(data.images || []);
    } catch (error) {
      console.error("Failed to fetch images:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!user?.user_id) return;
    let isActive = true;

    const loadImages = async () => {
      try {
        setIsLoading(true);
        const data = await getImages(user.user_id);
        if (isActive) setImages(data.images || []);
      } catch (error) {
        console.error("Failed to fetch images:", error);
      } finally {
        if (isActive) setIsLoading(false);
      }
    };

    loadImages();
    return () => { isActive = false; };
  }, [user?.user_id]);

  const handleImageClick = (image) => {
    setSelectedImage(image);
    setDescription(image.description || "");
    setSelectedTags([]);
    getImageTags(image.image_id)
      .then((data) => setSelectedTags(data.data?.tags || []))
      .catch((error) => console.error("Failed to fetch image tags:", error));
  };

  const closeViewer = () => setSelectedImage(null);

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
        <ImageGrid images={images} onImageClick={handleImageClick} onDownload={handleDownload} selectionMode={selectionMode} selectedIds={selectedIds} onToggleSelect={toggleSelection} />
      )}
      {selectedImage && (
        <div className="image-viewer" role="dialog" aria-modal="true" onClick={closeViewer}>
          <div className="image-viewer-panel" onClick={(event) => event.stopPropagation()}>
            <button className="image-viewer-close" type="button" onClick={closeViewer} aria-label="Close image"><X className="h-4 w-4" /></button>
            <div className="image-viewer-content">
              <div className="image-viewer-preview">
                <img src={getImageUrl(selectedImage.image_id)} alt={selectedImage.title || selectedImage.file_name} />
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
