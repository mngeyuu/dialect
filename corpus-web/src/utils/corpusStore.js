const STORAGE_KEY = 'corpus_words_v2'
const DATA_URL = `${import.meta.env.BASE_URL}data/corpus.json`.replace(/([^:]\/)\/+/g, '$1')

let cache = null

export function getCachedList () {
  if (cache) return cache
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const data = JSON.parse(raw)
      if (Array.isArray(data) && data.length) {
        cache = data
        return cache
      }
    }
  } catch (_) {}
  return null
}

export function setCache (list) {
  if (!Array.isArray(list) || !list.length) return
  cache = list
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list))
  } catch (_) {}
}

export async function loadCorpus () {
  const existing = getCachedList()
  try {
    const res = await fetch(DATA_URL, { cache: 'no-cache' })
    if (!res.ok) throw new Error(String(res.status))
    const data = await res.json()
    const list = Array.isArray(data) ? data : (data.results || [])
    if (list.length) {
      setCache(list)
      return list
    }
  } catch (e) {
    console.warn('[corpus] 拉取 corpus.json 失败，使用本地缓存', e.message)
  }
  return existing || []
}

export function normalizeItem (item, index) {
  return {
    id: item.id ?? index + 1,
    code: item.code != null ? String(item.code) : String(index + 1).padStart(4, '0'),
    word: item.word || '',
    old_dialect_word: item.old_dialect_word || '',
    old_dialect_phonetic: item.old_dialect_phonetic || '',
    old_dialect_audio: item.old_dialect_audio || '',
    new_dialect_word: item.new_dialect_word || '',
    new_dialect_phonetic: item.new_dialect_phonetic || '',
    new_dialect_audio: item.new_dialect_audio || ''
  }
}
