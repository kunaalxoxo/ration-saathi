import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use((c) => {
  const t = localStorage.getItem('token');
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});

export const authApi = {
  requestOtp: (p: string) => api.post('/auth/request-otp', { phone: p }),
  verifyOtp: (p: string, o: string) => api.post('/auth/verify-otp', { phone: p, otp: o })
};

export const casesApi = {
  getDetails: (id: string) => api.get(`/cases/${id}`),
  create: (d: any) => api.post('/cases', d)
};

export const entitlementApi = {
  check: (n: string) => api.get(`/entitlement/check?card_number=${n}`)
};

export const analyticsApi = {
  getOverview: () => api.get('/analytics/overview'),
  getFpsRisk: (p: any) => api.get('/analytics/fps-risk', { params: p }),
  getDistrictSummary: () => api.get('/analytics/district-summary')
};

export default api;
