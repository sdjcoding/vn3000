# VN 3000 越南语闪卡项目

## 项目名：VN 3000 Flash（越南语 3000 词闪卡）

---

## 现在状态：本地 MVP 完成 ✅ · 待部署

| 项目 | 内容 |
|------|------|
| 当前阶段 | Batch 1（300 词）本地版完成 |
| 目标规模 | 3000 词（分 10 个 Batch 陆续合并） |
| 线上地址（待部署） | https://sdjcoding.github.io/vn3000/（或 vn-flash） |
| GitHub 账号 | sdjcoding |

---

## 功能要点

- **正面：** 越南语单词（最大）· 日语单词（中，含 `<ruby>` 振り仮名）· 英语单词（最小）
- **背面：** 越南语例句（最大）· 日语例句（中，含振り仮名）· 英语例句（最小）
- **交互：** 点击/Space 翻面；←/→ 或 手机滑动 切换；
- **分类筛选：** All / Core / Business / Daily
- **学习数据：** 收藏 (⭐) · 已掌握 (✓) · 当前位置 · 主题偏好（localStorage）
- **视图切换：** 只看收藏 · 隐藏已掌握 · 一键清除所有标记
- **深色模式：** 自动跟随系统或手动切换

---

## 本地开发

```bash
# 在仓库根目录（Claude Code Dropbox 根目录）
python3 -m http.server 8765 --directory "VN 3000"
# 浏览 http://localhost:8765/flashcard.html
```

或通过 Claude Code preview（已配置 `.claude/launch.json` 的 `vn3000` 条目）。

---

## 数据来源与注入

原始数据：[`files22/Vietnamese_3000_Batch1_300.html`](files22/Vietnamese_3000_Batch1_300.html) 第 76 行 `const D=[...]`，300 项。

注入 `flashcard.html` 的占位符 `/* __DATA_ARRAY_PLACEHOLDER__ */`（已注入，无需重复）。之后有新 Batch 时，可用同样脚本替换：

```python
# 替换 flashcard.html 中的 const D=[...] 为新数据
import re
src = open("files22/Vietnamese_3000_Batch2_XXX.html", encoding="utf-8").read()
data_line = re.search(r'const D=\[.*?\];', src, re.DOTALL).group(0)
html = open("flashcard.html", encoding="utf-8").read()
html = re.sub(r'const D=\[.*?\];', data_line, html, count=1, flags=re.DOTALL)
open("flashcard.html", "w", encoding="utf-8").write(html)
```

数据字段：`no / cat (Core|Business|Daily) / freq (A|B|C) / vn / vn_ex / jp / jp_ex / en / en_ex / tag`

---

## 部署方法（GitHub Pages · 参考 KIIP）

```bash
# 1. GitHub CLI 登录（若未登录）
gh auth login --web -h github.com -p https

# 2. 新建仓库
gh repo create sdjcoding/vn3000 --public --description "Vietnamese 3000 flashcards (VN·JP·EN)"

# 3. 准备部署目录（flashcard.html 要重命名为 index.html）
cd "VN 3000"
git init
git branch -M main
cp flashcard.html index.html     # GitHub Pages 需 index.html
git add index.html flashcard.html CLAUDE.md
git commit -m "Initial VN 3000 flashcard (300 items)"
git remote add origin https://github.com/sdjcoding/vn3000.git
git push -u origin main

# 4. 开启 GitHub Pages（main 分支 / root）
gh repo edit sdjcoding/vn3000 --enable-pages --pages-branch main --pages-path /
# 若上面不行，用网页开启：Settings → Pages → Source: main / root
```

**注意：**
- GitHub Pages 根目录识别的是 `index.html`，所以部署时 `flashcard.html` 需要复制/重命名为 `index.html`
- 修改后推送 `git push`，GitHub Pages 几分钟内自动重新部署

---

## 文件结构

```
VN 3000/
├── CLAUDE.md                                       # ← 本文件
├── flashcard.html                                  # 主应用（内嵌 300 项数据）
├── files22/                                        # 第一批 300 项数据源
│   ├── Vietnamese_3000_Batch1_300.html             # ★ 数据源（第 76 行 const D=[...]）
│   └── Vietnamese_3000_Batch1_300.xlsx
└── files/
    └── Vietnamese_3000_RichText_Sample100.html     # 早期 100 项样本（保留）
```

---

## 对象用户

- 母语：可能是中文/韩语
- 学习目标：越南语（通过日语+英语对照辅助）
- 用途：商务、日常、核心词汇三类分级学习

---

## 技术栈

- **前端：** 单个 HTML 文件（HTML + CSS + Vanilla JS），无构建
- **持久化：** 浏览器 localStorage（key: `vn3k_state`）
- **托管：** GitHub Pages
- **尺寸：** 单文件约 97 KB（内嵌 300 项数据 + 完整 UI 逻辑）

---

## localStorage 数据结构

```js
// key: "vn3k_state"
{
  version: 1,
  position: 121,          // 当前卡片 no
  category: "Core",       // "all" | "Core" | "Business" | "Daily"
  hideMastered: false,
  onlyBookmarked: false,
  mastered: [1, 3, 7],    // 已掌握的 no 列表
  bookmarked: [5, 12],    // 收藏的 no 列表
  theme: "dark"           // "light" | "dark"
}
```

---

## 未来可能的扩展

- [ ] 合并 Batch 2–10 → 完整 3000 项
- [ ] 越南语 TTS 音频（复用 KIIP 的 Inworld AI API Key）
- [ ] 频率 (A/B/C) 和标签 (Greeting/Meal/Number 等) 多维筛选
- [ ] 间隔重复 SRS 算法（Anki 风格复习排程）
- [ ] 学习统计报表
- [ ] 录音跟读对比
- [ ] PWA 离线支持

---

## 相关项目

- KIIP 4단계 구술시험 플래시카드：[`../KIIP/CLAUDE.md`](../KIIP/CLAUDE.md) · [线上](https://sdjcoding.github.io/kiip-study/)
