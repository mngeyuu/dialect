import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/theme.css'
import { loadStaticCorpusIntoStorage } from './utils/staticCorpus'

async function bootstrap () {
  await loadStaticCorpusIntoStorage()
  const app = createApp(App)
  app.use(router)
  app.mount('#app')
}

bootstrap()