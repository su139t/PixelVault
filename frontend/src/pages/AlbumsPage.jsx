import { useState, useEffect } from "react";
import api from "../services/api";
import { FolderPlus, Folder } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function AlbumsPage() {
  const { user } = useAuth();
  const [albums, setAlbums] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user?.user_id) return;
    let isActive = true;

    const loadAlbums = async () => {
      try {
        setIsLoading(true);
        const response = await api.get(`/albums?user_id=${user.user_id}`);
        if (isActive) setAlbums(response.data.data?.albums || []);
      } catch (error) {
        console.error("Failed to fetch albums:", error);
      } finally {
        if (isActive) setIsLoading(false);
      }
    };

    loadAlbums();
    return () => { isActive = false; };
  }, [user?.user_id]);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title page-title-gradient">Albums</h1>
        <button className="btn-primary">
          <FolderPlus className="w-[18px] h-[18px]" />
          New Album
        </button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <div className="spinner" />
        </div>
      ) : albums.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">
            <Folder className="w-7 h-7 text-accent-violet" />
          </div>
          <p className="empty-state-title">No albums yet</p>
          <p className="empty-state-text">Create one to organize your photos</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {albums.map((album, i) => (
            <div
              key={album.album_id}
              className="album-card"
              style={{ animationDelay: `${i * 0.05}s` }}
            >
              <div className="album-card-cover animate-[fade-in_0.4s_ease_both]">
                <Folder className="w-12 h-12 text-accent-violet/50" />
              </div>
              <h3 className="font-medium text-text-primary text-sm px-1 truncate">
                {album.album_name}
              </h3>
              <p className="text-xs text-text-muted px-1">
                {new Date(album.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
