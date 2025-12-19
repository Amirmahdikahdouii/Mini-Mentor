<template>
  <aside class="sidebar" :class="{ 'is-open': isOpen }">
    <div class="sidebar-header">
      <h2>History</h2>
      <button class="btn btn-ghost close-btn" @click="$emit('toggle')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    
    <div class="sidebar-content">
      <div v-if="loading" class="loading-state">
        <LoadingSpinner size="small" />
        <span>Loading...</span>
      </div>
      
      <div v-else-if="roadmaps.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="12" y1="18" x2="12" y2="12"></line>
          <line x1="9" y1="15" x2="15" y2="15"></line>
        </svg>
        <p>No roadmaps yet</p>
        <span>Create your first learning roadmap!</span>
      </div>
      
      <ul v-else class="roadmap-list">
        <li 
          v-for="roadmap in roadmaps" 
          :key="roadmap.id"
          class="roadmap-item"
          @click="$emit('select', roadmap.id)"
        >
          <div class="item-content">
            <h4 class="item-title">{{ roadmap.title }}</h4>
            <p class="item-query">{{ roadmap.user_query }}</p>
            <span class="item-date">{{ formatDate(roadmap.created_at) }}</span>
          </div>
          <svg class="item-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </li>
      </ul>
    </div>
    
    <div v-if="roadmaps.length > 0" class="sidebar-footer">
      <span class="count">{{ roadmaps.length }} roadmap{{ roadmaps.length !== 1 ? 's' : '' }}</span>
    </div>
  </aside>
  
  <div 
    v-if="isOpen" 
    class="sidebar-overlay" 
    @click="$emit('toggle')"
  ></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'
import { listRoadmaps } from '../services/api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle', 'select'])

const roadmaps = ref([])
const loading = ref(false)

const fetchRoadmaps = async () => {
  loading.value = true
  try {
    const response = await listRoadmaps()
    roadmaps.value = response.roadmaps
  } catch (err) {
    console.error('Error fetching roadmaps:', err)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

onMounted(fetchRoadmaps)

// Refresh when sidebar opens
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    fetchRoadmaps()
  }
})
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 300px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  transform: translateX(-100%);
  transition: transform var(--transition-normal);
  z-index: 100;
}

.sidebar.is-open {
  transform: translateX(0);
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
  animation: fadeIn 0.2s ease;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-default);
}

.sidebar-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
}

.close-btn {
  padding: 0.5rem;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem 1rem;
  gap: 0.75rem;
  color: var(--text-muted);
}

.empty-state svg {
  opacity: 0.5;
}

.empty-state p {
  font-weight: 500;
  color: var(--text-secondary);
}

.empty-state span {
  font-size: 0.85rem;
}

.roadmap-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.roadmap-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.roadmap-item:hover {
  border-color: var(--accent-primary);
  background: var(--bg-card-hover);
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-query {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-date {
  font-size: 0.7rem;
  color: var(--accent-primary);
}

.item-arrow {
  color: var(--text-muted);
  flex-shrink: 0;
  margin-left: 0.5rem;
  transition: transform var(--transition-fast);
}

.roadmap-item:hover .item-arrow {
  color: var(--accent-primary);
  transform: translateX(3px);
}

.sidebar-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid var(--border-default);
}

.count {
  font-size: 0.8rem;
  color: var(--text-muted);
}

@media (min-width: 769px) {
  .sidebar-overlay {
    display: none;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

