<template>
  <div class="roadmap-view">
    <div v-if="loading" class="loading-container">
      <LoadingSpinner />
      <p>Loading your roadmap...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <div class="error-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <h2>Oops! Something went wrong</h2>
      <p>{{ error }}</p>
      <button class="btn btn-primary" @click="router.push('/')">
        Go Back Home
      </button>
    </div>
    
    <div v-else-if="roadmap" class="roadmap-container animate-fade-in">
      <div class="roadmap-header">
        <button class="btn btn-ghost back-btn" @click="router.push('/')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          New Roadmap
        </button>
        
        <div class="roadmap-meta">
          <span class="query-badge">{{ roadmap.user_query }}</span>
          <span class="date-badge">{{ formatDate(roadmap.created_at) }}</span>
        </div>
        
        <button class="btn btn-ghost delete-btn" @click="handleDelete" title="Delete roadmap">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
      
      <h1 class="roadmap-title">{{ roadmap.title }}</h1>
      
      <div class="roadmap-content-wrapper">
        <div class="timeline-section">
          <TimelineVisual 
            v-if="roadmap.visual_data" 
            :visual-data="roadmap.visual_data" 
          />
        </div>
        
        <div class="markdown-section">
          <RoadmapDisplay :roadmap="roadmap" :show-title="false" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import RoadmapDisplay from '../components/RoadmapDisplay.vue'
import TimelineVisual from '../components/TimelineVisual.vue'
import { getRoadmap, deleteRoadmap } from '../services/api'

const route = useRoute()
const router = useRouter()

const roadmap = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchRoadmap = async (id) => {
  loading.value = true
  error.value = null
  
  try {
    roadmap.value = await getRoadmap(id)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load roadmap'
    console.error('Error fetching roadmap:', err)
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this roadmap?')) return
  
  try {
    await deleteRoadmap(roadmap.value.id)
    router.push('/')
  } catch (err) {
    console.error('Error deleting roadmap:', err)
    alert('Failed to delete roadmap')
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchRoadmap(route.params.id)
})

watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchRoadmap(newId)
  }
})
</script>

<style scoped>
.roadmap-view {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
  gap: 1rem;
}

.error-icon {
  color: var(--accent-danger);
  margin-bottom: 1rem;
}

.error-container h2 {
  color: var(--text-primary);
}

.error-container p {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.roadmap-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.roadmap-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.roadmap-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.query-badge {
  background: var(--bg-tertiary);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  color: var(--text-secondary);
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.date-badge {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.delete-btn {
  color: var(--text-muted);
}

.delete-btn:hover {
  color: var(--accent-danger);
  background: rgba(248, 81, 73, 0.1);
}

.roadmap-title {
  font-size: 2rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.roadmap-content-wrapper {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
  align-items: start;
}

.timeline-section {
  position: sticky;
  top: 100px;
}

.markdown-section {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 2rem;
}

@media (max-width: 1024px) {
  .roadmap-content-wrapper {
    grid-template-columns: 1fr;
  }
  
  .timeline-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .roadmap-view {
    padding: 1rem;
  }
  
  .roadmap-title {
    font-size: 1.5rem;
  }
  
  .markdown-section {
    padding: 1rem;
  }
}
</style>





