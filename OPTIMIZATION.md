# 方言词汇语料库项目 — 优化建议

本文档汇总了从**性能、安全、代码质量、用户体验**等角度的优化方向，便于按优先级逐步实施。

---

## 一、数据流与架构

### 1. 统一数据源（高优先级）

- **现状**：数据页、搜索页目前只从 `localStorage` 读数据，导入页才调后端 API。数据存在「导入到后端」与「前端只用本地」的不一致。
- **建议**：
  - **方案 A**：数据页/搜索页优先从后端 API 拉取（分页 + 搜索参数），localStorage 仅作离线缓存或导出用。
  - **方案 B**：若产品定位为「单机 + 本地文件」，则明确只使用 localStorage/本地文件，导入仅写本地，不依赖 Django；此时可考虑弱化或移除后端列表接口。
- **收益**：数据一致、支持多设备/重装不丢数据（若选 A）；或逻辑更清晰、包体更小（若选 B）。

### 2. 后端分页与列表接口

- **现状**：Django REST 已配置 `PageNumberPagination`、`PAGE_SIZE=20`，但前端数据页未调用 API，而是整份数据放内存再前端分页。
- **建议**：若采用「后端为主」：
  - 数据页改为请求 `/api/dialect-words/?page=1&page_size=20`，并支持 `search`、`word`、`old_dialect`、`new_dialect` 等查询参数。
  - 避免一次性拉取全部词条，减少内存与首屏时间。

---

## 二、前端优化

### 3. 路由懒加载（中优先级）

- **现状**：`router/index.js` 中所有页面为同步 `import`，首包体积较大。
- **建议**：改为懒加载，例如：
  ```js
  component: () => import('../views/HomePage.vue')
  ```
- **收益**：首屏只加载当前路由对应 chunk，加快首屏。

### 4. 抽离公共逻辑（中优先级）

- **现状**：`DataPage.vue` 与 `SearchPage.vue` 中「音频播放、路径计算、Material Icons、记音字体」等大量重复。
- **建议**：
  - 将「老派/新派音频路径、播放、ref 管理」抽成 **composable**（如 `useDialectAudio.js`）或 **Mixin**。
  - 将「词汇表格行」（编号、词汇、老派/新派词、记音、音频按钮）抽成 **子组件**（如 `DialectWordRow.vue`），两页复用。
- **收益**：维护成本低、行为一致、减少重复代码。

### 5. 移除或隐藏生产环境调试 UI（低优先级）

- **现状**：数据页底部有「音频文件路径示例」等调试信息，对普通用户无意义。
- **建议**：删除该块，或使用 `v-if="process.env.NODE_ENV === 'development'"` 仅在开发环境显示。

### 6. 资源与依赖

- **Material Icons**：在多个页面重复通过 JS 插入 `<link>`，建议在 `index.html` 或 `App.vue` 中统一引入一次。
- **API 基地址**：`api.js` 中 `baseURL` 写死 `http://localhost:8000/api/`，建议改为 `process.env.VUE_APP_API_URL || 'http://localhost:8000'`，并在请求时统一加 `/api` 或在后端配置好代理，便于开发/生产/Electron 不同环境切换。

---

## 三、后端优化

### 7. 导入接口：日志与批量写入（中优先级）

- **现状**：`import_excel` 中大量使用 `print()` 做调试；逐条 `save()`，大量数据时较慢。
- **建议**：
  - 用 `logging` 替代 `print`，并按环境控制日志级别。
  - 先解析 Excel 得到对象列表，再用 `DialectWord.objects.bulk_create()` 批量插入（注意：若有「存在则更新」逻辑，可先查已存在编号，再分批 `bulk_create` + 少量 `update`）。
- **收益**：生产环境日志可控、导入速度明显提升。

### 8. 模型与序列化器（低优先级）

- **现状**：前端使用了 `old_dialect_phonetic`、`new_dialect_phonetic`，当前 Django 模型未包含这两列。
- **建议**：若业务需要记音字段，在 `DialectWord` 上增加对应字段并做迁移；若不需要，前端去掉对这两字段的展示与搜索，保持前后端一致。

---

## 四、Electron 与安全

### 9. 安全配置（高优先级）

- **现状**：`pack/dialect-electron-app/main.js` 中：
  - `webPreferences`: `nodeIntegration: true`, `contextIsolation: false`, `webSecurity: false`
- **建议**：
  - 开启 `contextIsolation: true`，关闭或最小化 `nodeIntegration`，通过 `preload` 暴露有限 API（如读本地路径、启动 Django 子进程等）。
  - 将 `webSecurity` 设为 `true`，仅在有跨域需求时通过 CSP 或代理放宽，避免全局关闭。
- **收益**：降低 XSS 或恶意页面访问本地/Node 的能力，符合常见桌面应用安全实践。

### 10. 启动与超时

- **现状**：`waitForDjango` 轮询 30 次、每次间隔 1 秒，且未区分「开发/打包」环境。
- **建议**：可考虑略缩短间隔（如 500ms）、增加总超时时间配置；在开发环境下可跳过等待或使用更短超时，提升开发体验。

---

## 五、构建与配置

### 11. vue.config.js 合并（低优先级）

- **现状**：存在两个 `module.exports`，后者会覆盖前者，导致 `publicPath`、`devServer.proxy`、`parallel` 等可能不生效。
- **建议**：合并为单一 `module.exports`，把 `publicPath`、`devServer`、`configureWebpack` 与 `pluginOptions.electronBuilder` 写在一起。

### 12. 环境变量与打包

- 为 Electron 打包与本地开发分别配置 `.env.development`、`.env.production`（如 `VUE_APP_API_URL`）。
- 打包后的应用若使用内嵌 Django，API 基地址应为相对路径或 `localhost`（与当前后端实际监听一致），避免硬编码。

---

## 六、实施优先级小结

| 优先级 | 项 | 说明 |
|--------|----|------|
| 高 | 统一数据源 | 决定数据页/搜索页用 API 还是纯本地，影响整体架构 |
| 高 | Electron 安全配置 | 提升桌面应用安全性 |
| 中 | 路由懒加载、抽离公共逻辑 | 首屏与可维护性 |
| 中 | 后端导入：logging + 批量写入 | 日志规范与导入性能 |
| 低 | 移除调试 UI、合并 vue.config、模型与前端字段统一 | 体验与配置清晰 |

建议先确定「数据源与产品形态」（后端为主 vs 单机本地），再按上表顺序逐步落地；每做完一块可做一次回归测试（导入、搜索、播放、打包运行）。
