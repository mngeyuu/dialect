<template>
  <div class="home">
    <section class="hero card">
      <div class="hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">口述传统 · 方言记录</p>
          <h1>听见乡土里的<br /><span class="hl">老派与新派</span></h1>
          <p class="lead">
            本站点汇集普通话词条与方言对应说法，配套记音与录音。图文介绍项目背景，音频随条目标注，支持静态部署与离线浏览。
          </p>
          <div class="cta">
            <router-link to="/corpus" class="btn btn-primary">进入语料库</router-link>
            <router-link to="/search" class="btn btn-ghost">快速搜索</router-link>
          </div>
          <ul class="stats">
            <li><strong>{{ count }}</strong><span>条词条（已加载）</span></li>
            <li><strong>双轨</strong><span>老派 / 新派对照</span></li>
            <li><strong>mp3</strong><span>本地或 CDN 均可</span></li>
          </ul>
        </div>
        <div class="hero-visual">
          <img src="/images/hero.svg" alt="水墨风格的日与山峦插画，象征方言与天地人文" width="480" height="360" />
        </div>
      </div>
    </section>

    <section class="features">
      <article class="feature card">
        <img src="/images/icon-text.svg" alt="" width="56" height="56" class="feat-ic" />
        <h2>文字与结构</h2>
        <p>每条含编号、普通话词、老派/新派词汇与可选记音字段。数据来自 <code>public/data/corpus.json</code>，可整库替换。</p>
      </article>
      <article class="feature card">
        <img src="/images/icon-audio.svg" alt="" width="56" height="56" class="feat-ic" />
        <h2>语音播放</h2>
        <p>自动尝试「0001 新派 词.mp3」与「0001_新派_词.mp3」两种文件名，兼容历史录音命名。</p>
      </article>
      <article class="feature card">
        <img src="/images/icon-map.svg" alt="" width="56" height="56" class="feat-ic" />
        <h2>静态部署</h2>
        <p>使用 Hash 路由，适合 GitHub Pages；构建产物内含图片、JSON 与音频目录，无需后端。</p>
      </article>
    </section>

    <section class="banner card">
      <div class="banner-inner">
        <img src="/images/banner-wave.svg" alt="" class="wave" width="120" height="80" />
        <div>
          <h2>如何加入录音？</h2>
          <p>将 mp3 放入 <code>public/audio/old_dialect</code> 与 <code>public/audio/new_dialect</code>，文件名与语料中「词汇」一致即可在页面一键播放。</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadCorpus } from '@/utils/corpusStore'

const count = ref(0)
onMounted(async () => {
  const list = await loadCorpus()
  count.value = list.length
})
</script>

<style scoped>
.home {
  padding-top: 0.5rem;
}

.hero {
  overflow: hidden;
  margin-bottom: 1.75rem;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
  padding: 1.5rem 1.5rem 1.5rem 2rem;
}

@media (max-width: 900px) {
  .hero-grid {
    grid-template-columns: 1fr;
    padding: 1.25rem;
  }
  .hero-visual {
    order: -1;
    text-align: center;
  }
  .hero-visual img {
    max-width: 100%;
    height: auto;
  }
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
  color: var(--gold);
  font-weight: 700;
  margin: 0 0 0.5rem;
}

h1 {
  font-size: clamp(1.75rem, 4vw, 2.35rem);
  margin: 0 0 1rem;
}

.hl {
  color: var(--accent);
}

.lead {
  color: var(--ink-muted);
  margin: 0 0 1.25rem;
  max-width: 36ch;
}

.cta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.cta a {
  text-decoration: none;
}

.stats {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem 2rem;
  font-size: 0.875rem;
  color: var(--ink-muted);
}

.stats li {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.stats strong {
  font-size: 1.25rem;
  color: var(--ink);
  font-family: var(--font-display);
}

.hero-visual img {
  display: block;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.75rem;
}

@media (max-width: 900px) {
  .features {
    grid-template-columns: 1fr;
  }
}

.feature {
  padding: 1.35rem 1.25rem;
}

.feature h2 {
  font-size: 1.1rem;
  margin: 0.5rem 0 0.5rem;
}

.feature p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--ink-muted);
}

.feat-ic {
  display: block;
}

.banner {
  padding: 1.5rem 1.75rem;
  background: linear-gradient(135deg, var(--gold-soft), var(--accent-soft));
  border-color: var(--border);
}

.banner-inner {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.banner h2 {
  margin: 0 0 0.35rem;
  font-size: 1.2rem;
}

.banner p {
  margin: 0;
  color: var(--ink-muted);
  font-size: 0.95rem;
}

code {
  font-size: 0.85em;
  background: rgba(255, 255, 255, 0.7);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}

@media (max-width: 600px) {
  .banner-inner {
    flex-direction: column;
    text-align: center;
  }
}
</style>
