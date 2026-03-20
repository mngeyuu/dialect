<template>
  <div class="home-page">
    <!-- 主容器 -->
    <div class="main-container">
      <!-- 左上角资料区域 -->
      <div class="info-section">
        <h2 class="dialect-title">河南 洛阳 伊川县【中原官话洛嵩片】 </h2>
        <div class="dialect-info">
          <p><span class="label">调查负责人：</span>李燕臻</p>
          <p><span class="label">单位：</span>兰州大学</p>
          <p><span class="label">调查简介：</span>伊川县，隶属河南省洛阳市。位于河南省西部，北依洛阳城区，南接嵩县，总面积1059平方千米。截至2022年，伊川县常住人口76.8万人。
洛阳伊川话，分布在河南省中西部，洛阳市南部，使用人口约76万，为本地普遍通用的方言。伊川话近年来变化较快，新老派词汇差异逐渐增加，特别是年轻人代表的新派，正在向普通话靠拢；而老年人代表的老派，则正在逐渐消逝。</p>
        </div>
      </div>

      <!-- 右侧地图区域 (使用静态图片) -->
      <div class="map-section">
        <div class="map-header">
          <span>伊川县地图</span>
        </div>
        <div class="static-map">
          <img src="images/map.jpg" alt="洛阳老城区地图">
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
        { url: 'images/photo1.jpg', description: '老城区历史建筑1' },
        { url: 'images/photo2.jpg', description: '老城区历史建筑2' },
        { url: 'images/photo3.jpg', description: '老城区历史建筑3' },
        { url: 'images/photo4.jpg', description: '老城区历史建筑4' },
        { url: 'images/photo5.jpg', description: '老城区历史建筑5' },
        { url: 'images/photo6.jpg', description: '老城区历史建筑5' }
      ],

      // 视频数据 - 使用公共路径
      videos: [
        {
          id: 'video3',
          title: '个人经历',
          src: 'videos/personal_experience1.mp4',
          thumb: 'images/video-thumbs/personal1.jpg'
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
  beforeUnmount() {
    if (this.showVideoModal && this.$refs.videoPlayer) {
      this.$refs.videoPlayer.pause();
    }
  }
}
</script>

<style scoped>
.home-page {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.main-container {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 28px;
  border: 1px solid var(--color-border);
  position: relative;
}

/* 资料 + 地图 两栏 */
.info-section {
  float: left;
  width: 42%;
  min-height: 340px;
  padding: 20px;
  border-radius: var(--radius-md);
  background: var(--color-primary-light);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
}

.dialect-title {
  color: var(--color-primary);
  font-size: 1.1rem;
  margin-top: 0;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--color-accent-soft);
  font-family: var(--font-serif);
  font-weight: 600;
}

.dialect-info {
  font-size: 0.9rem;
  line-height: 1.7;
  flex-grow: 1;
  color: var(--color-text-secondary);
}

.dialect-info p {
  margin-bottom: 0.6em;
}

.label {
  font-weight: 600;
  color: var(--color-text);
  margin-right: 4px;
}

.map-section {
  float: right;
  width: 55%;
  height: 340px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.map-header {
  background: linear-gradient(180deg, #faf8f5 0%, #f0ebe4 100%);
  padding: 10px 16px;
  border-bottom: 1px solid var(--color-border);
  font-weight: 600;
  color: var(--color-primary);
  font-size: 0.95rem;
}

.static-map {
  width: 100%;
  height: calc(100% - 42px);
}

.static-map img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.clearfix {
  clear: both;
}

/* 照片区域 */
.photos-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid var(--color-border-strong);
}

.photos-section h2 {
  margin-bottom: 16px;
  color: var(--color-primary);
}

.photo-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  padding: 8px 0;
}

.photo-item {
  width: 100%;
  height: 160px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition: box-shadow 0.25s, transform 0.25s;
}

.photo-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.35s;
}

.photo-item:hover img {
  transform: scale(1.04);
}

/* 视频区域 */
.videos-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid var(--color-border-strong);
}

.videos-section h2 {
  margin-bottom: 16px;
  color: var(--color-primary);
}

.video-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  padding: 8px 0;
}

.video-item {
  width: 100%;
  height: 140px;
  position: relative;
  cursor: pointer;
}

.video-thumbnail {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  transition: box-shadow 0.25s;
}

.video-thumbnail:hover {
  box-shadow: var(--shadow-md);
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
  font-size: 28px;
  background: rgba(107, 45, 60, 0.75);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.25s, transform 0.25s;
}

.video-thumbnail:hover .play-button {
  background: var(--color-primary);
  transform: translate(-50%, -50%) scale(1.08);
}

.video-title {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  color: #fff;
  padding: 24px 10px 8px;
  font-size: 0.8rem;
  text-align: center;
}

/* 视频模态框 */
.video-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.82);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.video-modal-content {
  width: 90%;
  max-width: 800px;
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  background: var(--color-primary-light);
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.05rem;
  color: var(--color-primary);
}

.close-button {
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-secondary);
  line-height: 1;
  padding: 4px;
  transition: color 0.2s;
}

.close-button:hover {
  color: var(--color-primary);
}

/* 响应式 */
@media (max-width: 991px) {
  .info-section,
  .map-section {
    float: none;
    width: 100%;
    margin-bottom: 20px;
  }

  .map-section {
    height: 280px;
  }

  .photo-container,
  .video-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 767px) {
  .main-container {
    padding: 18px;
  }

  .photo-container,
  .video-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .photo-container,
  .video-container {
    grid-template-columns: 1fr;
  }
}
</style>