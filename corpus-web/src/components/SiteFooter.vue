<template>
  <footer class="footer">
    <div class="footer-inner">
      <p>方言语料库 · 仅供学术与文化记录使用</p>
      <p class="muted">语音文件请置于 <code>public/audio/</code> 并与词条命名一致</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: auto;
  padding: 2rem 1.25rem;
  border-top: 1px solid var(--border);
  background: var(--bg-card);
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  font-size: 0.875rem;
  color: var(--ink-muted);
}

.footer-inner p {
  margin: 0.35rem 0;
}

.muted {
  font-size: 0.8rem;
}

code {
  font-size: 0.85em;
  background: var(--gold-soft);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}
</style>
