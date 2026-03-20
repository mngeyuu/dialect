<template>
  <div class="audio-player">
    <button @click="togglePlay" class="play-button">
      <span v-if="isPlaying">⏸️</span>
      <span v-else>▶️</span>
    </button>
    <audio ref="audioElement" :src="src" @ended="onAudioEnded"></audio>
  </div>
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isPlaying: false
    };
  },
  methods: {
    togglePlay() {
      const audio = this.$refs.audioElement;

      if (this.isPlaying) {
        audio.pause();
      } else {
        audio.play();
      }

      this.isPlaying = !this.isPlaying;
    },
    onAudioEnded() {
      this.isPlaying = false;
    }
  }
};
</script>

<style scoped>
.audio-player {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden; /* 防止内容溢出 */
}

/* 隐藏原生 audio 控件 */
audio {
  display: none;
}

.play-button {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #4a90e2;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: background-color 0.3s ease;
}

.play-button:hover {
  background-color: #357ABD;
}
</style>
