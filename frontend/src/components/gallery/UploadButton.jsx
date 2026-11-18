import { useRef, useState } from "react";
import { Upload, Loader2 } from "lucide-react";
import { uploadImage } from "../../services/imageService";

export function UploadButton({ onUploadSuccess }) {
  const fileInputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadCount, setUploadCount] = useState(0);
  const [uploadProgress, setUploadProgress] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    try {
      setError("");
      setIsUploading(true);
      setUploadCount(files.length);
      setUploadProgress({ completed: 0, total: files.length, failed: 0 });
      const failedFiles = [];
      for (const file of files) {
        try {
          const title = file.name.replace(/\.[^/.]+$/, "");
          await uploadImage(file, title);
        } catch (uploadError) {
          console.error(`Upload failed for ${file.name}:`, uploadError);
          failedFiles.push(file.name);
        } finally {
          setUploadProgress((currentProgress) => ({
            ...currentProgress,
            completed: currentProgress.completed + 1,
            failed: failedFiles.length,
          }));
        }
      }

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      if (failedFiles.length) {
        setError(`${files.length - failedFiles.length} uploaded. Failed: ${failedFiles.join(", ")}`);
      }

      if (onUploadSuccess && failedFiles.length < files.length) {
        await onUploadSuccess();
      }
    } catch (error) {
      console.error("Upload failed:", error);
      setError(error.response?.data?.message || "Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
      setUploadCount(0);
    }
  };

  return (
    <div className="upload-control">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        multiple
        className="hidden"
      />
      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={isUploading}
        className="btn-primary"
      >
        {isUploading ? (
          <Loader2 className="w-[18px] h-[18px] animate-spin" />
        ) : (
          <Upload className="w-[18px] h-[18px]" />
        )}
        {isUploading ? `Uploading ${uploadCount}…` : "Upload photos"}
      </button>
      {uploadProgress && (
        <div className="upload-progress" role="status" aria-live="polite">
          <div className="upload-progress-label"><span>{uploadProgress.completed === uploadProgress.total ? "Upload complete" : "Uploading photos..."}</span><strong>{uploadProgress.completed}/{uploadProgress.total}</strong></div>
          <div className="upload-progress-track"><div className="upload-progress-bar" style={{ width: `${(uploadProgress.completed / uploadProgress.total) * 100}%` }} /></div>
        </div>
      )}
      {error && <p className="upload-error" role="alert">{error}</p>}
    </div>
  );
}
