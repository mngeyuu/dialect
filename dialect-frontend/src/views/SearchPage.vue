<template>
  <div class="search-container">
    <div class="page-header">
      <h1>方言词汇搜索</h1>
      <p class="page-desc">在语料库中按词汇、老派/新派检索</p>
    </div>

    <div class="card search-card">
      <div class="search-mode-toggle">
        <button
          :class="{ active: searchMode === 'basic' }"
          @click="searchMode = 'basic'">基本搜索</button>
        <button
          :class="{ active: searchMode === 'advanced' }"
          @click="searchMode = 'advanced'">高级搜索</button>
      </div>

      <!-- 基本搜索 -->
      <div v-if="searchMode === 'basic'" class="search-form basic">
        <input
          v-model="basicSearchTerm"
          @keyup.enter="performBasicSearch"
          placeholder="输入词汇或老派/新派说法...">
        <button class="btn-primary" @click="performBasicSearch">搜索</button>
      </div>

      <!-- 高级搜索 -->
      <div v-else class="search-form advanced">
        <div class="form-row">
          <div class="form-group">
            <label>词汇</label>
            <input v-model="advancedSearch.word" placeholder="普通话词汇">
          </div>
          <div class="form-group">
            <label>老派词汇</label>
            <input v-model="advancedSearch.oldDialect" placeholder="老派说法">
          </div>
          <div class="form-group">
            <label>新派词汇</label>
            <input v-model="advancedSearch.newDialect" placeholder="新派说法">
          </div>
        </div>
        <button class="btn-primary" @click="performAdvancedSearch">高级搜索</button>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div class="search-results card">
      <h2>搜索结果 <span class="badge">{{ searchResults.length }}</span></h2>
      <div v-if="searchResults.length > 0" class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>编号</th>
            <th>词汇</th>
            <th>老派词汇</th>
            <th>老派语音</th>
            <th>新派词汇</th>
            <th>新派语音</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in searchResults" :key="item.id || item.code">
            <td>{{ item.code }}</td>
            <td>{{ item.word }}</td>
            <td>{{ item.old_dialect_word }}</td>
            <td class="audio-cell">
              <div v-if="item.word" class="audio-button-wrapper">
                <audio
                  :ref="el => setAudioRef(`old_audio_${item.code}`, el)"
                  :src="getAudioSrcFor(item, 'old')"
                  preload="none"
                  @ended="handleAudioEnded(`old_audio_${item.code}`)"
                  @error="onDialectAudioError(item, 'old', `old_audio_${item.code}`)">
                </audio>
                <button
                  class="play-button"
                  @click="togglePlay(`old_audio_${item.code}`, item, 'old')"
                  :class="{ 'playing': isPlaying[`old_audio_${item.code}`] }">
                  <span v-if="isPlaying[`old_audio_${item.code}`]" class="material-icons">pause</span>
                  <span v-else class="material-icons">play_arrow</span>
                </button>
              </div>
              <span v-else>无音频</span>
            </td>
            <td>{{ item.new_dialect_word }}</td>
            <td class="audio-cell">
              <div v-if="item.word" class="audio-button-wrapper">
                <audio
                  :ref="el => setAudioRef(`new_audio_${item.code}`, el)"
                  :src="getAudioSrcFor(item, 'new')"
                  preload="none"
                  @ended="handleAudioEnded(`new_audio_${item.code}`)"
                  @error="onDialectAudioError(item, 'new', `new_audio_${item.code}`)">
                </audio>
                <button
                  class="play-button"
                  @click="togglePlay(`new_audio_${item.code}`, item, 'new')"
                  :class="{ 'playing': isPlaying[`new_audio_${item.code}`] }">
                  <span v-if="isPlaying[`new_audio_${item.code}`]" class="material-icons">pause</span>
                  <span v-else class="material-icons">play_arrow</span>
                </button>
              </div>
              <span v-else>无音频</span>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
      <div v-else class="no-results">
        <p>没有找到匹配的结果</p>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { getDialectAudioSrcCandidates } from '@/utils/audioPaths'

export default {
  data() {
    return {
      searchMode: 'basic',
      basicSearchTerm: '',
      advancedSearch: {
        word: '',
        oldDialect: '',
        newDialect: ''
      },
      searchResults: [],
      allData: [],
      isLoading: false,
      isPlaying: {},   // 用于跟踪每个音频的播放状态
      audioRefs: {},   // 用于存储音频引用
      /** 同一词条先试空格命名、失败再试下划线命名：'old_0001' -> 候选下标 */
      audioCandidateIdx: {}
    };
  },
  mounted() {
    // 加载本地数据
    this.loadLocalData();

    // 加载Material Icons图标字体
    this.loadMaterialIcons();

    // 设置后备字体
    this.setupFallbackFonts();
  },
  methods: {
    // 设置音频引用
    setAudioRef(key, el) {
      if (el) {
        this.audioRefs[key] = el;
      }
    },

    // 加载Material Icons字体
    loadMaterialIcons() {
      if (!document.querySelector('link[href*="Material+Icons"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons';
        document.head.appendChild(link);
      }
    },

    audioSideKey (item, side) {
      return `${side}_${item.code}`
    },

    getAudioSrcFor (item, side) {
      const list = getDialectAudioSrcCandidates(item, side)
      const k = this.audioSideKey(item, side)
      const idx = this.audioCandidateIdx[k] ?? 0
      return list[idx] || list[0] || ''
    },

    /** 空格版 404 时自动改试下划线版（如前 15 条历史命名） */
    onDialectAudioError (item, side, audioKey) {
      const list = getDialectAudioSrcCandidates(item, side)
      if (list.length < 2) return
      const k = this.audioSideKey(item, side)
      const idx = this.audioCandidateIdx[k] ?? 0
      if (idx + 1 >= list.length) {
        const el = this.audioRefs[audioKey]
        const src = el ? (el.currentSrc || el.src || '(无地址)') : '(无地址)'
        alert(
          '无法播放该条录音。\n\n' +
          '已尝试空格/下划线与 .mp3/.MP3 组合。\n' +
          '请检查该文件是否已上传并可访问。\n\n' +
          `当前请求地址：\n${src}`
        )
        return
      }
      this.audioCandidateIdx[k] = idx + 1
      this.$nextTick(() => {
        const el = this.audioRefs[audioKey]
        if (!el) return
        el.load()
        el.play().catch(() => {})
      })
    },

    // 切换音频播放状态
    togglePlay (audioKey, item, side) {
      // 停止所有其他音频
      Object.keys(this.audioRefs).forEach(key => {
        if (key !== audioKey && this.audioRefs[key]) {
          this.audioRefs[key].pause();
          this.isPlaying[key] = false;
        }
      });

      // 获取当前音频元素
      const audioElement = this.audioRefs[audioKey];
      if (!audioElement) return;

      // 切换播放状态
      if (audioElement.paused) {
        const k = this.audioSideKey(item, side)
        delete this.audioCandidateIdx[k]
        this.$nextTick(() => {
          audioElement.load()
          const playPromise = audioElement.play();
          if (playPromise !== undefined) {
            playPromise.then(() => {
              this.isPlaying[audioKey] = true;
            }).catch((error) => {
              // 首个候选失败时不立即弹错，等待 onerror 自动回退下一个候选
              console.warn('播放候选失败，准备回退下一候选:', error)
            });
          }
        })
      } else {
        audioElement.pause();
        this.isPlaying[audioKey] = false;
      }
    },

    // 处理音频播放结束事件
    handleAudioEnded(audioKey) {
      this.isPlaying[audioKey] = false;
    },

    // 设置后备字体
    setupFallbackFonts() {
      // 添加字体选择器
      const style = document.createElement('style');
      style.textContent = `
        .phonetic {
          font-family: 'Arial Unicode MS', 'Lucida Sans Unicode', 'Noto Sans', 'DejaVu Sans', Arial, sans-serif;
        }
      `;
      document.head.appendChild(style);
    },


    // 从本地存储加载数据
    loadLocalData() {
      try {
        const savedData = localStorage.getItem('dialectWords');
        if (savedData) {
          this.allData = JSON.parse(savedData);
        } else {
          console.log('本地存储中没有找到数据');
        }
      } catch (error) {
        console.error('加载本地数据失败:', error);
      }
    },

    // 基本搜索方法
    performBasicSearch() {
      if (!this.basicSearchTerm.trim()) {
        this.searchResults = [];
        return;
      }

      const searchTerm = this.basicSearchTerm.toLowerCase().trim();

      this.searchResults = this.allData.filter(item => {
        return (
          (item.word && item.word.toLowerCase().includes(searchTerm)) ||
          (item.old_dialect_word && item.old_dialect_word.toLowerCase().includes(searchTerm)) ||
          (item.new_dialect_word && item.new_dialect_word.toLowerCase().includes(searchTerm))
        );
      });
    },

    // 高级搜索方法
    performAdvancedSearch() {
      // 如果所有字段都为空，清空结果
      if (!this.advancedSearch.word && !this.advancedSearch.oldDialect && !this.advancedSearch.newDialect) {
        this.searchResults = [];
        return;
      }

      this.searchResults = this.allData.filter(item => {
        // 检查每个搜索条件，如果有条件但数据不匹配则跳过
        if (this.advancedSearch.word &&
            (!item.word || !item.word.toLowerCase().includes(this.advancedSearch.word.toLowerCase()))) {
          return false;
        }

        if (this.advancedSearch.oldDialect &&
            (!item.old_dialect_word || !item.old_dialect_word.toLowerCase().includes(this.advancedSearch.oldDialect.toLowerCase()))) {
          return false;
        }

        if (this.advancedSearch.newDialect &&
            (!item.new_dialect_word || !item.new_dialect_word.toLowerCase().includes(this.advancedSearch.newDialect.toLowerCase()))) {
          return false;
        }

        return true;
      });
    }
  }
};
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-desc {
  color: var(--color-text-secondary);
  font-size: 0.95rem;
  margin-top: 4px;
}

.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  padding: 24px;
  margin-bottom: 24px;
}

.search-card {
  margin-bottom: 28px;
}

.search-mode-toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.search-mode-toggle button {
  padding: 10px 20px;
  border: 1px solid var(--color-border-strong);
  background: var(--color-bg);
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.search-mode-toggle button:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.search-mode-toggle button.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

.search-form.basic {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-form.basic input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 1rem;
  transition: border-color 0.2s;
}

.search-form.basic input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-text);
}

.form-group input {
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.btn-primary {
  padding: 12px 24px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.02s;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
}

.btn-primary:active {
  transform: scale(0.98);
}

.search-results h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 26px;
  height: 26px;
  padding: 0 8px;
  background: var(--color-accent-soft);
  color: var(--color-accent);
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
}

.table-wrap {
  overflow-x: auto;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  table-layout: fixed;
}

.data-table th,
.data-table td {
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.data-table th {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: 600;
  white-space: nowrap;
}

/* 语音列表头与内容居中，避免和按钮列错位 */
.data-table th:nth-child(4),
.data-table th:nth-child(6),
.data-table td:nth-child(4),
.data-table td:nth-child(6) {
  text-align: center;
}

.data-table th:nth-child(1),
.data-table td:nth-child(1) { width: 90px; }
.data-table th:nth-child(2),
.data-table td:nth-child(2) { width: 180px; }
.data-table th:nth-child(3),
.data-table td:nth-child(3) { width: 220px; }
.data-table th:nth-child(4),
.data-table td:nth-child(4) { width: 110px; }
.data-table th:nth-child(5),
.data-table td:nth-child(5) { width: 220px; }
.data-table th:nth-child(6),
.data-table td:nth-child(6) { width: 110px; }

.data-table td:nth-child(2),
.data-table td:nth-child(3),
.data-table td:nth-child(5) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.data-table tbody tr {
  transition: background 0.15s;
}

.data-table tbody tr:hover {
  background: var(--color-primary-light);
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.no-results {
  text-align: center;
  padding: 48px 24px;
  color: var(--color-text-secondary);
  background: var(--color-primary-light);
  border-radius: var(--radius-sm);
}

.phonetic {
  font-size: 1em;
  letter-spacing: 0.03em;
  color: var(--color-text-secondary);
}

.audio-cell {
  text-align: center;
  vertical-align: middle;
  width: 72px;
}

.audio-button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.play-button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
  box-shadow: var(--shadow-sm);
}

.play-button:hover {
  background: var(--color-primary-hover);
  transform: scale(1.06);
}

.play-button.playing {
  background: var(--color-accent);
}

.play-button.playing:hover {
  filter: brightness(1.1);
}

.material-icons {
  font-size: 20px;
  line-height: 1;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .search-form.basic {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>