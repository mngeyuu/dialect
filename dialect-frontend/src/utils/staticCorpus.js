/**
 * GitHub Pages 等纯静态部署：从 public/data/dialect-words.json 拉取语料，
 * 写入 localStorage（与「数据库 / 搜索」页现有逻辑一致）。
 * 音频文件需放在 public/audio/old_dialect、public/audio/new_dialect，命名与前端一致。
 */

const STORAGE_KEY = 'dialectWords'

function resolveCorpusUrl () {
  const base = process.env.BASE_URL || './'
  // 保证拼接成 ./data/... 或 /repo/data/...
  const prefix = base.endsWith('/') ? base : `${base}/`
  return `${prefix}data/dialect-words.json`
}

function normalizeItem (item, index) {
  return {
    id: item.id ?? index + 1,
    code: item.code != null ? String(item.code) : String(index + 1),
    word: item.word || '',
    old_dialect_word: item.old_dialect_word || '',
    old_dialect_phonetic: item.old_dialect_phonetic || '',
    old_dialect_audio: item.old_dialect_audio || '',
    new_dialect_word: item.new_dialect_word || '',
    new_dialect_phonetic: item.new_dialect_phonetic || '',
    new_dialect_audio: item.new_dialect_audio || ''
  }
}

function normalizeList (data) {
  if (Array.isArray(data)) {
    return data.map((item, i) => normalizeItem(item, i))
  }
  if (data && Array.isArray(data.results)) {
    return data.results.map((item, i) => normalizeItem(item, i))
  }
  return null
}

/**
 * @returns {Promise<boolean>} 是否成功从静态文件加载并写入 localStorage
 */
export async function loadStaticCorpusIntoStorage () {
  const url = resolveCorpusUrl()
  try {
    const res = await fetch(url, { cache: 'no-cache' })
    if (!res.ok) {
      return false
    }
    const data = await res.json()
    const list = normalizeList(data)
    if (!list) {
      return false
    }
    // 空数组不写入，避免覆盖用户本机已导入的数据（仓库占位 [] 时）
    if (list.length === 0) {
      return false
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list))
    return true
  } catch (e) {
    console.warn('[staticCorpus] 未加载静态语料（可忽略，将使用本地已导入数据）:', e.message)
    return false
  }
}
