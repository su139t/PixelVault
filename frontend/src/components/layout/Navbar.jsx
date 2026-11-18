import { Link, useLocation } from "react-router-dom";
import { Image as ImageIcon, Search, Folder, Users, Tag, Heart, LogOut } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export function Navbar() {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { name: "Photos", path: "/", icon: <ImageIcon className="w-[18px] h-[18px]" /> },
    { name: "Search", path: "/search", icon: <Search className="w-[18px] h-[18px]" /> },
    { name: "Albums", path: "/albums", icon: <Folder className="w-[18px] h-[18px]" /> },
    { name: "People", path: "/people", icon: <Users className="w-[18px] h-[18px]" /> },
    { name: "Tags", path: "/tags", icon: <Tag className="w-[18px] h-[18px]" /> },
    { name: "Favorites", path: "/favorites", icon: <Heart className="w-[18px] h-[18px]" /> },
  ];

  const isActive = (path) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  const initial = user?.name?.charAt(0)?.toUpperCase() || "U";

  return (
    <nav className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <ImageIcon className="w-[18px] h-[18px] text-white" />
        </div>
        <span className="sidebar-logo-text">PixelVault</span>
      </div>

      {/* Navigation */}
      <div className="sidebar-nav">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`nav-link ${isActive(item.path) ? "active" : ""}`}
          >
            <span className="nav-icon">{item.icon}</span>
            {item.name}
          </Link>
        ))}
      </div>

      {/* User Profile */}
      <div className="sidebar-user">
        <div className="sidebar-user-card">
          <div className="sidebar-avatar">
            {user?.photo_url ? (
              <img src={user.photo_url} alt={user.name} />
            ) : (
              initial
            )}
          </div>
          <div className="sidebar-user-info">
            <p className="sidebar-user-name">{user?.name || "User"}</p>
            <p className="sidebar-user-handle">
              {user?.username ? `@${user.username}` : `ID: ${user?.user_id || ""}`}
            </p>
          </div>
          <button
            onClick={logout}
            className="sidebar-logout"
            title="Sign out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </nav>
  );
}
