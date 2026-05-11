import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('resumelift_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authApi = {
  register: (payload) => api.post('/register', payload),
  login: (payload) => api.post('/login', payload),
}

export const resumeApi = {
  list: () => api.get('/resumes'),
  upload: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/resumes/upload-resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

export const jobApi = {
  list: () => api.get('/job-description'),
  create: (payload) => api.post('/job-description', payload),
}

export const matchApi = {
  list: () => api.get('/matches'),
  analyze: (payload) => api.post('/analyze-match', payload),
  feedback: (payload) => api.post('/generate-feedback', payload),
}

export const dashboardApi = {
  get: () => api.get('/dashboard'),
}

export default api
