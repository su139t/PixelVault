import api from "./api";

export const createUser = (userData) => api.post("/users", userData);

export const getUsers = () => api.get("/users");
