<template>
  <div class="page">
    <header class="page-head">
      <h1>语料库</h1>
      <p class="sub">分页浏览，点击圆钮播放老派 / 新派录音</p>
    </header>

    <div v-if="loading" class="card state">加载语料中…</div>
    <div v-else-if="!items.length" class="card state">
      暂无数据。请将 <code>corpus.json</code> 放入 <code>public/data/</code> 后重新构建。
    </div>

    <template v-else>
      <div class="toolbar card">
        <label>每页 <select v-model.number="pageSize">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select> 条</label>
        <span class="meta">共 {{ items.length }} 条 · 第 {{ page }} / {{ totalPages }} 页</span>
        <div class="pager">
          <button type="button" class="btn btn-ghost" :disabled="page <= 1" @click="page--">上一页</button>
          <button type="button" class="btn btn-ghost" :disabled="page >= totalPages" @click="page++">下一页</button>
        </div>
      </div>

      <div class="cards-mobile">
        <article v-for="row in pageRows" :key="row.code" class="card row-card">
          <div class="row-head">
            <span class="code">{{ row.code }}</span>
            <span class="word">{{ row.word }}</span>
          </div>
          <div class="pair">
            <div>
              <span class="tag old">老派</span>
              <p>{{ row.old_dialect_word || '—' }}</p>
              <DualAudioButton :item="row" side="old" />
            </div>
            <div>
              <span class="tag new">新派</span>
              <p>{{ row.new_dialect_word || '—' }}</p>
              <DualAudioButton :item="row" side="new" />
            </div>
          </div>
        </article>
      </div>

      <div class="table-wrap card">
        <table class="desk-table">
          <thead>
            <tr>
              <th>编号</th>
              <th>词汇</th>
              <th>老派</th>
              <th>老派音</th>
              <th>新派</th>
              <th>新派音</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in pageRows" :key="'t-' + row.code">
              <td>{{ row.code }}</td>
              <td class="w">{{ row.word }}</td>
              <td>{{ row.old_dialect_word }}</td>
              <td><DualAudioButton :item="row" side="old" /></td>
              <td>{{ row.new_dialect_word }}</td>
              <td><DualAudioButton :item="row" side="new" /></td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { loadCorpus, normalizeItem } from '@/utils/corpusStore'
import DualAudioButton from '@/components/DualAudioButton.vue'

const loading = ref(true)
const items = ref([])
const page = ref(1)
const pageSize = ref(20)

const totalPages = computed(() => Math.max(1, Math.ceil(items.value.length / pageSize.value)))

const pageRows = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return items.value.slice(start, start + pageSize.value)
})

watch(pageSize, () => { page.value = 1 })

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
  font-size: 1.75rem;
}
.sub {
  margin: 0.35rem 0 0;
  color: var(--ink-muted);
  font-size: 0.95rem;
}

.state {
  padding: 2rem;
  text-align: center;
  color: var(--ink-muted);
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  margin-bottom: 1rem;
}

.toolbar select {
  margin: 0 0.35rem;
  padding: 0.35rem 0.5rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  font-family: inherit;
}

.meta {
  flex: 1;
  font-size: 0.875rem;
  color: var(--ink-muted);
}

.pager {
  display: flex;
  gap: 0.5rem;
}

.cards-mobile {
  display: none;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.row-card {
  padding: 1rem 1.15rem;
}
.row-head {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}
.code {
  font-family: ui-monospace, monospace;
  font-size: 0.85rem;
  color: var(--gold);
  font-weight: 700;
}
.word {
  font-weight: 700;
  font-size: 1.05rem;
}
.pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.tag {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.tag.old { color: var(--accent); }
.tag.new { color: var(--gold); }
.pair p {
  margin: 0.25rem 0 0.5rem;
  font-size: 0.9rem;
}

.table-wrap {
  overflow-x: auto;
  padding: 0;
}

.desk-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
.desk-table th,
.desk-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  text-align: left;
  vertical-align: middle;
}
.desk-table th {
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 700;
  white-space: nowrap;
}
.desk-table .w {
  font-weight: 600;
}

@media (max-width: 768px) {
  .table-wrap {
    display: none;
  }
  .cards-mobile {
    display: flex;
  }
}
</style>
