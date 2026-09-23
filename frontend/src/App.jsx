import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { Layout } from "./components/layout/Layout";
import LoginPage from "./pages/LoginPage";
import PhotosPage from "./pages/PhotosPage";
import AlbumsPage from "./pages/AlbumsPage";
import FavoritesPage from "./pages/FavoritesPage";
import PeoplePage from "./pages/PeoplePage";
import SearchPage from "./pages/SearchPage";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public route */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<PhotosPage />} />
                    <Route path="/search" element={<SearchPage />} />
                    <Route path="/albums" element={<AlbumsPage />} />
                    <Route path="/people" element={<PeoplePage />} />
                    <Route path="/tags" element={<div className="text-white/60 text-center py-20">Tags — Coming Soon</div>} />
                    <Route path="/favorites" element={<FavoritesPage />} />
                  </Routes>
                </Layout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
