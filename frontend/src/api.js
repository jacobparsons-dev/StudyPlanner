import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000",
});
export const getRecommendations = async () => {
  const response = await API.get("/recommendations");
  return response.data;
};

export const createReview = async (reviewData) => {
  const response = await API.post("/reviews", reviewData);
  return response.data;
};
export const getStudyItems = async() => {
    const response = await API.get("/study-items");
    return response.data;
};
export const createStudyItem = async (itemData) => {
    const response = await API.post("/study-items", itemData);
    return response.data;
};
export const updateStudyItem = async (itemId, itemData) => {
    const response = await API.put(`/study-items/${itemId}`, itemData);
    return response.data;
};
export const deleteStudyItem = async (itemId) => {
    const response = await API.delete(`/study-items/${itemId}`);
    return response.data;
};