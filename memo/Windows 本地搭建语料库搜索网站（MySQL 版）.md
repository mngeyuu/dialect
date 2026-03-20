### **Windows 本地搭建语料库搜索网站（MySQL 版）**



。

------

## **1. 安装开发环境**

### **1.1 安装 MySQL**

1. **下载 MySQL Installer**
   - 访问 [MySQL 官网](https://dev.mysql.com/downloads/installer/)
   - 选择 **MySQL Community Server**，下载并安装
2. **安装时选择组件**：
   - 必选：
     - **MySQL Server**（数据库服务器）
     - **MySQL Workbench**（可视化管理工具）
   - 可选：
     - **MySQL Shell**（命令行管理）
3. **设置 MySQL 配置**
   - 选择 **开发者默认（Developer Default）** 安装类型
   - **设置 root 密码**（务必记住！）
   - 创建一个数据库（比如 `corpus_db`）

------

### **1.2 安装 Python 和 Django**

1. **安装 Python（如果未安装）**

   - 访问 [Python 官网](https://www.python.org/downloads/) 下载并安装

   - 安装时 **勾选 "Add Python to PATH"**

   - 安装后打开 

     终端（CMD）

     ，输入：

     ```bash
     python --version
     ```

     确保安装成功

2. **安装 Django**

   - 运行：

     ```bash
     pip install django mysqlclient
     ```

3. **创建 Django 项目**

   - 运行：

     ```bash
     python -m django startproject corpus_search
     cd corpus_search
     python manage.py startapp search
     ```

------

## **2. 配置数据库**

### **2.1 修改 `settings.py`**

在 `corpus_search/settings.py` 里，找到 `DATABASES`，改成：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'corpus_db',
        'USER': 'root',
        'PASSWORD': '你的MySQL密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### **2.2 运行数据库迁移**

```bash
python manage.py migrate
```

如果没有报错，说明 MySQL 连接成功！

------

## **3. 处理 Excel 和 MP3 数据**

### **3.1 解析 Excel 数据**

Django 可以用 **pandas** 读取 Excel 数据：

```bash
pip install pandas openpyxl
```

在 `search/views.py` 里写一个导入 Excel 数据的函数：

```python
import pandas as pd
from search.models import CorpusEntry

def import_excel(file_path):
    df = pd.read_excel(file_path, engine="openpyxl")
    for _, row in df.iterrows():
        CorpusEntry.objects.create(
            number=row["编号"],
            word=row["词汇"],
            old_word=row["老派词汇"],
            new_word=row["新派词汇"]
        )
```

### **3.2 处理 MP3 文件**

Django **不存储 MP3 到数据库**，而是保存 **文件路径**：

1. 在 `models.py` 里添加字段

   ：

   ```python
   from django.db import models
   
   class CorpusEntry(models.Model):
       number = models.CharField(max_length=10)
       word = models.CharField(max_length=100)
       old_word = models.CharField(max_length=100, null=True, blank=True)
       new_word = models.CharField(max_length=100, null=True, blank=True)
       audio = models.FileField(upload_to="audios/", null=True, blank=True)
   ```

2. 上传 MP3

   在 

   ```
   views.py
   ```

    里创建上传功能：

   ```python
   from django.shortcuts import render
   from .models import CorpusEntry
   from django.core.files.storage import FileSystemStorage
   
   def upload_audio(request):
       if request.method == "POST" and request.FILES["audio"]:
           audio_file = request.FILES["audio"]
           fs = FileSystemStorage()
           filename = fs.save(f"audios/{audio_file.name}", audio_file)
           return render(request, "upload.html", {"filename": filename})
       return render(request, "upload.html")
   ```

------

## **4. 创建搜索接口**

### **4.1 在 `views.py` 里添加搜索功能**

```python
from django.shortcuts import render
from .models import CorpusEntry

def search(request):
    query = request.GET.get("q", "")
    results = CorpusEntry.objects.filter(word__icontains=query)
    return render(request, "search.html", {"results": results})
```

### **4.2 在 `urls.py` 里注册路由**

```python
from django.urls import path
from .views import search, upload_audio

urlpatterns = [
    path("search/", search, name="search"),
    path("upload/", upload_audio, name="upload"),
]
```

------

## **5. 运行项目**

1. 创建超级用户（管理后台）

   ```bash
   python manage.py createsuperuser
   ```

2. 启动 Django 服务器

   ```bash
   python manage.py runserver
   ```

3. 访问管理后台

   打开浏览器，访问：

   ```
   http://127.0.0.1:8000/admin
   ```

------

## **6. 创建前端界面（可选）**

如果你希望做一个更现代的前端，可以：

- **使用 HTML + JavaScript（简单）**
- **用 React / Vue（更强大）**
- **用 Bootstrap 让界面更好看**

**示例搜索页面 `search.html`**

```html
<form action="{% url 'search' %}" method="GET">
    <input type="text" name="q" placeholder="输入词汇...">
    <button type="submit">搜索</button>
</form>

{% if results %}
    <ul>
    {% for entry in results %}
        <li>{{ entry.word }}（老派：{{ entry.old_word }}，新派：{{ entry.new_word }}）
            {% if entry.audio %}
                <audio controls><source src="{{ entry.audio.url }}" type="audio/mpeg"></audio>
            {% endif %}
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>未找到结果</p>
{% endif %}
```

------

## **7. 总结**

### **你已经完成的内容**

✅ 安装 MySQL 并创建数据库
 ✅ 配置 Django 连接 MySQL
 ✅ 解析 Excel 并存入数据库
 ✅ 处理 MP3 文件并存储路径
 ✅ 创建搜索功能
 ✅ 启动 Django 服务器并测试

------

## **下一步（可选）**

🔹 **前端优化**（React/Vue/Bootstrap）
 🔹 **改进搜索功能**（拼音搜索、模糊匹配）
 🔹 **支持 MP3 批量上传**

如果你需要进一步指导，欢迎随时问我！😊