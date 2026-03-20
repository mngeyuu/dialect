# 使用 public 目录实现方言首页

使用 public 目录是处理静态资源的简单可靠方法，特别适合 Electron 应用。下面是完整的实现方案：

## 1. 创建资源目录结构

在项目根目录下创建以下目录结构：

```
public/
├── images/
│   ├── map.jpg              // 地区地图
│   ├── photo1.jpg           // 历史照片1
│   ├── photo2.jpg           // 历史照片2
│   ├── photo3.jpg           // 历史照片3
│   ├── photo4.jpg           // 历史照片4
│   ├── photo5.jpg           // 历史照片5
│   └── video-thumbs/        // 视频缩略图
│       ├── local1.jpg
│       ├── festival.jpg
│       ├── personal1.jpg
│       ├── local2.jpg
│       └── personal2.jpg
└── videos/
    ├── local_situation1.mp4
    ├── traditional_festival.mp4
    ├── personal_experience1.mp4
    ├── local_situation2.mp4
    └── personal_experience2.mp4
```

## 2. 创建 HomePage.vue 组件

```vue
<template>
  <div class="home-page">
    <!-- 主容器 -->
    <div class="main-container">
      <!-- 左上角资料区域 -->
      <div class="info-section">
        <h2 class="dialect-title">洞庭 洞庭 老城区 【中原官话-洞庭片】</h2>
        <div class="dialect-info">
          <p><span class="label">调查负责人：</span>无名姓</p>
          <p><span class="label">单位：</span>洛阳理工学院</p>
          <p><span class="label">调查简介：</span>洛阳老城区位于河南老城区，是拥有人口9.5万多，为本地带富调研的方言。近年来受化妆体系影响幕老化，近在中原普通话范畴。老城区大体以四条（东、西、南、北）为界，四条内外语音差异较小，主要变现为否定词"不"音和"出租车不用"，如"钩""圪"，四条之外读"tshy3"，四条之外有的地方读"tshou3"，都为老城人士语言口袋仓库。</p>
        </div>
        
        <!-- 文档/下载区域 -->
        <div class="document-section">
          <h3>文档</h3>
          <div class="document-list">
            <div class="document-item">
              <span>方言点基本信息</span>
              <span class="download">↓</span>
            </div>
            <div class="document-item">
              <span>方言词汇录音采访记录</span>
              <span class="download">↓</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧地图区域 (使用静态图片) -->
      <div class="map-section">
        <div class="map-header">
          <span>老城区地图</span>
        </div>
        <div class="static-map">
          <img src="/images/map.jpg" alt="洛阳老城区地图">
        </div>
      </div>
      
      <!-- 清除浮动 -->
      <div class="clearfix"></div>
      
      <!-- 照片区域 -->
      <div class="photos-section">
        <h2>历史照片</h2>
        <div class="photo-container">
          <div v-for="(photo, index) in photos" :key="'photo-'+index" class="photo-item">
            <img :src="photo.url" :alt="photo.description">
          </div>
        </div>
      </div>
      
      <!-- 视频区域 -->
      <div class="videos-section">
        <h2>方言视频</h2>
        <div class="video-container">
          <div v-for="(video, index) in videos" :key="'video-'+index" class="video-item">
            <div class="video-thumbnail" @click="playVideo(video)">
              <img :src="video.thumb" :alt="video.title">
              <div class="play-button">▶</div>
              <span class="video-title">{{ video.title }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 视频播放模态框 -->
      <div v-if="showVideoModal" class="video-modal" @click="closeVideoModal">
        <div class="video-modal-content" @click.stop>
          <div class="modal-header">
            <h3>{{ currentVideo.title }}</h3>
            <span class="close-button" @click="closeVideoModal">&times;</span>
          </div>
          <video ref="videoPlayer" controls autoplay width="100%">
            <source :src="currentVideo.src" type="video/mp4">
            您的浏览器不支持HTML5视频
          </video>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      // 照片数据 - 使用公共路径
      photos: [
        { url: '/images/photo1.jpg', description: '老城区历史建筑1' },
        { url: '/images/photo2.jpg', description: '老城区历史建筑2' },
        { url: '/images/photo3.jpg', description: '老城区历史建筑3' },
        { url: '/images/photo4.jpg', description: '老城区历史建筑4' },
        { url: '/images/photo5.jpg', description: '老城区历史建筑5' }
      ],
      
      // 视频数据 - 使用公共路径
      videos: [
        { 
          id: 'video1', 
          title: '当地情况', 
          src: '/videos/local_situation1.mp4',
          thumb: '/images/video-thumbs/local1.jpg'
        },
        { 
          id: 'video2', 
          title: '传统节日', 
          src: '/videos/traditional_festival.mp4',
          thumb: '/images/video-thumbs/festival.jpg'
        },
        { 
          id: 'video3', 
          title: '个人经历', 
          src: '/videos/personal_experience1.mp4',
          thumb: '/images/video-thumbs/personal1.jpg'
        },
        { 
          id: 'video4', 
          title: '当地情况', 
          src: '/videos/local_situation2.mp4',
          thumb: '/images/video-thumbs/local2.jpg'
        },
        { 
          id: 'video5', 
          title: '个人经历', 
          src: '/videos/personal_experience2.mp4',
          thumb: '/images/video-thumbs/personal2.jpg'
        }
      ],
      
      // 视频播放控制
      showVideoModal: false,
      currentVideo: null
    }
  },
  methods: {
    playVideo(video) {
      this.currentVideo = video;
      this.showVideoModal = true;
      
      // 在nextTick后确保video元素已经渲染并开始播放
      this.$nextTick(() => {
        if (this.$refs.videoPlayer) {
          this.$refs.videoPlayer.play().catch(err => {
            console.error('视频播放失败:', err);
          });
        }
      });
    },
    closeVideoModal() {
      // 关闭模态框前暂停视频
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.pause();
      }
      this.showVideoModal = false;
      this.currentVideo = null;
    }
  },
  // 确保在组件销毁时清理资源
  beforeDestroy() {
    if (this.showVideoModal && this.$refs.videoPlayer) {
      this.$refs.videoPlayer.pause();
    }
  }
}
</script>

<style scoped>
.home-page {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Microsoft YaHei', Arial, sans-serif;
}

.main-container {
  border: 1px solid #e0e0e0;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* 资料区域样式 */
.info-section {
  float: left;
  width: 40%;
  padding: 15px;
  border: 1px solid #e0e0e0;
  background-color: #f9f9f9;
  position: relative;
}

.dialect-title {
  color: #d32f2f;
  font-size: 18px;
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
}

.dialect-info {
  font-size: 14px;
  line-height: 1.6;
}

.label {
  font-weight: bold;
  color: #555;
}

.document-section {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #e0e0e0;
}

.document-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px dashed #e0e0e0;
}

.download {
  cursor: pointer;
  color: #d32f2f;
}

/* 地图区域样式 */
.map-section {
  float: right;
  width: 58%;
  height: 350px;
  border: 1px solid #e0e0e0;
  overflow: hidden;
}

.map-header {
  background-color: #f5f5f5;
  padding: 8px 15px;
  border-bottom: 1px solid #e0e0e0;
  font-weight: bold;
}

.static-map {
  width: 100%;
  height: calc(100% - 37px); /* 减去header高度 */
}

.static-map img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片覆盖整个区域 */
}

.clearfix {
  clear: both;
}

/* 照片区域样式 */
.photos-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #d32f2f;
}

.photos-section h2 {
  color: #333;
  font-size: 20px;
  margin-bottom: 15px;
}

.photo-container {
  display: flex;
  overflow-x: auto;
  padding: 10px 0;
}

.photo-item {
  flex: 0 0 auto;
  width: 200px;
  height: 150px;
  margin-right: 15px;
  border: 1px solid #e0e0e0;
  overflow: hidden;
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.photo-item img:hover {
  transform: scale(1.05);
}

/* 视频区域样式 */
.videos-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #d32f2f;
}

.videos-section h2 {
  color: #333;
  font-size: 20px;
  margin-bottom: 15px;
}

.video-container {
  display: flex;
  overflow-x: auto;
  padding: 10px 0;
}

.video-item {
  flex: 0 0 auto;
  width: 200px;
  height: 150px;
  margin-right: 15px;
  position: relative;
  cursor: pointer;
}

.video-thumbnail {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 30px;
  background-color: rgba(0, 0, 0, 0.5);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.video-thumbnail:hover .play-button {
  background-color: rgba(211, 47, 47, 0.7);
}

.video-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 5px 10px;
  font-size: 12px;
  text-align: center;
}

/* 视频播放模态框 */
.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.video-modal-content {
  width: 80%;
  max-width: 800px;
  background-color: #fff;
  border-radius: 5px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-button {
  font-size: 24px;
  cursor: pointer;
  color: #555;
}

.close-button:hover {
  color: #d32f2f;
}
</style>
```

## 3. 修改 router/index.js

确保添加首页路由：

```javascript
import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '../views/HomePage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  // 其他已有路由保持不变
]

const router = new VueRouter({
  mode: 'history',  // 使用HTML5历史模式
  base: process.env.BASE_URL,
  routes
})

export default router
```

## 4. 修改 vue.config.js

使用简化版本，避免任何可能的加载器冲突：

```javascript
module.exports = {
  publicPath: "./", // 让 Vue 生成相对路径
  
  // 禁用并行处理，避免线程加载器错误
  parallel: false,
  
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  
  // 简化配置
  configureWebpack: {
    performance: {
      hints: false  // 关闭性能提示
    }
  }
}
```

## 5. 准备资源文件

为了方便您实现这个页面，我为您提供几个建议：

1. **地图图片**：您可以从百度地图或高德地图截图，或使用地图API生成静态地图图片。
2. **历史照片**：如果没有实际照片，可以使用通用的历史建筑照片。
3. **视频缩略图**：如果没有实际的视频缩略图，可以：
   - 从视频中截取第一帧作为缩略图
   - 创建简单的文字显示图片作为占位符
   - 使用视频主题相关的图片
4. **视频文件**：如果您还没有实际视频，可以先使用短的示例视频文件进行测试。

## 6. 支持视频上传功能

如果您需要添加视频上传功能，可以在 HomePage.vue 中添加上传组件：

```vue
<template>
  <!-- 在视频区域的末尾添加 -->
  <div class="videos-section">
    <!-- ...现有代码 -->
    
    <!-- 视频上传按钮 -->
    <div class="upload-container">
      <button class="upload-button" @click="showUploadDialog">上传新视频</button>
    </div>
    
    <!-- 上传对话框 -->
    <div v-if="showUpload" class="upload-dialog">
      <div class="upload-header">
        <h3>上传方言视频</h3>
        <span class="close-button" @click="cancelUpload">&times;</span>
      </div>
      <div class="upload-body">
        <div class="form-group">
          <label>视频标题</label>
          <input type="text" v-model="uploadTitle" placeholder="请输入视频标题">
        </div>
        <div class="form-group">
          <label>视频类型</label>
          <select v-model="uploadType">
            <option value="当地情况">当地情况</option>
            <option value="传统节日">传统节日</option>
            <option value="个人经历">个人经历</option>
          </select>
        </div>
        <div class="form-group">
          <label>选择视频文件</label>
          <input type="file" @change="handleFileUpload" accept="video/mp4,video/webm">
          <p class="file-name" v-if="selectedFile">已选择: {{ selectedFile.name }}</p>
        </div>
        <div class="upload-actions">
          <button class="upload-submit" @click="uploadVideo" :disabled="!selectedFile || !uploadTitle">上传</button>
          <button class="upload-cancel" @click="cancelUpload">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // ...现有代码
  
  data() {
    return {
      // ...现有数据
      
      // 上传相关
      showUpload: false,
      uploadTitle: '',
      uploadType: '当地情况',
      selectedFile: null,
      uploadProgress: 0
    }
  },
  
  methods: {
    // ...现有方法
    
    // 上传相关方法
    showUploadDialog() {
      this.showUpload = true;
    },
    
    cancelUpload() {
      this.showUpload = false;
      this.uploadTitle = '';
      this.selectedFile = null;
      this.uploadProgress = 0;
    },
    
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    
    uploadVideo() {
      if (!this.selectedFile || !this.uploadTitle) return;
      
      // 创建表单数据
      const formData = new FormData();
      formData.append('video', this.selectedFile);
      formData.append('title', this.uploadTitle);
      formData.append('type', this.uploadType);
      
      // 发送到后端API
      // 使用axios或其他HTTP客户端
      this.$http.post('/api/videos/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: progressEvent => {
          this.uploadProgress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
        }
      }).then(response => {
        // 上传成功处理
        alert('视频上传成功！');
        this.videos.push({
          id: response.data.id,
          title: this.uploadTitle,
          src: response.data.videoUrl,
          thumb: response.data.thumbnailUrl
        });
        this.cancelUpload();
      }).catch(error => {
        // 错误处理
        console.error('上传失败:', error);
        alert('视频上传失败: ' + (error.response?.data?.message || '未知错误'));
      });
    }
  }
}
</script>

<style scoped>
/* ...现有样式 */

/* 上传按钮样式 */
.upload-container {
  margin-top: 15px;
  text-align: right;
}

.upload-button {
  background-color: #d32f2f;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.upload-button:hover {
  background-color: #b71c1c;
}

/* 上传对话框样式 */
.upload-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 500px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  z-index: 1100;
}

.upload-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.upload-header h3 {
  margin: 0;
  font-size: 18px;
}

.upload-body {
  padding: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input[type="text"],
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.file-name {
  margin-top: 5px;
  font-size: 14px;
  color: #555;
}

.upload-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.upload-submit,
.upload-cancel {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.upload-submit {
  background-color: #4caf50;
  color: white;
}

.upload-submit:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.upload-cancel {
  background-color: #f5f5f5;
  color: #333;
}
</style>
```

## 7. Electron 集成注意事项

1. **在 Electron 主进程中正确处理公共目录**:

```javascript
// main.js
const path = require('path');
const { app, BrowserWindow } = require('electron');
const isDev = require('electron-is-dev');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:8080');
    mainWindow.webContents.openDevTools();
  } else {
    // 加载Vue打包后的文件
    mainWindow.loadFile(path.join(__dirname, 'frontend/dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
```

1. **打包配置中包含静态资源**:

确保在 `electron-builder` 配置中包含 public 文件夹：

```json
"build": {
  "appId": "com.yourcompany.dialect-app",
  "productName": "方言搜索",
  "files": [
    "main.js",
    "preload.js",
    "frontend/dist/**/*",
    "!**/node_modules/**/*",
    "package.json"
  ],
  "extraResources": [
    {
      "from": "frontend/public",
      "to": "public"
    },
    {
      "from": "backend",
      "to": "backend"
    },
    {
      "from": "python-env",
      "to": "python"
    }
  ]
}
```

1. **在生产环境中正确访问资源**:

如果打包后无法正确访问资源，可能需要在 preload.js 中添加全局变量来处理资源路径：

```javascript
// preload.js
const { contextBridge } = require('electron');
const path = require('path');
const fs = require('fs');
const { app } = require('@electron/remote');

contextBridge.exposeInMainWorld('electronAPI', {
  getResourcePath: (resourceType) => {
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      return `/${resourceType}`;
    } else {
      return path.join(app.getAppPath(), '../public', resourceType);
    }
  }
});
```

然后在 Vue 组件中使用：

```javascript
mounted() {
  if (window.electronAPI) {
    // 在Electron环境中
    const imagesPath = window.electronAPI.getResourcePath('images');
    const videosPath = window.electronAPI.getResourcePath('videos');
    
    // 更新资源路径
    this.photos = this.photos.map(photo => {
      return {
        ...photo,
        url: path.join(imagesPath, path.basename(photo.url))
      };
    });
    
    this.videos = this.videos.map(video => {
      return {
        ...video,
        src: path.join(videosPath, path.basename(video.src)),
        thumb: path.join(imagesPath, 'video-thumbs', path.basename(video.thumb))
      };
    });
  }
}
```

## 8. 总结与测试

1. 创建所需目录结构并准备静态资源
2. 实现 HomePage.vue 组件
3. 更新路由配置
4. 修改 vue.config.js 简化配置
5. 在开发环境中测试
6. 构建并在 Electron 中测试

使用 public 目录的主要优点是简化资源处理，避免 webpack 加载器错误，并且在 Electron 应用中更容易管理大型静态资源。

测试步骤：

1. `npm run serve` - 测试Vue开发服务器
2. `npm run build` - 构建Vue项目
3. `npm run electron:serve` - 测试在Electron中的表现

遵循这些步骤，您应该能够成功实现方言首页并避免之前遇到的编译错误。