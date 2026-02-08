import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,  // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add CORS headers support
api.defaults.xsrfCookieName = 'csrftoken';
api.defaults.xsrfHeaderName = 'X-CSRFToken';

export const fetchEquipment = async () => {
  const response = await fetch(`${API_BASE}/equipment/`);
  return response.json();
};

export const equipmentAPI = {
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    // Don't manually set Content-Type header for FormData - Axios handles this
    return api.post('/upload/', formData);
  },
  
  getDataset: (id) => api.get(`/datasets/${id}/`),
  getHistory: () => api.get('/history/'),
  downloadPDF: (id) => api.get(`/datasets/${id}/pdf/`, { responseType: 'blob' }),
};

export default api;