<template>
  <div class="input-section">
    <form @submit.prevent="handleSubmit" class="input-form">
      <div class="input-wrapper">
        <textarea
          v-model="query"
          class="input query-input"
          placeholder="What do you want to learn? e.g., 'I want to learn Go language' or 'Help me master machine learning'"
          :disabled="loading"
          rows="3"
          @keydown.enter.ctrl="handleSubmit"
          @keydown.enter.meta="handleSubmit"
        ></textarea>
        
        <div class="input-actions">
          <span class="shortcut-hint">Press Ctrl+Enter to submit</span>
          <button 
            type="submit" 
            class="btn btn-primary submit-btn"
            :disabled="!query.trim() || loading"
          >
            <LoadingSpinner v-if="loading" size="small" />
            <template v-else>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
              Generate Roadmap
            </template>
          </button>
        </div>
      </div>
    </form>
    
    <div class="suggestions">
      <span class="suggestions-label">Try:</span>
      <button 
        v-for="suggestion in suggestions" 
        :key="suggestion"
        class="suggestion-chip"
        @click="setQuery(suggestion)"
        :disabled="loading"
      >
        {{ suggestion }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoadingSpinner from './LoadingSpinner.vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const query = ref('')

const suggestions = [
  'Learn Python',
  'Master React',
  'DevOps fundamentals',
  'System Design',
  'Data Science'
]

const handleSubmit = () => {
  if (query.value.trim() && !props.loading) {
    emit('submit', query.value.trim())
  }
}

const setQuery = (text) => {
  query.value = `I want to learn ${text}`
  handleSubmit()
}
</script>

<style scoped>
.input-section {
  width: 100%;
  max-width: 700px;
}

.input-form {
  width: 100%;
}

.input-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 1rem;
  transition: all var(--transition-normal);
}

.input-wrapper:focus-within {
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-glow);
}

.query-input {
  background: transparent;
  border: none;
  resize: none;
  font-size: 1rem;
  line-height: 1.6;
}

.query-input:focus {
  box-shadow: none;
}

.input-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-muted);
}

.shortcut-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.suggestions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  justify-content: center;
}

.suggestions-label {
  font-size: 0.875rem;
  color: var(--text-muted);
}

.suggestion-chip {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 0.375rem 0.875rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: var(--font-sans);
}

.suggestion-chip:hover:not(:disabled) {
  background: var(--bg-card-hover);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.suggestion-chip:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .input-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .shortcut-hint {
    display: none;
  }
  
  .submit-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>





