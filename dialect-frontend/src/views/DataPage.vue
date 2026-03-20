<template>
  <div class="data-container">
    <div class="page-header">
      <h1>词汇数据库</h1>
      <p class="page-desc">浏览与筛选语料库词条；GitHub 部署时可使用 public/data/dialect-words.json，亦可本地 JSON/CSV 导入</p>
    </div>

    <div class="card toolbar">
      <div class="filters">
        <div class="filter-group">
          <label>每页显示</label>
          <select v-model="pageSize" @change="updateDisplayedData">
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
        </div>
        <div class="filter-group file-upload">
          <label>导入数据</label>
          <input type="file" id="data-file" @change="importData" accept=".json, .csv">
          <span class="help-text">支持 JSON、CSV</span>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="card loading">
      <p>数据加载中...</p>
    </div>

    <div v-else-if="dataList.length === 0" class="card no-data">
      <p>暂无数据，请导入数据文件</p>
    </div>

    <div v-else class="card table-card">
    <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th>编号</th>
          <th>词汇</th>
          <th>老派词汇</th>
          <th>老派记音</th>
          <th>老派语音</th>
          <th>新派词汇</th>
          <th>新派记音</th>
          <th>新派语音</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in displayedData" :key="item.id || item.code">
          <td>{{ item.code }}</td>
          <td>{{ item.word }}</td>
          <td>{{ item.old_dialect_word }}</td>
          <td class="phonetic">{{ item.old_dialect_phonetic }}</td>
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
          <td class="phonetic">{{ item.new_dialect_phonetic }}</td>
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

    <div class="pagination">
      <button
        @click="prevPage"
        :disabled="currentPage === 1">
        上一页
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages || 1 }}</span>
      <button
        @click="nextPage"
        :disabled="currentPage < totalPages">
        下一页
      </button>
    </div>
    </div>

    <!-- 仅开发环境显示：音频路径调试 -->
    <div v-if="isDev && displayedData.length > 0" class="debug-info">
      <h3>音频文件路径示例：</h3>
      <div>
        <p><strong>老派候选 URL（先空格后下划线）:</strong> {{ formatAudioCandidates(displayedData[0], 'old') }}</p>
        <p><strong>新派候选 URL:</strong> {{ formatAudioCandidates(displayedData[0], 'new') }}</p>
        <button @click="testAudioPath">测试音频路径</button>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { getDialectAudioSrc, getDialectAudioSrcCandidates } from '@/utils/audioPaths'

export default {
  data() {
    return {
      allData: [],
      dataList: [],
      displayedData: [],
      currentPage: 1,
      pageSize: 20,
      totalItems: 0,
      isLoading: false,
      isPlaying: {},
      audioRefs: {},
      audioCandidateIdx: {},
      isDev: process.env.NODE_ENV === 'development'
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.pageSize) || 1;
    }
  },
  created() {
    // 加载Material Icons图标字体
    this.loadMaterialIcons();
  },
  mounted() {
    this.loadLocalData();
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
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons';
      document.head.appendChild(link);
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

    formatAudioCandidates (item, side) {
      return getDialectAudioSrcCandidates(item, side).join('\n')
    },

    onDialectAudioError (item, side, audioKey) {
      const list = getDialectAudioSrcCandidates(item, side)
      if (list.length < 2) return
      const k = this.audioSideKey(item, side)
      const idx = this.audioCandidateIdx[k] ?? 0
      if (idx + 1 >= list.length) return
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
      Object.keys(this.audioRefs).forEach(key => {
        if (key !== audioKey && this.audioRefs[key]) {
          this.audioRefs[key].pause();
          this.isPlaying[key] = false;
        }
      });

      const audioElement = this.audioRefs[audioKey];
      if (!audioElement) return;

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
              console.error('播放失败:', error)
              const src = audioElement.currentSrc || audioElement.src || '(无地址)'
              alert(
                '无法播放该条录音。\n\n' +
                '常见原因：\n' +
                '1. 尚未部署对应 mp3：请放到 public/audio/old_dialect 与 new_dialect，并重新构建/推送。\n' +
                '2. 文件名须与「词汇」一致；支持「0001 新派 太阳.mp3」或「0001_新派_太阳.mp3」两种。\n' +
                '3. 也可在数据里填写 old_dialect_audio / new_dialect_audio 为完整 URL 或相对路径。\n\n' +
                `当前请求地址：\n${src}`
              )
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

    getOldAudioPath(item) {
      return getDialectAudioSrc(item, 'old')
    },

    getNewAudioPath(item) {
      return getDialectAudioSrc(item, 'new')
    },

    // 从本地存储加载数据
    loadLocalData() {
      try {
        const savedData = localStorage.getItem('dialectWords');
        if (savedData) {
          this.allData = JSON.parse(savedData);
          this.updateDisplayedData();
        }
      } catch (error) {
        console.error('加载本地数据失败:', error);
      }
    },

    // 更新显示的数据
    updateDisplayedData() {
      if (!this.allData || this.allData.length === 0) return;

      this.totalItems = this.allData.length;
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.displayedData = this.allData.slice(start, end);
      this.dataList = this.allData;
    },

    // 导入数据文件
    importData(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.isLoading = true;

      // 处理JSON或CSV文件
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          let data;
          if (file.name.endsWith('.json')) {
            data = JSON.parse(e.target.result);
          } else if (file.name.endsWith('.csv')) {
            data = this.parseCSV(e.target.result);
          }

          if (Array.isArray(data)) {
            // 确保数据中包含记音字段
            data = data.map((item, index) => ({
              id: item.id || index + 1,
              code: item.code || (index + 1).toString(),
              word: item.word || '',
              old_dialect_word: item.old_dialect_word || '',
              old_dialect_phonetic: item.old_dialect_phonetic || '',
              old_dialect_audio: item.old_dialect_audio || '',
              new_dialect_word: item.new_dialect_word || '',
              new_dialect_phonetic: item.new_dialect_phonetic || '',
              new_dialect_audio: item.new_dialect_audio || ''
            }));

            this.allData = data;
            localStorage.setItem('dialectWords', JSON.stringify(data));
            this.currentPage = 1;
            this.updateDisplayedData();
          } else if (data && data.results && Array.isArray(data.results)) {
            // 处理API风格的响应格式
            const results = data.results.map((item, index) => ({
              id: item.id || index + 1,
              code: item.code || (index + 1).toString(),
              word: item.word || '',
              old_dialect_word: item.old_dialect_word || '',
              old_dialect_phonetic: item.old_dialect_phonetic || '',
              old_dialect_audio: item.old_dialect_audio || '',
              new_dialect_word: item.new_dialect_word || '',
              new_dialect_phonetic: item.new_dialect_phonetic || '',
              new_dialect_audio: item.new_dialect_audio || ''
            }));

            this.allData = results;
            localStorage.setItem('dialectWords', JSON.stringify(results));
            this.currentPage = 1;
            this.updateDisplayedData();
          }
        } catch (error) {
          console.error('解析数据文件失败:', error);
          alert('解析数据文件失败，请检查文件格式是否正确');
        } finally {
          this.isLoading = false;
        }
      };

      reader.onerror = () => {
        console.error('读取文件失败');
        this.isLoading = false;
        alert('读取文件失败');
      };

      reader.readAsText(file);
    },

    // 解析CSV
    parseCSV(text) {
      const lines = text.split('\n');
      const headers = lines[0].split(',').map(h => h.trim());

      return lines.slice(1).filter(line => line.trim()).map(line => {
        // 处理CSV中的引号包裹的字段
        const values = [];
        let inQuotes = false;
        let currentValue = '';

        for (let i = 0; i < line.length; i++) {
          const char = line[i];

          if (char === '"' && (i === 0 || line[i-1] !== '\\')) {
            inQuotes = !inQuotes;
          } else if (char === ',' && !inQuotes) {
            values.push(currentValue.trim());
            currentValue = '';
          } else {
            currentValue += char;
          }
        }

        // 添加最后一个值
        values.push(currentValue.trim());

        // 将值与表头匹配
        const obj = {};
        headers.forEach((header, index) => {
          if (index < values.length) {
            // 移除值两端的引号
            let value = values[index];
            if (value.startsWith('"') && value.endsWith('"')) {
              value = value.substring(1, value.length - 1);
            }
            obj[header] = value;
          } else {
            obj[header] = '';
          }
        });

        // 规范化字段名
        return {
          id: obj.id || obj.ID || obj['编号'] || '',
          code: obj.code || obj.CODE || obj['编号'] || '',
          word: obj.word || obj.WORD || obj['词汇'] || '',
          old_dialect_word: obj.old_dialect_word || obj['老派词汇'] || '',
          old_dialect_phonetic: obj.old_dialect_phonetic || obj['老派记音'] || '',
          old_dialect_audio: obj.old_dialect_audio || obj['老派语音'] || '',
          new_dialect_word: obj.new_dialect_word || obj['新派词汇'] || '',
          new_dialect_phonetic: obj.new_dialect_phonetic || obj['新派记音'] || '',
          new_dialect_audio: obj.new_dialect_audio || obj['新派语音'] || ''
        };
      });
    },

    // 分页操作
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        this.updateDisplayedData();
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
        this.updateDisplayedData();
      }
    },

    // 测试音频路径
    testAudioPath() {
      if (this.displayedData.length === 0) {
        alert('没有数据可供测试');
        return;
      }

      const item = this.displayedData[0];
      const oldList = getDialectAudioSrcCandidates(item, 'old').join('\n')
      const newList = getDialectAudioSrcCandidates(item, 'new').join('\n')

      alert(`测试音频路径（先空格后下划线，自动依次尝试）:\n\n老派:\n${oldList}\n\n新派:\n${newList}\n\n请在开发者工具「网络」中检查上述 URL 是否能 200 加载。`);
    }
  }
};
</script>

<style scoped>
.data-container {
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

.toolbar {
  padding: 16px 24px;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 24px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text);
}

.filter-group select {
  padding: 8px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: #fff;
  min-width: 80px;
}

.filter-group.file-upload input[type="file"] {
  font-size: 0.85rem;
  padding: 6px 0;
}

.help-text {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
}

.loading, .no-data {
  text-align: center;
  padding: 48px 24px;
  color: var(--color-text-secondary);
}

.table-card {
  padding: 0;
  overflow: hidden;
}

.table-wrap {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
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

.data-table tbody tr:hover {
  background: var(--color-primary-light);
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

.material-icons {
  font-size: 20px;
  line-height: 1;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-top: 1px solid var(--color-border);
}

.pagination button {
  padding: 10px 20px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.pagination button:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.pagination button:disabled {
  background: var(--color-border-strong);
  color: var(--color-text-secondary);
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.debug-info {
  margin-top: 24px;
  padding: 16px;
  background: var(--color-primary-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
}

.debug-info button {
  margin-top: 10px;
  padding: 8px 14px;
  background: var(--color-text-secondary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.85rem;
}
</style>