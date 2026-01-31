import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const equipmentAPI = {
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  
  getDataset: (id) => api.get(`/datasets/${id}/`),
  getHistory: () => api.get('/history/'),
  downloadPDF: (id) => api.get(`/datasets/${id}/pdf/`, { responseType: 'blob' }),
};

export default api;