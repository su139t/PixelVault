import { useState, useEffect } from "react";
import { addTagToImage, createTag, deleteImage, downloadImage, getFavorites, getImageTags, getImageUrl, removeFavorite, removeTagFromImage, updateImage } from "../services/imageService";
import { ImageGrid } from "../components/gallery/ImageGrid";
import { Download, Heart, Save, Tag, Trash2, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function FavoritesPage() {
  const { user } = useAuth();
  const [images, setImages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [description, setDescription] = useState("");
  const [tagName, setTagName] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isAddingTag, setIsAddingTag] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    if (!user?.user_id) return;
    let isActive = true;

    const loadFavorites = async () => {
      try {
        setIsLoading(true);
        const response = await getFavorites(user.user_id);
        if (isActive) setImages(response.favorites || []);
      } catch (error) {
        console.error("Failed to fetch favorites:", error);
      } finally {
        if (isActive) setIsLoading(false);
      }
    };

    loadFavorites();
    return () => { isActive = false; };
  }, [user?.user_id]);

  const handleImageClick = (image) => {
    setSelectedImage(image);
    setDescription(image.description || "");
    setTagName("");
    setSelectedTags([]);
    getImageTags(image.image_id)
      .then((data) => setSelectedTags(data.data?.tags || []))
      .catch((error) => console.error("Failed to fetch image tags:", error));
  };

  const closeViewer = () => setSelectedImage(null);

  const handleSaveDescription = async () => {
    setIsSaving(true);
    try {
      const response = await updateImage(selectedImage.image_id, { description });
      const updatedImage = response.data?.image || { ...selectedImage, description };
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
      const response = await createTag(user.user_id, trimmedName);
      const tag = response.data?.tag;
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

  const handleRemoveFavorite = async () => {
    if (!selectedImage || !window.confirm("Remove this photo from favorites?")) return;
    try {
      await removeFavorite(user.user_id, selectedImage.image_id);
      setImages((currentImages) => currentImages.filter((image) => image.image_id !== selectedImage.image_id));
      closeViewer();
    } catch (error) {
      console.error("Failed to remove favorite:", error);
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
    <div>
      <div className="page-header">
        <div className="flex items-center gap-3">
          <Heart className="w-7 h-7 text-accent-rose fill-accent-rose" />
          <h1 className="page-title page-title-gradient">Favorites</h1>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <div className="spinner" />
        </div>
      ) : (
        <ImageGrid images={images} onImageClick={handleImageClick} onDownload={handleDownload} />
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
                <div className="image-viewer-heading"><p className="section-kicker">Favorite photo</p><h2>{selectedImage.title || selectedImage.file_name}</h2></div>
                <div className="image-meta-grid">
                  <div><span>Dimensions</span><strong>{selectedImage.width || "?"} × {selectedImage.height || "?"} px</strong></div>
                  <div><span>File size</span><strong>{selectedImage.file_size ? `${(selectedImage.file_size / (1024 * 1024)).toFixed(1)} MB` : "Unknown"}</strong></div>
                  <div><span>Uploaded</span><strong>{selectedImage.upload_date ? new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(selectedImage.upload_date)) : "Unknown"}</strong></div>
                  <div><span>File type</span><strong>{selectedImage.mime_type || "Image"}</strong></div>
                </div>
                <button className="favorite-button active" type="button" onClick={handleRemoveFavorite}><Heart className="h-4 w-4" fill="currentColor" /> Remove from favorites</button>
                <label className="detail-label" htmlFor="favorite-image-description">Description</label>
                <textarea id="favorite-image-description" value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Write something about this moment..." rows="4" />
                <button className="btn-primary detail-save" type="button" onClick={handleSaveDescription} disabled={isSaving}><Save className="h-4 w-4" /> {isSaving ? "Saving..." : "Save description"}</button>
                <div className="detail-tags">
                  <label className="detail-label"><Tag className="h-3.5 w-3.5" /> Tags</label>
                  <div className="tag-list">{selectedTags.map((tag) => <span className="tag-chip" key={tag.tag_id}>{tag.tag_name}<button type="button" onClick={() => handleRemoveTag(tag)} aria-label={`Remove ${tag.tag_name}`}><X className="h-3 w-3" /></button></span>)}{!selectedTags.length && <span className="detail-empty">No tags yet</span>}</div>
                  <form className="tag-form" onSubmit={handleAddTag}><input value={tagName} onChange={(event) => setTagName(event.target.value)} placeholder="Add a tag" aria-label="New tag" /><button type="submit" disabled={!tagName.trim() || isAddingTag}>Add</button></form>
                </div>
                <div className="detail-actions"><button className="detail-download" type="button" onClick={() => handleDownload(selectedImage)}><Download className="h-4 w-4" /> Download original</button><button className="detail-delete" type="button" onClick={handleDeleteImage} disabled={isDeleting}><Trash2 className="h-4 w-4" /> {isDeleting ? "Deleting..." : "Delete photo"}</button></div>
              </aside>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
