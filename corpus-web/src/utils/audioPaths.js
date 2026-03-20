/**
 * 录音 URL：支持「空格 / 下划线」两种文件名；GitHub Pages base；可选 JSON 自定义字段。
 */

function publicBase () {
  const base = import.meta.env.BASE_URL || './'
  return base.endsWith('/') ? base : `${base}/`
}

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

function urlForFolderAndFilename (folderRel, filename) {
  return publicBase() + encodePathSegments(`${folderRel}/${filename}`)
}

function isAudioFilePath (p) {
  const pure = String(p || '').split('#')[0].split('?')[0]
  return /\.(mp3|wav|ogg|m4a)$/i.test(pure)
}

export function getDialectAudioSrcCandidates (item, side) {
  if (!item || !item.code || !item.word) return []

  const custom = (side === 'old'
    ? (item.old_dialect_audio || '')
    : (item.new_dialect_audio || '')
  ).trim()

  if (custom) {
    if (/^(https?:|data:|blob:)/i.test(custom) && isAudioFilePath(custom)) return [custom]
    if (isAudioFilePath(custom)) {
      const rel = custom.replace(/^\.\//, '')
      return [publicBase() + encodePathSegments(rel)]
    }
  }

  const code = formatDialectCode(item.code)
  const tag = side === 'old' ? '老派' : '新派'
  const folder = side === 'old' ? 'audio/old_dialect' : 'audio/new_dialect'

  return defaultFilenameVariants(code, tag, item.word).map((filename) =>
    urlForFolderAndFilename(folder, filename)
  )
}

export function getDialectAudioSrc (item, side) {
  const list = getDialectAudioSrcCandidates(item, side)
  return list[0] || ''
}
