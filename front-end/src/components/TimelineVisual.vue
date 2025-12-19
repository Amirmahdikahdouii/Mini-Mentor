<template>
  <div class="timeline-visual">
    <div class="timeline-header">
      <h3>Learning Journey</h3>
      <span class="total-duration">{{ visualData.total_duration }}</span>
    </div>
    
    <div class="timeline-container">
      <div class="timeline-line"></div>
      
      <div 
        v-for="(phase, index) in visualData.phases" 
        :key="phase.id"
        class="timeline-phase"
        :class="{ 'active': activePhase === index }"
        @click="activePhase = activePhase === index ? null : index"
      >
        <div class="phase-marker">
          <div class="marker-dot">
            <span class="marker-number">{{ index + 1 }}</span>
          </div>
        </div>
        
        <div class="phase-content">
          <div class="phase-header">
            <h4 class="phase-title">{{ phase.title }}</h4>
            <span class="phase-duration">{{ phase.duration }}</span>
          </div>
          
          <p class="phase-description">{{ phase.description }}</p>
          
          <transition name="expand">
            <div v-if="activePhase === index" class="phase-milestones">
              <div class="milestones-header">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Milestones</span>
              </div>
              <ul class="milestones-list">
                <li v-for="(milestone, mIndex) in phase.milestones" :key="mIndex">
                  {{ milestone }}
                </li>
              </ul>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  visualData: {
    type: Object,
    required: true
  }
})

const activePhase = ref(0)
</script>

<style scoped>
.timeline-visual {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}

.timeline-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-muted);
}

.timeline-header h3 {
  font-size: 1.125rem;
  color: var(--text-primary);
}

.total-duration {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 600;
  font-size: 0.875rem;
}

.timeline-container {
  position: relative;
  padding-left: 2rem;
}

.timeline-line {
  position: absolute;
  left: 15px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--accent-primary), var(--accent-secondary));
  border-radius: 1px;
}

.timeline-phase {
  position: relative;
  margin-bottom: 1.5rem;
  cursor: pointer;
}

.timeline-phase:last-child {
  margin-bottom: 0;
}

.phase-marker {
  position: absolute;
  left: -2rem;
  top: 0;
}

.marker-dot {
  width: 30px;
  height: 30px;
  background: var(--bg-secondary);
  border: 2px solid var(--accent-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  z-index: 1;
  position: relative;
}

.timeline-phase.active .marker-dot {
  background: var(--gradient-primary);
  border-color: transparent;
  box-shadow: var(--shadow-glow);
}

.marker-number {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--accent-primary);
}

.timeline-phase.active .marker-number {
  color: white;
}

.phase-content {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 1rem;
  transition: all var(--transition-normal);
}

.timeline-phase:hover .phase-content,
.timeline-phase.active .phase-content {
  border-color: var(--accent-primary);
}

.phase-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.phase-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

.phase-duration {
  font-size: 0.75rem;
  color: var(--accent-primary);
  background: rgba(88, 166, 255, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  white-space: nowrap;
}

.phase-description {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.5;
}

.phase-milestones {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-muted);
}

.milestones-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--accent-success);
  margin-bottom: 0.5rem;
}

.milestones-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.milestones-list li {
  font-size: 0.8rem;
  color: var(--text-secondary);
  padding: 0.25rem 0;
  padding-left: 1rem;
  position: relative;
}

.milestones-list li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--accent-primary);
}

/* Expand transition */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  margin-top: 0;
  padding-top: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 200px;
}
</style>

