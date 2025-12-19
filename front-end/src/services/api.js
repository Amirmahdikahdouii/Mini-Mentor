import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 120000, // 2 minute timeout for AI generation
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API] Response error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

/**
 * Create a new learning roadmap
 * @param {string} query - The learning goal query
 * @returns {Promise<Object>} The created roadmap
 */
export const createRoadmap = async (query) => {
  const response = await api.post('/roadmaps', { query })
  return response.data
}

/**
 * Get a list of all roadmaps
 * @param {number} skip - Number of items to skip
 * @param {number} limit - Maximum number of items to return
 * @returns {Promise<Object>} List of roadmaps with total count
 */
export const listRoadmaps = async (skip = 0, limit = 50) => {
  const response = await api.get('/roadmaps', {
    params: { skip, limit }
  })
  return response.data
}

/**
 * Get a specific roadmap by ID
 * @param {number} id - The roadmap ID
 * @returns {Promise<Object>} The roadmap
 */
export const getRoadmap = async (id) => {
  const response = await api.get(`/roadmaps/${id}`)
  return response.data
}

/**
 * Delete a roadmap by ID
 * @param {number} id - The roadmap ID
 * @returns {Promise<void>}
 */
export const deleteRoadmap = async (id) => {
  await api.delete(`/roadmaps/${id}`)
}

export default api

