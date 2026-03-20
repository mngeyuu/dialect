<template>
  <div class="page">
    <header class="page-head">
      <h1>关于本站</h1>
      <p class="sub">国创 / 校创方言语料数字化展示（示例站）</p>
    </header>

    <div class="grid">
      <article class="card prose">
        <h2>项目说明</h2>
        <p>
          本站从零使用 <strong>Vite + Vue 3</strong> 构建，与旧版工程相互独立，目录为仓库内 <code>corpus-web/</code>。
          页面包含<strong>首页图文</strong>、<strong>语料分页</strong>、<strong>全文搜索</strong>与<strong>双轨音频</strong>（老派 / 新派）。
        </p>
        <p>
          文本数据位于 <code>public/data/corpus.json</code>；配图为 <code>public/images/</code> 下 SVG；
          录音放在 <code>public/audio/old_dialect</code> 与 <code>public/audio/new_dialect</code>，构建后随静态资源一并发布。
        </p>
        <h2>技术要点</h2>
        <ul>
          <li>Hash 路由（<code>#/</code>），适配 GitHub Pages 子路径</li>
          <li><code>base: './'</code> 相对资源路径</li>
          <li>语料拉取成功后写入 <code>localStorage</code> 作离线缓存</li>
          <li>音频文件名自动尝试空格版与下划线版</li>
        </ul>
      </article>
      <aside class="card aside">
        <img src="/images/about-side.svg" alt="线装书与声波装饰图" width="280" height="200" class="side-img" />
        <h3>替换资源</h3>
        <ol>
          <li>用完整语料覆盖 <code>corpus.json</code></li>
          <li>按命名规则放入 mp3</li>
          <li>运行 <code>npm run build</code></li>
        </ol>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.page-head {
  margin-bottom: 1.5rem;
}
.page-head h1 {
  margin: 0;
}

.sub {
  color: var(--ink-muted);
  margin: 0.35rem 0 0;
}

.grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 1.25rem;
  align-items: start;
}

@media (max-width: 800px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

.prose {
  padding: 1.5rem 1.75rem;
}

.prose h2 {
  font-size: 1.15rem;
  margin: 1.25rem 0 0.5rem;
}
.prose h2:first-child {
  margin-top: 0;
}

.prose p,
.prose li {
  color: var(--ink-muted);
  font-size: 0.95rem;
}

.prose ul {
  padding-left: 1.25rem;
}

code {
  font-size: 0.88em;
  background: var(--gold-soft);
  padding: 0.12rem 0.4rem;
  border-radius: 4px;
}

.aside {
  padding: 1.5rem;
  text-align: center;
}

.side-img {
  max-width: 100%;
  height: auto;
  margin-bottom: 1rem;
}

.aside h3 {
  margin: 0 0 0.5rem;
  font-size: 1.05rem;
}

.aside ol {
  text-align: left;
  color: var(--ink-muted);
  font-size: 0.9rem;
  padding-left: 1.2rem;
  margin: 0;
}
</style>
