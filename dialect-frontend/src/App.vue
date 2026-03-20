<template>
  <div id="app">
    <nav-bar />
    <main class="app-main">
      <router-view/>
    </main>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
/* ========== 设计变量：大红色主色 ========== */
:root {
  --color-bg: #f8f4f2;
  --color-bg-card: #ffffff;
  --color-primary: #c82704;
  --color-primary-hover: #a71f03;
  --color-primary-light: rgba(200, 39, 4, 0.08);
  --color-accent: #c82704;
  --color-accent-soft: rgba(200, 39, 4, 0.12);
  --color-text: #2c2c2c;
  --color-text-secondary: #5c5c5c;
  --color-border: #e8e2da;
  --color-border-strong: #d4ccc0;
  --shadow-sm: 0 1px 3px rgba(200, 39, 4, 0.06);
  --shadow-md: 0 4px 12px rgba(200, 39, 4, 0.08);
  --shadow-lg: 0 8px 24px rgba(200, 39, 4, 0.1);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --font-sans: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  --font-serif: "Noto Serif SC", "Source Han Serif SC", "SimSun", serif;
  --font-nav: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--color-text);
  line-height: 1.6;
  background: var(--color-bg);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  padding: 24px 20px 40px;
}

h1, h2, h3, h4, h5, h6 {
  margin-bottom: 0.5em;
  color: var(--color-text);
  font-weight: 600;
}

h1 {
  font-size: 1.75rem;
  margin-bottom: 1rem;
  color: var(--color-primary);
  font-family: var(--font-serif);
}

h2 {
  font-size: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.35rem;
  border-bottom: 2px solid var(--color-primary-light);
}

button {
  cursor: pointer;
  font-family: inherit;
}

input, select, textarea {
  font-family: inherit;
  font-size: inherit;
}

a {
  color: var(--color-primary);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
