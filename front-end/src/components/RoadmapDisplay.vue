<template>
  <div class="roadmap-display">
    <h2 v-if="showTitle" class="display-title">{{ roadmap.title }}</h2>
    <div class="markdown-content" v-html="renderedContent"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps({
  roadmap: {
    type: Object,
    required: true
  },
  showTitle: {
    type: Boolean,
    default: true
  }
})

// Configure marked with syntax highlighting
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.error('Highlighting error:', err)
      }
    }
    return code
  },
  breaks: true,
  gfm: true
})

const renderedContent = computed(() => {
  if (!props.roadmap?.content) return ''
  return marked.parse(props.roadmap.content)
})
</script>

<style scoped>
.roadmap-display {
  animation: fadeIn 0.3s ease-out;
}

.display-title {
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--accent-primary);
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.markdown-content {
  line-height: 1.8;
  color: var(--text-secondary);
}

/* Import highlight.js theme styles */
.markdown-content :deep(pre) {
  background: var(--bg-primary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 1rem;
  overflow-x: auto;
  margin: 1rem 0;
}

.markdown-content :deep(code) {
  font-family: var(--font-mono);
  font-size: 0.875rem;
}

.markdown-content :deep(pre code) {
  background: none;
  padding: 0;
  color: var(--text-primary);
}

/* Syntax highlighting colors */
.markdown-content :deep(.hljs-keyword),
.markdown-content :deep(.hljs-selector-tag) {
  color: #ff7b72;
}

.markdown-content :deep(.hljs-string),
.markdown-content :deep(.hljs-addition) {
  color: #a5d6ff;
}

.markdown-content :deep(.hljs-comment) {
  color: #8b949e;
}

.markdown-content :deep(.hljs-function),
.markdown-content :deep(.hljs-title) {
  color: #d2a8ff;
}

.markdown-content :deep(.hljs-variable),
.markdown-content :deep(.hljs-attr) {
  color: #79c0ff;
}

.markdown-content :deep(.hljs-number) {
  color: #ffa657;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

