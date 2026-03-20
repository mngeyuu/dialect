/**
 * 方言录音 URL：与 public/audio 目录命名约定一致，兼容 GitHub Pages BASE_URL 与 Electron。
 * 若 JSON 中 old_dialect_audio / new_dialect_audio 非空，优先使用该字段（相对路径会拼在站点根下）。
 */

function publicBase () {
  const base = process.env.BASE_URL || './'
  return base.endsWith('/') ? base : `${base}/`
}

/** 对路径每一段做 encodeURIComponent，避免中文、空格导致 404 */
export function encodePathSegments (relPath) {
  if (!relPath) return ''
  return relPath
    .split('/')
    .filter(Boolean)
    .map((seg) => encodeURIComponent(seg))
    .join('/')
}

export function formatDialectCode (code) {
  const n = parseInt(String(code), 10)
  if (Number.isNaN(n)) return String(code)
  return String(n).padStart(4, '0')
}

function isElectron () {
  return typeof window !== 'undefined' && !!window.electronAPI
}

function urlForFolderAndFilename (folderRel, filename) {
  if (isElectron()) {
    return `${folderRel}/${filename}`
  }
  return publicBase() + encodePathSegments(`${folderRel}/${filename}`)
}

/**
 * 默认命名候选：
 * 1) 空格分隔优先，其次下划线；
 * 2) 扩展名优先 .mp3，其次 .MP3（兼容历史文件）。
 */
function defaultFilenameVariants (code, tag, word) {
  const stems = [`${code} ${tag} ${word}`, `${code}_${tag}_${word}`]
  const exts = ['.mp3', '.MP3']
  const out = []
  for (const stem of stems) {
    for (const ext of exts) {
      out.push(`${stem}${ext}`)
    }
  }
  return Array.from(new Set(out))
}

/**
 * 所有候选 URL（先空格后下划线）。自定义 old_dialect_audio 时仅一项。
 * @param {object} item
 * @param {'old'|'new'} side
 * @returns {string[]}
 */
export function getDialectAudioSrcCandidates (item, side) {
  if (!item || !item.code || !item.word) return []

  const custom = (side === 'old'
    ? (item.old_dialect_audio || '')
    : (item.new_dialect_audio || '')
  ).trim()

  if (custom) {
    if (/^(https?:|data:|blob:)/i.test(custom)) {
      return [custom]
    }
    if (isElectron()) {
      return [custom.replace(/^\.\//, '')]
    }
    const rel = custom.replace(/^\.\//, '')
    return [publicBase() + encodePathSegments(rel)]
  }

  const code = formatDialectCode(item.code)
  const tag = side === 'old' ? '老派' : '新派'
  const folderWeb = side === 'old' ? 'audio/old_dialect' : 'audio/new_dialect'
  const folderEl = side === 'old' ? 'old_dialect' : 'new_dialect'
  const folder = isElectron() ? folderEl : folderWeb

  return defaultFilenameVariants(code, tag, item.word).map((filename) =>
    urlForFolderAndFilename(folder, filename)
  )
}

/**
 * @param {object} item
 * @param {'old'|'new'} side
 * @returns {string} 可直接赋给 <audio src>（首选：空格命名）
 */
export function getDialectAudioSrc (item, side) {
  const list = getDialectAudioSrcCandidates(item, side)
  return list[0] || ''
}
