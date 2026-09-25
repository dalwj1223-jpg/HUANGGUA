# 千岛 - 夏日跳跳乐 (CodeX 部署工程包)

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
