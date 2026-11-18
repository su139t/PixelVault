import { Link, useLocation } from "react-router-dom";
import { Image as ImageIcon, Search, Folder, Heart, Users } from "lucide-react";

export function BottomNav() {
  const location = useLocation();

  const items = [
    { name: "Photos", path: "/", icon: <ImageIcon className="w-5 h-5" /> },
    { name: "Search", path: "/search", icon: <Search className="w-5 h-5" /> },
    { name: "Albums", path: "/albums", icon: <Folder className="w-5 h-5" /> },
    { name: "People", path: "/people", icon: <Users className="w-5 h-5" /> },
    { name: "Favorites", path: "/favorites", icon: <Heart className="w-5 h-5" /> },
  ];

  const isActive = (path) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  return (
    <div className="bottom-nav">
      <div className="bottom-nav-items">
        {items.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`bottom-nav-link ${isActive(item.path) ? "active" : ""}`}
          >
            {item.icon}
            <span>{item.name}</span>
            <div className="bottom-nav-dot" />
          </Link>
        ))}
      </div>
    </div>
  );
}
