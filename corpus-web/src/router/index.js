import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue'), meta: { title: '首页' } },
  { path: '/corpus', name: 'corpus', component: () => import('@/views/CorpusView.vue'), meta: { title: '语料库' } },
  { path: '/search', name: 'search', component: () => import('@/views/SearchView.vue'), meta: { title: '搜索' } },
  { path: '/about', name: 'about', component: () => import('@/views/AboutView.vue'), meta: { title: '关于' } }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior () {
    return { top: 0 }
  }
})

router.afterEach((to) => {
  const t = to.meta.title
  document.title = t ? `${t} · 方言语料库` : '方言语料库'
})

export default router
