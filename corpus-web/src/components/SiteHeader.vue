<template>
  <header class="header">
    <div class="header-inner card">
      <router-link to="/" class="brand">
        <img src="/images/logo-mark.svg" alt="" class="brand-icon" width="40" height="40" />
        <div class="brand-text">
          <span class="brand-title">方言语料库</span>
          <span class="brand-sub">老派 · 新派 · 语音</span>
        </div>
      </router-link>
      <button type="button" class="menu-toggle" aria-label="打开菜单" @click="open = !open">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav" :class="{ open }">
        <router-link v-for="l in links" :key="l.to" :to="l.to" @click="open = false">{{ l.label }}</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const open = ref(false)
const links = [
  { to: '/', label: '首页' },
  { to: '/corpus', label: '语料库' },
  { to: '/search', label: '搜索' },
  { to: '/about', label: '关于' }
]
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  padding: 0.75rem 1.25rem 0;
  background: linear-gradient(180deg, var(--bg-page) 70%, transparent);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 0.65rem 1.25rem;
  background: rgba(255, 252, 247, 0.92);
  backdrop-filter: blur(8px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: inherit;
  text-decoration: none;
}
.brand:hover {
  text-decoration: none;
  opacity: 0.9;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.brand-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 600;
}

.brand-sub {
  font-size: 0.75rem;
  color: var(--ink-muted);
}

.nav {
  display: flex;
  gap: 0.25rem 1.25rem;
  align-items: center;
}

.nav a {
  color: var(--ink);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 0.35rem 0;
  border-bottom: 2px solid transparent;
  text-decoration: none;
}
.nav a:hover {
  color: var(--accent);
}
.nav a.router-link-active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  padding: 8px;
  background: transparent;
  border: none;
}
.menu-toggle span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--ink);
  border-radius: 1px;
}

@media (max-width: 720px) {
  .menu-toggle {
    display: flex;
  }
  .nav {
    display: none;
    width: 100%;
    flex-direction: column;
    align-items: stretch;
    padding-bottom: 0.5rem;
  }
  .nav.open {
    display: flex;
  }
}
</style>
