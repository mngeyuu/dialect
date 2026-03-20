<template>
  <div class="import-container">
    <div class="page-header">
      <h1>导入数据</h1>
      <p class="page-desc">通过 Excel 上传词条并关联语音文件</p>
    </div>

    <div class="card form-container">
      <div class="info-box">
        <h3>导入说明</h3>
        <p>1. 请上传包含以下列的 Excel 文件：<strong>编号、词汇、老派词汇、新派词汇</strong></p>
        <p>2. 系统将自动匹配 MP3 文件，命名规则：<code>[编号] [类型] [词汇].mp3</code></p>
        <p>3. 示例：<code>0001 老派 太阳.mp3</code>、<code>0001 新派 太阳.mp3</code></p>
      </div>

      <div class="form-group">
        <label>选择 Excel 文件</label>
        <input
          type="file"
          @change="handleFileChange"
          accept=".xlsx,.xls"
          class="file-input"
        >
      </div>

      <div class="buttons">
        <button
          @click="uploadFile"
          :disabled="!selectedFile || isUploading"
          class="btn-primary"
        >
          {{ isUploading ? '上传中...' : '上传并导入' }}
        </button>
      </div>

      <div v-if="uploadResult" class="result-message" :class="{ success: uploadResult.success }">
        <h3>{{ uploadResult.success ? '导入成功' : '导入失败' }}</h3>
        <p>{{ uploadResult.message }}</p>

        <div v-if="uploadResult.errors && uploadResult.errors.length > 0" class="error-details">
          <h4>错误详情</h4>
          <ul>
            <li v-for="(error, index) in uploadResult.errors" :key="index">
              编号 {{ error.code }} ({{ error.word }}): {{ error.error }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  data() {
    return {
      selectedFile: null,
      isUploading: false,
      uploadResult: null
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.uploadResult = null;
    },
    async uploadFile() {
      if (!this.selectedFile) return;

      this.isUploading = true;
      this.uploadResult = null;

      const formData = new FormData();
      formData.append('excel_file', this.selectedFile);

      try {
        // 不要手动设 Content-Type，否则缺少 boundary，上传会失败
        const response = await api.post('import-excel/', formData);

        this.uploadResult = response.data;
      } catch (error) {
        console.error('上传失败:', error);
        this.uploadResult = {
          success: false,
          message: '上传失败: ' + (error.response?.data?.message || error.message)
        };
      } finally {
        this.isUploading = false;
      }
    }
  }
};
</script>

<style scoped>
.import-container {
  max-width: 880px;
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
  padding: 28px;
}

.info-box {
  background: var(--color-primary-light);
  padding: 18px 20px;
  border-radius: var(--radius-sm);
  margin-bottom: 24px;
  border-left: 4px solid var(--color-primary);
}

.info-box h3 {
  font-size: 1rem;
  margin-bottom: 10px;
  color: var(--color-primary);
}

.info-box p {
  margin: 6px 0;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
}

.file-input {
  padding: 8px 0;
  font-size: 0.9rem;
}

.buttons {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  padding: 12px 24px;
  background: var(--color-primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-primary:disabled {
  background: var(--color-border-strong);
  color: var(--color-text-secondary);
  cursor: not-allowed;
}

.result-message {
  margin-top: 28px;
  padding: 18px 20px;
  border-radius: var(--radius-sm);
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.result-message.success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
}

.result-message h3 {
  font-size: 1rem;
  margin-bottom: 8px;
}

.result-message.success h3 {
  color: #166534;
}

.result-message:not(.success) h3 {
  color: #991b1b;
}

.result-message p {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin: 0;
}

.error-details {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid rgba(0,0,0,0.08);
}

.error-details h4 {
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: var(--color-text);
}

.error-details ul {
  padding-left: 20px;
  font-size: 0.85rem;
  color: var(--color-text-secondary);
}

.error-details li {
  margin-bottom: 4px;
}

code {
  background: var(--color-border);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: ui-monospace, monospace;
  font-size: 0.88em;
}

@media (max-width: 768px) {
  .import-container {
    max-width: 100%;
  }

  .card {
    padding: 20px;
  }

  .buttons {
    justify-content: stretch;
  }

  .btn-primary {
    width: 100%;
  }
}
</style>