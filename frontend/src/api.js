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