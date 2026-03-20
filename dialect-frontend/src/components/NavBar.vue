<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <router-link to="/" class="logo">
        <span class="logo-text">方言词汇语料库</span>
        <span class="logo-sub">伊川 · 中原官话</span>
      </router-link>
      <ul class="nav-links">
        <li><router-link to="/" active-class="active" exact-active-class="active">首页</router-link></li>
        <li><router-link to="/Search" active-class="active">搜索</router-link></li>
        <li><router-link to="/data" active-class="active">数据库</router-link></li>
        <li><router-link to="/import" active-class="active">导入</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #c82704 0%, #ac2103 100%);
  color: #fff;
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
  font-family: var(--font-nav);
}

.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-decoration: none;
  color: #fff;
  gap: 2px;
}

.logo:hover {
  text-decoration: none;
  opacity: 0.95;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.logo-sub {
  font-size: 0.75rem;
  opacity: 0.88;
  letter-spacing: 0.08em;
}

.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 4px;
}

.nav-links a {
  color: rgba(255, 255, 255, 0.95);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  transition: background 0.2s, color 0.2s;
}

.nav-links a:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  text-decoration: none;
}

.nav-links a.active {
  background: rgba(255, 255, 255, 0.22);
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}
</style>
