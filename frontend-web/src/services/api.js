import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const fetchEquipment = async () => {
  const response = await fetch(`${API_BASE}/equipment/`);
  return response.json();
};

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