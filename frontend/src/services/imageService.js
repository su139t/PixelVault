import api from "./api";

export const getImages = async (userId) => {
  const uid = userId || localStorage.getItem("pv_user") && JSON.parse(localStorage.getItem("pv_user"))?.user_id;
  const response = await api.get(`/images?user_id=${uid}`);
  return response.data;
};

export const searchImages = async (userId, query, uploadDate) => {
  const params = new URLSearchParams({ user_id: userId });
  if (query?.trim()) params.set("q", query.trim());
  if (uploadDate) params.set("date", uploadDate);
  const response = await api.get(`/search?${params.toString()}`);
  return response.data;
};

export const getImage = async (imageId) => {
  const response = await api.get(`/images/${imageId}`);
  return response.data;
};

export const updateImage = async (imageId, changes) => {
  const response = await api.put(`/images/${imageId}`, changes);
  return response.data;
};

export const getImageTags = async (imageId) => {
  const response = await api.get(`/images/${imageId}/tags`);
  return response.data;
};

export const createTag = async (userId, tagName) => {
  const response = await api.post("/tags", { user_id: userId, tag_name: tagName });
  return response.data;
};

export const addTagToImage = async (imageId, tagId) => {
  const response = await api.post(`/images/${imageId}/tags/${tagId}`);
  return response.data;
};

export const removeTagFromImage = async (imageId, tagId) => {
  const response = await api.delete(`/images/${imageId}/tags/${tagId}`);
  return response.data;
};

export const uploadImage = async (file, title, userId) => {
  const uid = userId || localStorage.getItem("pv_user") && JSON.parse(localStorage.getItem("pv_user"))?.user_id;
  const formData = new FormData();
  formData.append("file", file);
  formData.append("user_id", uid);
  if (title) formData.append("title", title);

  const response = await api.post("/images", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

export const deleteImage = async (imageId) => {
  const response = await api.delete(`/images/${imageId}`);
  return response.data;
};

// URL for an image tag (used directly in img src)
export const getImageUrl = (imageId) => {
  return `${api.defaults.baseURL}/images/${imageId}/file`;
};

export const downloadImage = async (imageId) => {
  const response = await api.get(`/images/${imageId}/file`, {
    responseType: "blob",
  });
  return response.data;
};
