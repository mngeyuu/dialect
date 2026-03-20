<template>
  <div class="page">
    <header class="page-head">
      <h1>搜索</h1>
      <p class="sub">在全文（词、老派、新派、记音）中模糊匹配</p>
    </header>

    <div class="search-bar card">
      <input
        v-model="q"
        type="search"
        placeholder="输入关键字，例如：太阳、日头、雨…"
        autocomplete="off"
        @keydown.enter.prevent
      />
      <span v-if="items.length" class="hint">{{ filtered.length }} / {{ items.length }} 条</span>
    </div>

    <div v-if="loading" class="card state">加载中…</div>
    <ul v-else class="results">
      <li v-for="row in filtered" :key="row.code" class="card hit">
        <div class="hit-top">
          <span class="code">{{ row.code }}</span>
          <strong>{{ row.word }}</strong>
        </div>
        <div class="hit-body">
          <div>
            <em>老派</em> {{ row.old_dialect_word || '—' }}
            <span v-if="row.old_dialect_phonetic" class="pho">〔{{ row.old_dialect_phonetic }}〕</span>
            <DualAudioButton :item="row" side="old" />
          </div>
          <div>
            <em>新派</em> {{ row.new_dialect_word || '—' }}
            <span v-if="row.new_dialect_phonetic" class="pho">〔{{ row.new_dialect_phonetic }}〕</span>
            <DualAudioButton :item="row" side="new" />
          </div>
        </div>
      </li>
    </ul>
    <p v-if="!loading && items.length && !filtered.length" class="empty card">无匹配结果</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { loadCorpus, normalizeItem } from '@/utils/corpusStore'
import DualAudioButton from '@/components/DualAudioButton.vue'

const loading = ref(true)
const items = ref([])
const q = ref('')

const filtered = computed(() => {
  const s = q.value.trim().toLowerCase()
  if (!s) return items.value
  return items.value.filter((row) => {
    const blob = [
      row.word,
      row.old_dialect_word,
      row.new_dialect_word,
      row.old_dialect_phonetic,
      row.new_dialect_phonetic,
      row.code
    ].filter(Boolean).join(' ').toLowerCase()
    return blob.includes(s)
  })
})

onMounted(async () => {
  const raw = await loadCorpus()
  items.value = raw.map(normalizeItem)
  loading.value = false
})
</script>

<style scoped>
.page-head {
  margin-bottom: 1.25rem;
}
.page-head h1 {
  margin: 0;
}
.sub {
  margin: 0.35rem 0 0;
  color: var(--ink-muted);
}

.search-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1.25rem;
}

.search-bar input {
  flex: 1;
  min-width: 200px;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 1rem;
  font-family: inherit;
}
.search-bar input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.hint {
  font-size: 0.875rem;
  color: var(--ink-muted);
}

.state {
  padding: 2rem;
  text-align: center;
}

.results {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.hit {
  padding: 1.1rem 1.25rem;
}

.hit-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.65rem;
}

.code {
  font-family: ui-monospace, monospace;
  font-size: 0.8rem;
  color: var(--gold);
  font-weight: 700;
}

.hit-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  font-size: 0.92rem;
  color: var(--ink-muted);
}

.hit-body em {
  font-style: normal;
  font-weight: 700;
  color: var(--accent);
  margin-right: 0.35rem;
}

.hit-body > div:nth-child(2) em {
  color: var(--gold);
}

.hit-body > div {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}

.pho {
  font-size: 0.85em;
  opacity: 0.9;
}

@media (max-width: 640px) {
  .hit-body {
    grid-template-columns: 1fr;
  }
}

.empty {
  padding: 2rem;
  text-align: center;
  color: var(--ink-muted);
}
</style>
