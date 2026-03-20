import { createRouter, createWebHashHistory } from 'vue-router'; // ✅ 确保正确引入
import SearchPage from '../views/SearchPage.vue';
import DataPage from '../views/DataPage.vue';
import ImportPage from '../views/ImportPage.vue';
import HomePage from '../views/HomePage.vue'

const routes = [
  {
    path: '/Search',
    name: 'Search',
    component: SearchPage
  },
  {
    path: '/data',
    name: 'Data',
    component: DataPage
  },
  {
    path: '/import',
    name: 'Import',
    component: ImportPage
  },
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
];

const router = createRouter({
  history: createWebHashHistory(), // ✅ 使用 Hash 模式
  routes,
});

export default router;
