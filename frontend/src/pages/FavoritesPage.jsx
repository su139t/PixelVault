import { useState, useEffect } from "react";
import api from "../services/api";
import { ImageGrid } from "../components/gallery/ImageGrid";
import { Heart } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function FavoritesPage() {
  const { user } = useAuth();
  const [images, setImages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user?.user_id) return;
    let isActive = true;

    const loadFavorites = async () => {
      try {
        setIsLoading(true);
        const response = await api.get(`/favorites?user_id=${user.user_id}`);
        if (isActive) setImages(response.data.data?.favorites || []);
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
    console.log("Favorite clicked:", image);
    // TODO: Open modal viewer
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
        <ImageGrid images={images} onImageClick={handleImageClick} />
      )}
    </div>
  );
}
