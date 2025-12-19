<template>
  <div class="home-view">
    <div class="hero-section">
      <div class="hero-content animate-slide-up">
        <h1 class="hero-title">
          <span class="gradient-text">Your AI Learning Mentor</span>
        </h1>
        <p class="hero-description">
          Tell us what you want to learn, and we'll create a personalized roadmap 
          with phases, milestones, and resources to guide your journey.
        </p>
      </div>
      
      <InputSection 
        @submit="handleSubmit" 
        :loading="loading"
        class="animate-slide-up delay-1"
      />
      
      <div v-if="error" class="error-message animate-fade-in">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        {{ error }}
      </div>
    </div>
    
    <div v-if="roadmap" class="result-section animate-slide-up">
      <RoadmapDisplay :roadmap="roadmap" />
    </div>
    
    <div v-if="!roadmap" class="features-section animate-slide-up delay-2">
      <div class="feature-card">
        <div class="feature-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <h3>Structured Learning</h3>
        <p>Get a clear, phased approach to mastering any skill</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </div>
        <h3>Time Estimates</h3>
        <p>Know how long each phase will take to complete</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
          </svg>
        </div>
        <h3>Curated Resources</h3>
        <p>Access recommended books, courses, and tutorials</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import InputSection from '../components/InputSection.vue'
import RoadmapDisplay from '../components/RoadmapDisplay.vue'
import { createRoadmap } from '../services/api'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const roadmap = ref(null)

const handleSubmit = async (query) => {
  loading.value = true
  error.value = null
  
  try {
    const result = await createRoadmap(query)
    roadmap.value = result
    // Navigate to the roadmap view
    router.push(`/roadmap/${result.id}`)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to generate roadmap. Please try again.'
    console.error('Error creating roadmap:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.home-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 2rem;
}

.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4rem 1rem 3rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.hero-content {
  margin-bottom: 2.5rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.gradient-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  line-height: 1.7;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(248, 81, 73, 0.1);
  border: 1px solid var(--accent-danger);
  border-radius: var(--radius-md);
  color: var(--accent-danger);
  font-size: 0.9rem;
}

.result-section {
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
  padding-top: 2rem;
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  max-width: 1000px;
  margin: 4rem auto 0;
  width: 100%;
}

.feature-card {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 2rem;
  text-align: center;
  transition: all var(--transition-normal);
}

.feature-card:hover {
  border-color: var(--accent-primary);
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.feature-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: var(--gradient-primary);
  border-radius: var(--radius-lg);
  margin-bottom: 1rem;
  color: white;
}

.feature-card h3 {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  font-size: 0.9rem;
  color: var(--text-muted);
}

/* Animation delays */
.delay-1 {
  animation-delay: 0.1s;
}

.delay-2 {
  animation-delay: 0.2s;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .hero-section {
    padding: 2rem 1rem;
  }
}
</style>

