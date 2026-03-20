<template>
  <div class="wrap">
    <audio
      ref="el"
      :src="currentSrc"
      preload="none"
      @ended="playing = false"
      @error="onError"
    />
    <button
      type="button"
      class="play"
      :class="{ playing }"
      :disabled="!candidates.length"
      :aria-label="playing ? '暂停' : '播放'"
      @click="toggle"
    >
      <span v-if="playing" class="ic">❚❚</span>
      <span v-else class="ic">▶</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { getDialectAudioSrcCandidates } from '@/utils/audioPaths'

const props = defineProps({
  item: { type: Object, required: true },
  side: { type: String, required: true }
})

const el = ref(null)
const playing = ref(false)
const candidateIdx = ref(0)

const candidates = computed(() => getDialectAudioSrcCandidates(props.item, props.side))

const currentSrc = computed(() => {
  const list = candidates.value
  const i = candidateIdx.value
  return list[i] || list[0] || ''
})

let globalStop = null
onMounted(() => {
  globalStop = () => {
    if (el.value) {
      el.value.pause()
      playing.value = false
    }
  }
  window.addEventListener('corpus-audio-stop', globalStop)
})
onUnmounted(() => {
  window.removeEventListener('corpus-audio-stop', globalStop)
})

watch(() => [props.item?.code, props.side], () => {
  candidateIdx.value = 0
  playing.value = false
})

function onError () {
  const list = candidates.value
  if (list.length < 2) return
  const next = candidateIdx.value + 1
  if (next >= list.length) return
  candidateIdx.value = next
  requestAnimationFrame(() => {
    el.value?.load()
    el.value?.play().catch(() => {})
  })
}

function toggle () {
  const a = el.value
  if (!a || !candidates.value.length) return

  if (a.paused) {
    window.dispatchEvent(new Event('corpus-audio-stop'))
    candidateIdx.value = 0
    nextTick(() => {
      a.load()
      a.play()
        .then(() => { playing.value = true })
        .catch(() => {
          alert('无法播放。请确认已放置 mp3，或文件名支持「空格 / 下划线」两种格式。')
        })
    })
  } else {
    a.pause()
    playing.value = false
  }
}
</script>

<style scoped>
.wrap {
  display: inline-flex;
  justify-content: center;
}

.play {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, transform 0.05s;
}
.play:hover:not(:disabled) {
  background: var(--accent-hover);
}
.play:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.play.playing {
  background: var(--gold);
}
.play:active:not(:disabled) {
  transform: scale(0.96);
}

.ic {
  font-size: 12px;
  letter-spacing: -2px;
  margin-left: 2px;
}
</style>
