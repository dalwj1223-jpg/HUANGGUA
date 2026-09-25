import os
import glob
import zipfile
import shutil

def build_offline():
    dist_dir = 'dist'
    if not os.path.exists(dist_dir):
        print("dist directory does not exist")
        return

    # Find CSS and JS in dist
    css_files = glob.glob(os.path.join(dist_dir, '*.css'))
    js_files = glob.glob(os.path.join(dist_dir, '*.js'))

    if not css_files or not js_files:
        print("CSS or JS file not found in dist")
        return

    css_path = css_files[0]
    js_path = js_files[0]

    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()

    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    # Base HTML template for 100% offline standalone execution
    html = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
    <title>千岛 - 夏日跳跳乐 (离线单文件版)</title>
    <meta name="description" content="千岛 - 夏日跳跳乐：完全离线运行的水上跳跃游戏，踩踏浮板避开红色陷阱方块。" />
    <style>
      /* Fallback system fonts for complete offline environments */
      html, body {{
        margin: 0;
        padding: 0;
        background-color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
        -webkit-user-select: none;
        user-select: none;
        overflow: hidden;
      }}
      {css}
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script>
{js}
    </script>
  </body>
</html>"""

    # 1. Save as dist/index.html (the primary bundle)
    with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    # 2. Save as dist/offline_game.html
    with open(os.path.join(dist_dir, 'offline_game.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    # 3. Save as root offline_game.html and public copies
    with open('offline_game.html', 'w', encoding='utf-8') as f:
        f.write(html)

    if os.path.exists('public'):
        with open('public/offline_game.html', 'w', encoding='utf-8') as f:
            f.write(html)

    # 4. Pack into dist.zip
    with zipfile.ZipFile('dist.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(dist_dir, 'index.html'), 'index.html')
        z.write(os.path.join(dist_dir, '.nojekyll'), '.nojekyll')
        z.write(os.path.join(dist_dir, 'offline_game.html'), 'offline_game.html')
        z.write(css_path, os.path.basename(css_path))
        z.write(js_path, os.path.basename(js_path))

    # ==============================================================
    # 5. Build Codex Project Folder (codex_project)
    # ==============================================================
    codex_dir = 'codex_project'
    if os.path.exists(codex_dir):
        shutil.rmtree(codex_dir)
    os.makedirs(codex_dir, exist_ok=True)

    # Copy src directory
    shutil.copytree('src', os.path.join(codex_dir, 'src'))

    # Clean package.json for standard Node/Vite environments
    codex_package_json = """{
  "name": "qiandao-summer-jump",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tailwindcss/vite": "^4.1.14",
    "@vitejs/plugin-react": "^5.0.4",
    "lucide-react": "^0.546.0",
    "motion": "^12.23.24",
    "react": "^19.0.1",
    "react-dom": "^19.0.1",
    "tailwindcss": "^4.1.14",
    "vite": "^6.2.3"
  },
  "devDependencies": {
    "@types/react": "^19.0.10",
    "@types/react-dom": "^19.0.4",
    "typescript": "~5.8.2"
  }
}
"""
    with open(os.path.join(codex_dir, 'package.json'), 'w', encoding='utf-8') as f:
        f.write(codex_package_json)

    # Clean vite.config.ts
    codex_vite_config = """import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  plugins: [react(), tailwindcss()],
  build: {
    outDir: 'dist',
    assetsDir: '',
    emptyOutDir: true,
  },
});
"""
    with open(os.path.join(codex_dir, 'vite.config.ts'), 'w', encoding='utf-8') as f:
        f.write(codex_vite_config)

    # Clean tsconfig.json
    codex_tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": false,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": false,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""
    with open(os.path.join(codex_dir, 'tsconfig.json'), 'w', encoding='utf-8') as f:
        f.write(codex_tsconfig)

    # Root index.html for Vite development
    with open('index.html', 'r', encoding='utf-8') as f:
        dev_index_html = f.read()
    with open(os.path.join(codex_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(dev_index_html)

    # Pre-built standalone html for direct zero-install execution
    with open(os.path.join(codex_dir, 'standalone.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    # Pre-built dist directory inside codex_project so it is ready-to-deploy immediately
    codex_dist_dir = os.path.join(codex_dir, 'dist')
    os.makedirs(codex_dist_dir, exist_ok=True)
    with open(os.path.join(codex_dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    shutil.copy(css_path, os.path.join(codex_dist_dir, os.path.basename(css_path)))
    shutil.copy(js_path, os.path.join(codex_dist_dir, os.path.basename(js_path)))
    with open(os.path.join(codex_dist_dir, '.nojekyll'), 'w') as f:
        pass

    # .gitignore for codex
    with open(os.path.join(codex_dir, '.gitignore'), 'w', encoding='utf-8') as f:
        f.write("node_modules/\ndist/\n*.zip\n.DS_Store\n")

    # README.md for CodeX
    codex_readme = """# 千岛 - 夏日跳跳乐 (CodeX 部署工程包)

这是一个适配 375×812 移动端与全平台游玩的清凉水上跳跃游戏。包含动态物理跳跃、红色尖刺陷阱方块、清爽水球射击机制、小章鱼与粉红水母、连击得分与 Web Audio 8-bit 和弦音效。

---

## 📁 目录结构

```text
codex_project/
├── dist/                # ⚡ 预编译好的生产产物（直接部署用它即可！）
│   ├── index.html       # 包含全部逻辑与样式的开箱即用网页
│   ├── index-*.css      # 独立样式
│   └── index-*.js       # 独立逻辑脚本
├── src/                 # 💻 完整 TypeScript + React 源码
│   ├── components/      # 游戏画面与渲染逻辑组件
│   │   ├── DoodleGame.tsx
│   │   ├── characterRenderer.ts
│   │   ├── worldRenderer.ts
│   │   └── QiandaoLogo.tsx
│   ├── audio.ts         # Web Audio API 合成音效引擎
│   ├── gameEngine.ts    # 物理弹跳、碰撞、生成与射击引擎
│   ├── types.ts         # 类型定义
│   ├── App.tsx          # 界面根组件
│   └── main.tsx         # React 入口
├── standalone.html      # 100% 纯脱机单文件版本（双击直接在任何浏览器运行）
├── index.html           # Vite 开发服务入口
├── package.json         # 项目依赖与运行脚本
├── vite.config.ts       # Vite 构建配置（相对路径 base: './'）
└── tsconfig.json        # TypeScript 编译配置
```

---

## 🚀 部署与运行方法（支持 3 种方式）

### 方式 1：在 CodeX 或静态托管中直接部署（最简单，零配置）
直接使用项目根目录下的 `standalone.html` 或 `dist/` 文件夹：
- 将 `dist/` 内的文件（或 `standalone.html` 重命名为 `index.html`）上传到你的托管平台或 CodeX 静态站点。
- 无需安装 Node.js，无需任何编译步骤，直接上线访问！

### 方式 2：在 CodeX / 本地开发环境中运行与调试
如果你在支持 Node.js 的 CodeX 或本地终端环境：
1. **安装依赖**：
   ```bash
   npm install
   ```
2. **启动本地开发服务器**：
   ```bash
   npm run dev
   ```
   启动后打开控制台输出的本地链接（例如 `http://localhost:5173`）即可热重载开发。

3. **重新打包构建**：
   ```bash
   npm run build
   ```
   打包完成后产物将输出在 `dist/` 目录中。

---

## 🎮 操作说明
- **移动**：
  - 键盘 `A` / `D` 或左右方向键 `←` / `→`
  - 手机触屏底部左右按钮，或直接在屏幕上左右滑动
- **发射水球**：
  - 键盘 `空格键` 或鼠标点击屏幕
  - 手机触屏底部粉红色“发射水球”按钮
- **静音/暂停**：点击右上角快捷按键。
"""
    with open(os.path.join(codex_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(codex_readme)

    # ==============================================================
    # 6. Build Codex Static Package (codex_static)
    # ==============================================================
    static_dir = 'codex_static'
    if os.path.exists(static_dir):
        shutil.rmtree(static_dir)
    os.makedirs(static_dir, exist_ok=True)
    with open(os.path.join(static_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    static_readme = """# 千岛 - 夏日跳跳乐 (CodeX 极速静态部署包)

这是一个 100% 纯脱机、零外部依赖的单文件完整网页应用。

## 部署说明：
1. 直接将本文件夹内的 `index.html` 部署到 CodeX 或任意静态 Web 服务器（如 GitHub Pages、Vercel、Netlify、Nginx 等）。
2. 也可无需服务器，直接在本地电脑双击 `index.html` 离线畅玩！
"""
    with open(os.path.join(static_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(static_readme)

    # ==============================================================
    # 7. Zip Packages (codex_project.zip & codex_static.zip)
    # ==============================================================
    def zip_folder(folder_path, output_zip_path):
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, folder_path)
                    zipf.write(full_path, rel_path)

    zip_folder(codex_dir, 'codex_project.zip')
    zip_folder(static_dir, 'codex_static.zip')

    # Copy zips and htmls to public and dist directories for browser download
    targets = ['public', 'dist']
    for t in targets:
        if os.path.exists(t):
            shutil.copy('codex_project.zip', os.path.join(t, 'codex_project.zip'))
            shutil.copy('codex_static.zip', os.path.join(t, 'codex_static.zip'))
            shutil.copy('dist.zip', os.path.join(t, 'dist.zip'))

    print("Offline standalone HTML built successfully! Size:", len(html.encode('utf-8')), "bytes")
    print("CodeX packages created: codex_project/, codex_static/, codex_project.zip, codex_static.zip")

if __name__ == '__main__':
    build_offline()

