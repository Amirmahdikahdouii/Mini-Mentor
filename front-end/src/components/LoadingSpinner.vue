<template>
  <div class="spinner-container" :class="size">
    <div class="spinner">
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})
</script>

<style scoped>
.spinner-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.spinner-container.small {
  --spinner-size: 20px;
  --ring-size: 2px;
}

.spinner-container.medium {
  --spinner-size: 40px;
  --ring-size: 3px;
}

.spinner-container.large {
  --spinner-size: 60px;
  --ring-size: 4px;
}

.spinner {
  position: relative;
  width: var(--spinner-size);
  height: var(--spinner-size);
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: var(--ring-size) solid transparent;
}

.spinner-ring:nth-child(1) {
  border-top-color: var(--accent-primary);
  animation: spin 1s linear infinite;
}

.spinner-ring:nth-child(2) {
  border-right-color: var(--accent-secondary);
  animation: spin 1s linear infinite 0.1s;
  opacity: 0.8;
}

.spinner-ring:nth-child(3) {
  border-bottom-color: var(--accent-primary);
  animation: spin 1s linear infinite 0.2s;
  opacity: 0.6;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>

