# 把「国创」项目部署成 GitHub 网页（GitHub Pages）

本仓库的 **网站部分** 是 `dialect-frontend`（Vue 3）。已配置 **GitHub Actions**：推送到 `main` 或 `master` 后自动构建并发布到 GitHub Pages。

---

## 一、在 GitHub 上建仓库并推送代码

1. 在 GitHub 新建一个仓库（建议英文名，例如 `guochuang` 或 `dialect-corpus`）。
2. 在本机项目根目录（`国创`）执行：

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/mngeyuu/dialect.git
git branch -M main
git push -u origin main
```

（若远程已存在同名仓库，请把上面地址换成你的；当前示例为 [mngeyuu/dialect](https://github.com/mngeyuu/dialect)。）

> 若仓库很大（含 `pack-env`、`node_modules` 等），请先配置 **`.gitignore`**，不要提交 `node_modules`、虚拟环境等大目录。

---

## 二、开启 GitHub Pages（必须）

1. 打开 GitHub 仓库 → **Settings** → **Pages**。
2. **Build and deployment** → **Source** 选择 **GitHub Actions**（不要选 Deploy from a branch 的旧方式，否则和本 Workflow 不一致）。
3. 保存后，**Actions** 标签页里应出现 **Deploy GitHub Pages** 工作流；推送代码或手动 **Run workflow** 即可部署。

---

## 三、访问地址

- **项目站**：`https://你的用户名.github.io/仓库名/`  
  例如：`https://zhangsan.github.io/guochuang/`
- **用户站**（仅当仓库名为 `用户名.github.io` 时）：`https://你的用户名.github.io/`

本项目前端使用 **`publicPath: './'`** 与 **Hash 路由**（地址形如 `.../guochuang/#/`），在 **项目子路径** 下一般可正常加载 JS/CSS 与图片。

若你改成了 **history 模式** 或 **绝对路径 base**，需同步修改 `vue.config.js` 里的 `publicPath` 为 `/仓库名/`。

---

## 四、不上传后端：只放「剪辑数据 + 录音」到 GitHub（推荐）

**可以。** 不需要自己的服务器，把文件放进 `dialect-frontend/public` 即可，和网页一起部署后就能在站点里 **搜索 + 播放音频**。

### 你要维护的文件

| 位置 | 作用 |
|------|------|
| `dialect-frontend/public/data/dialect-words.json` | 词条列表（编号、词汇、老派/新派词、记音等） |
| `dialect-frontend/public/audio/old_dialect/*.mp3` | 老派录音 |
| `dialect-frontend/public/audio/new_dialect/*.mp3` | 新派录音 |

### 录音命名（须与 JSON 里 `word`、`code` 一致）

- 老派：`0001 老派 太阳.mp3`（四位编号 + 空格 + 老派 + 空格 + 词汇 + `.mp3`）
- 新派：`0001 新派 太阳.mp3`

**字段说明、示例** 见同目录 **`public/data/README.md`**。

### 工作流程

1. 用剪辑软件导出 MP3，按上面规则命名，放进 `audio/old_dialect`、`audio/new_dialect`。
2. 编辑 `dialect-words.json`（可用 Excel 整理好再转 JSON，或复制现有导出格式）。
3. `git add` → `commit` → `push`，等 **GitHub Actions** 部署完成。
4. 打开 `https://你的用户名.github.io/仓库名/#/`，建议 **Ctrl+F5** 强刷，避免旧 JSON 被缓存。

### 行为说明

- 打开网站时会请求 **`data/dialect-words.json`**；若文件里 **至少有一条词条**，会写入浏览器缓存，**搜索 / 数据库** 页直接使用。
- 若 JSON 仍是 **空数组 `[]`**，则**不会覆盖**你本机已在「数据库」页导入的数据。
- 音频走静态地址 **`./audio/...`**，与 GitHub Pages 兼容；仓库体积大时注意 [GitHub 单文件 100MB 限制](https://docs.github.com/repositories/working-with-files/managing-large-files/about-large-files-on-github)。

---

## 五、GitHub Pages 上能做什么 / 不能做什么

| 可以 | 不可以 |
|------|--------|
| 首页、地图、照片、视频等 **静态资源** | 运行本机 **Django 后端** |
| **静态语料 JSON + MP3**（见上一节）在线浏览、搜索、播放 | **导入 Excel 到服务器**（无后端时不可用） |
| **数据库**页用 **JSON/CSV 导入**（仅本机浏览器） | 直接访问 `localhost:8000` 的后端 |

若以后把 Django 部署到公网（如 Railway、自己的服务器），可在构建时设置环境变量：

```yaml
# 在 .github/workflows/github-pages.yml 的 build 步骤里增加：
env:
  VUE_APP_API_URL: https://你的API域名
```

并在 `dialect-frontend` 里已支持通过 `VUE_APP_API_URL` 配置 API 根地址。

---

## 六、手动本地构建预览（可选）

```bash
cd dialect-frontend
npm install
npm run build
```

用任意静态服务器打开 `dialect-frontend/dist`（注意用子路径预览时与线上 URL 一致更准）。

---

## 七、常见问题

1. **Actions 报错 `npm ci` 失败**  
   确认已提交 `dialect-frontend/package-lock.json`。

2. **页面空白**  
   打开浏览器开发者工具 → Network，看 JS/CSS 是否 404；若是，检查 `publicPath` 与仓库子路径是否一致。

3. **图片/视频不显示**  
   确认文件在 `dialect-frontend/public/` 下且已提交到 Git；路径区分大小写。
