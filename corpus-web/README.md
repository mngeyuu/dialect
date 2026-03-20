# 方言语料库 · 新版站点（corpus-web）

从零搭建的 **Vite + Vue 3** 单页应用：首页图文、语料分页、搜索、老派/新派双音频，静态资源（**图片 SVG、JSON、mp3**）均在 `public/`。

## 开发

```bash
cd corpus-web
npm install
npm run dev
```

浏览器访问终端提示的本地地址（一般为 `http://localhost:5173`）。

## 构建

```bash
npm run build
```

产物在 `dist/`，可部署到任意静态主机或 GitHub Pages（已含 `public/.nojekyll`）。

## 内容资源

| 类型 | 位置 |
|------|------|
| 词条 JSON | `public/data/corpus.json`（可从 `../dialect-frontend/public/data/dialect-words.json` 复制改名） |
| 配图 | `public/images/*.svg`（可替换为自有 SVG/PNG 并改组件引用路径） |
| 录音 | `public/audio/old_dialect/`、`public/audio/new_dialect/` |

## 与旧版 `dialect-frontend` 的关系

本目录为**独立工程**，不依赖 Vue CLI / Electron。若需桌面端，可继续沿用原 `dialect-frontend` 或对 `dist` 做套壳。
