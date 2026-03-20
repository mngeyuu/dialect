# 静态语料数据（GitHub Pages / 无后端）

把本文件 **`dialect-words.json`** 与 **`public/audio/`** 下的录音一起提交到仓库，推送后会随网站部署；打开网页时会自动加载到浏览器（与「数据库 / 搜索」共用一份数据）。

## `dialect-words.json` 格式

JSON **数组**，每条对象字段示例：

```json
[
  {
    "id": 1,
    "code": "0001",
    "word": "太阳",
    "old_dialect_word": "日头",
    "old_dialect_phonetic": "",
    "old_dialect_audio": "",
    "new_dialect_word": "",
    "new_dialect_phonetic": "",
    "new_dialect_audio": ""
  }
]
```

也可使用与「数据库」页导出相同的字段名；记音、音频路径可选。

## 录音文件放哪里、怎么命名

放在：

- `public/audio/old_dialect/`
- `public/audio/new_dialect/`

文件名需与表内 **四位 `code`**、**`word`（普通话词）** 一致，**扩展名小写 `.mp3`**。支持两种分隔（页面会**先试空格版，失败再试下划线版**）：

- 空格：`0001 新派 太阳.mp3`、`0001 老派 太阳.mp3`
- 下划线：`0001_新派_太阳.mp3`、`0001_老派_太阳.mp3`（适合早期已录好的文件）

**建议 0016 条之后统一用空格命名**，更易读；前若干条若已是下划线无需重命名。

GitHub 上路径区分大小写，请与本地完全一致。

## 更新数据后

修改 JSON 或替换 MP3 后 **提交并推送**，等 GitHub Actions 部署完成；访问网站时建议 **强制刷新**（Ctrl+F5）或清空本站缓存，以免旧版 `dialect-words.json` 被缓存。

## 与本地导入的关系

每次打开网站都会尝试拉取 `data/dialect-words.json`；**成功则覆盖**当前浏览器里该站的语料缓存（`localStorage`）。若文件不存在或拉取失败，则保留你之前在「数据库」页用 JSON/CSV 导入的内容。
