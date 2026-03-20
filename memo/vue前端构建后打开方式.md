### **3. 本地直接打开 `index.html`**

如果你 **双击 `dist/index.html` 在浏览器中打开**，Vue 资源路径会失效，导致 JS 无法加载。Vue 需要在**本地服务器**运行，而不是 `file://` 方式。

#### **✅ 解决方案**

用 `npx serve` 启动本地服务器：

```sh
npx serve dist
```

然后在浏览器中访问：

```
http://localhost:5000/
```

------

