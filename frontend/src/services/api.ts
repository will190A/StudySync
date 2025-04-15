import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 用户相关 API
export const authAPI = {
  login: (data: { username: string; password: string }) =>
    api.post('/auth/login', data),
  register: (data: { username: string; email: string; password: string; full_name?: string }) =>
    api.post('/users/register', data),
};

// 用户相关 API
export const userAPI = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data: { full_name?: string; password?: string }) =>
    api.put('/users/me', data),
  checkIn: () => api.post('/users/check-in'),
};

// 题目相关 API
export const questionAPI = {
  getDailyPractice: () => api.get('/questions/daily-practice'),
  submitAnswer: (data: { question_id: number; answer: any[]; time_spent: number }) =>
    api.post('/questions/answer', data),
  getWrongQuestions: () => api.get('/questions/wrong-questions'),
  getKnowledgeProfile: () => api.get('/questions/knowledge-profile'),
};

// 学习计划相关 API
export const studyPlanAPI = {
  generatePlan: (data: { target_date: string; daily_study_time: number }) =>
    api.post('/study-plans/generate', data),
  getMyPlans: () => api.get('/study-plans/my-plans'),
  getPlan: (id: number) => api.get(`/study-plans/plan/${id}`),
  completeTask: (id: number) => api.put(`/study-plans/task/${id}/complete`),
  skipTask: (id: number) => api.put(`/study-plans/task/${id}/skip`),
};

export default api; 