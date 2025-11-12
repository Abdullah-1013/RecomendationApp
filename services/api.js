import axios from 'axios';

const API_URL = "http://192.168.0.104:8000";

export const signup = (data) => axios.post(`${API_URL}/signup`, data);
export const login = (data) => axios.post(`${API_URL}/login`, data);
export const getRecommendations = (userId) => axios.get(`${API_URL}/recommendations/${userId}`);
