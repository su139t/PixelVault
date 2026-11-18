import { useState } from "react";
import { CalendarDays, Search, SlidersHorizontal, X } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { ImageGrid } from "../components/gallery/ImageGrid";
import { downloadImage, searchImages } from "../services/imageService";

export default function SearchPage() {
  const { user } = useAuth();
  const [query, setQuery] = useState("");
  const [date, setDate] = useState("");
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (event) => {
    event.preventDefault();
    if (!query.trim() && !date) return;

    setIsLoading(true);
    setError("");
    setHasSearched(true);
    try {
      const response = await searchImages(user.user_id, query, date);
      setResults(response.data?.images || response.images || []);
    } catch (searchError) {
      console.error("Failed to search images:", searchError);
      setError("Search could not be completed. Please try again.");
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setQuery("");
    setDate("");
    setResults([]);
    setHasSearched(false);
    setError("");
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
    <div className="search-page">
      <header className="search-header">
        <div>
          <p className="section-kicker"><SlidersHorizontal className="h-3.5 w-3.5" /> Find a memory</p>
          <h1 className="page-title">Search your vault</h1>
          <p className="search-description">Look through titles, descriptions, AI notes, tags, filenames, or a specific upload date.</p>
        </div>
      </header>

      <form className="search-form" onSubmit={handleSearch}>
        <label className="search-input-wrap" htmlFor="photo-search">
          <Search className="h-4 w-4" />
          <input id="photo-search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Try “passport”, “beach”, or a description" />
        </label>
        <label className="date-input-wrap" htmlFor="photo-date">
          <CalendarDays className="h-4 w-4" />
          <input id="photo-date" type="date" value={date} onChange={(event) => setDate(event.target.value)} aria-label="Filter by upload date" />
        </label>
        <button className="btn-primary search-submit" type="submit" disabled={isLoading || (!query.trim() && !date)}>
          <Search className="h-4 w-4" /> Search
        </button>
        {(query || date) && <button className="search-clear" type="button" onClick={handleClear} title="Clear search"><X className="h-4 w-4" /> Clear</button>}
      </form>

      {error && <p className="search-error">{error}</p>}
      {isLoading && <div className="flex justify-center py-20"><div className="spinner" /></div>}
      {!isLoading && hasSearched && results.length > 0 && (
        <div className="search-results">
          <div className="search-results-heading"><p className="section-kicker">Results</p><strong>{results.length} {results.length === 1 ? "photo" : "photos"} found</strong></div>
          <ImageGrid images={results} onImageClick={() => {}} onDownload={handleDownload} />
        </div>
      )}
      {!isLoading && hasSearched && !results.length && !error && (
        <div className="empty-state search-empty"><div className="empty-state-icon"><Search className="w-7 h-7 text-accent-violet" /></div><p className="empty-state-title">No matching photos</p><p className="empty-state-text">Try a different word or upload date.</p></div>
      )}
      {!hasSearched && <div className="search-hint"><Search className="h-5 w-5" /><p>Search by what you remember, not just the filename.</p></div>}
    </div>
  );
}
