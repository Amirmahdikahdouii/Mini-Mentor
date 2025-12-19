<template>
  <div class="app-layout">
    <HistorySidebar 
      :is-open="sidebarOpen" 
      @toggle="sidebarOpen = !sidebarOpen"
      @select="handleSelectRoadmap"
    />
    <main class="main-content" :class="{ 'sidebar-open': sidebarOpen }">
      <header class="app-header">
        <button class="menu-btn btn-ghost" @click="sidebarOpen = !sidebarOpen">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
        <div class="logo">
          <svg width="32" height="32" viewBox="0 0 100 100">
            <defs>
              <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#58a6ff" />
                <stop offset="100%" style="stop-color:#1f6feb" />
              </linearGradient>
            </defs>
            <circle cx="50" cy="50" r="45" fill="url(#logoGrad)"/>
            <path d="M30 55 L45 70 L75 35" stroke="white" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="logo-text">Mini Mentor</span>
        </div>
      </header>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import HistorySidebar from './components/HistorySidebar.vue'

const router = useRouter()
const sidebarOpen = ref(false)

const handleSelectRoadmap = (id) => {
  router.push(`/roadmap/${id}`)
  if (window.innerWidth < 768) {
    sidebarOpen.value = false
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left var(--transition-normal);
}

.main-content.sidebar-open {
  margin-left: 300px;
}

.app-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-default);
  position: sticky;
  top: 0;
  z-index: 10;
}

.menu-btn {
  padding: 0.5rem;
  border-radius: var(--radius-sm);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 600;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .main-content.sidebar-open {
    margin-left: 0;
  }
}
</style>

