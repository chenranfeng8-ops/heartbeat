# Vibe Coding 实战示例：heartbeat ECG 项目适配版

> 本文档基于 [vibe-coding-constraint](https://github.com/chenranfeng8-ops/vibe-coding-constraint) 仓库，
> 针对 heartbeat（ECG 信号处理 + 公平性去偏 + RNN 分类）项目定制。
> **核心理念：用 `.md` 文件当"外挂记忆"，每次对话让 AI 先读文件再干活，干完更新文件，下次再读。**

---

## 目录结构说明：仓库文件放在哪里

```
heartbeat/                          ← 你的项目根目录
├── heartbeat.py                    ← 主代码（当前单体文件，后续需拆分）
├── AGENTS.md                       ← 【新建】AI 行为规则（每次对话 AI 必读）
├── CONSTRAINT/                     ← 【约束仓库内容存放处】
│   ├── vibe-coding-实战示例.md      ← 本文件（操作手册）
│   ├── rules/                      ← 从仓库提取的规则文档
│   │   ├── 强前置条件约束.md         ← AI 编码红线
│   │   ├── 代码组织.md              ← 模块化原则
│   │   ├── 开发经验.md              ← 编码规范
│   │   └── 常见坑汇总.md            ← 避坑手册
│   └── skills/                     ← 技能文件（按需添加）
│       └── README.md               ← 技能索引
├── memory-bank/                    ← 【新建】AI 记忆库
│   ├── prd.md                      ← 产品需求文档
│   ├── tech-stack.md               ← 技术栈说明
│   ├── implementation-plan.md      ← 分步实施计划
│   ├── progress.md                 ← 进度追踪
│   └── architecture.md             ← 架构说明（每个文件/模块的作用）
└── mit-bih-arrhythmia-database-1.0.0/  ← 数据集（已有）
```

### 放置原则

| 仓库中的内容 | 放到项目的位置 | 原因 |
|---|---|---|
| `AGENTS.md` | **项目根目录** `heartbeat/AGENTS.md` | AI 每次启动时自动读取根目录的 AGENTS.md |
| 方法论文档（开发经验/代码组织/避坑等） | `CONSTRAINT/rules/` | 作为 AI 的参考手册，需要时指定读取 |
| Skills（技能文件） | `CONSTRAINT/skills/` | 按需放入，大多数与你项目无关 |
| Memory Bank 模板 | `memory-bank/` | 项目自身的记忆，不放在 CONSTRAINT 下 |

---

## 第 0 步：一次性配置（只做一次）

### 0.1 创建 AGENTS.md（项目根目录）

在 `heartbeat/AGENTS.md` 中写入 AI 行为规则。这是**最关键的文件**——
支持 AGENTS.md 的 AI 工具（Claude Code、Codex CLI、GitHub Copilot）会在每次对话开始时自动读取它。

**你不需要手动粘贴任何内容。** AI 启动后会自动加载 AGENTS.md 中的规则。

### 0.2 创建 memory-bank 目录

memory-bank 里的文件是你项目特有的，需要你和 AI 一起生成：

```
提示词（给 AI）：
───────────────────
阅读 heartbeat.py 的全部代码，然后：
1. 生成 memory-bank/prd.md —— 描述这个项目要做什么
2. 生成 memory-bank/tech-stack.md —— 列出所有技术栈和依赖
3. 生成 memory-bank/architecture.md —— 说明每个函数/类的作用
4. 生成 memory-bank/implementation-plan.md —— 将代码重构为模块化的分步计划
5. 生成 memory-bank/progress.md —— 初始为空，标记"尚未开始"
```

### 0.3 下载规则文档到 CONSTRAINT/rules/

可以手动下载（浏览器访问 raw 链接 → 另存为），也可以用命令行：

```powershell
# PowerShell 一键下载（在项目根目录执行）
$base = "https://raw.githubusercontent.com/chenranfeng8-ops/vibe-coding-constraint/develop/assets/documents/principles/fundamentals"
$dest = "CONSTRAINT/rules"

# 如果目录不存在则创建
New-Item -ItemType Directory -Force -Path $dest

# 下载四个核心文档
@(
    @{Name="强前置条件约束.md"; Url="$base/%E5%BC%BA%E5%89%8D%E7%BD%AE%E6%9D%A1%E4%BB%B6%E7%BA%A6%E6%9D%9F.md"},
    @{Name="代码组织.md";       Url="$base/%E4%BB%A3%E7%A0%81%E7%BB%84%E7%BB%87.md"},
    @{Name="开发经验.md";       Url="$base/%E5%BC%80%E5%8F%91%E7%BB%8F%E9%AA%8C.md"},
    @{Name="常见坑汇总.md";     Url="$base/%E5%B8%B8%E8%A7%81%E5%9D%91%E6%B1%87%E6%80%BB.md"}
) | ForEach-Object {
    Invoke-WebRequest -Uri $_.Url -OutFile "$dest/$($_.Name)"
    Write-Host "已下载: $($_.Name)"
}
```

---

## 第 1 步：每次开发对话的标准开头

### 方式 A：在 VS Code Copilot Chat 中（你当前的环境）

每次新对话的**第一条消息**用这个模板：

```
请先阅读以下文件，然后执行我的任务：
1. AGENTS.md（AI 行为规则）
2. memory-bank/progress.md（当前进度）
3. memory-bank/architecture.md（架构说明）
4. memory-bank/implementation-plan.md（实施计划）

然后执行：[你的具体任务]

完成后更新 memory-bank/progress.md 和 memory-bank/architecture.md。
```

### 方式 B：如果需要引用规则文档

当你需要 AI 遵循特定规则时，在消息中追加：

```
另外请阅读 CONSTRAINT/rules/强前置条件约束.md，
严格遵守其中的约束条件来编写代码。
```

### 方式 C：如果需要使用某个 Skill

```
请先阅读 CONSTRAINT/skills/xxx/SKILL.md，
按照该技能的模式来完成任务。
```

**关键：你不需要手动粘贴文件内容。** 只需要告诉 AI 去读哪个文件路径，AI 会自动读取。

---

## 第 2 步：开发循环（每个子任务重复）

```
你（人类）                         AI                           文件变化
────────────────────────────────────────────────────────────────────────
"读 memory-bank，执行计划第N步" → 读文件 → 执行修改        → 代码变更
你验证：运行代码，检查输出      → 告诉 AI "通过/失败"     →
AI 更新记录                     →                          → progress.md 更新
── git commit ──
"读 memory-bank，继续第N+1步"  → 重复...                   → ...
```

### 每步完成后做的事

1. **运行代码验证** —— 确认功能正常
2. **告诉 AI 结果** —— "测试通过" 或 "报错了：[错误信息]"
3. **AI 更新 memory-bank** —— progress.md 记录完成了什么
4. **Git 提交** —— `git add -A && git commit -m "完成第N步：xxx"`

---

## 第 3 步：给 heartbeat 项目的具体重构任务

你的 heartbeat.py 当前是 888 行的单体文件，建议按以下顺序拆分：

### 拆分计划（参考）

| 步骤 | 目标 | 拆分出的文件 | 验证方式 |
|---|---|---|---|
| 1 | 拆分导入和配置 | `config.py` | import 不报错 |
| 2 | 拆分串口/网络工具 | `communication.py`（UDP、串口） | UDP 函数可调用 |
| 3 | 拆分信号预处理 | `preprocessing.py`（denoise、preprocessing） | 小波去噪正常运行 |
| 4 | 拆分数据集加载 | `dataset.py`（getDataSet、loadData、CustomDataset） | MIT-BIH 数据可加载 |
| 5 | 拆分模型定义 | `model.py`（CustomAdversarialDebiasing） | 模型可实例化 |
| 6 | 拆分训练/评估流程 | `train.py` | 端到端训练可运行 |
| 7 | 创建主入口 | `main.py` | 一键运行全流程 |

### 每步的提示词模板

```
阅读 memory-bank/ 所有文件和 CONSTRAINT/rules/代码组织.md，
然后执行实施计划第 [N] 步：[具体任务描述]。

要求：
- 遵循 AGENTS.md 中的规则
- 遵循 CONSTRAINT/rules/代码组织.md 的模块化原则
- 完成后更新 memory-bank/progress.md 和 architecture.md
- 在我确认测试通过前不要开始下一步
```

---

## 第 4 步：如何判断需不需要从仓库拿更多文件

### 判断标准

| 场景 | 是否需要从仓库拿文件 | 拿什么 |
|---|---|---|
| 日常开发 | **不需要** | AGENTS.md + memory-bank 已足够 |
| AI 写的代码质量差/不遵守规范 | **拿规则** | `强前置条件约束.md` 或 `代码组织.md` |
| 想让 AI 学会某个领域技能 | **拿 Skill 或自建** | 从仓库 skills/ 中挑选或用元技能生成 |
| 想用特定工作流 | **拿 workflow** | 从仓库 `assets/workflow/` 中挑选 |
| 遇到环境配置问题 | **拿避坑指南** | `常见坑汇总.md` |

### 从仓库获取文件的方式（不克隆）

**方式 1：PowerShell 直接下载单个文件**
```powershell
$url = "https://raw.githubusercontent.com/chenranfeng8-ops/vibe-coding-constraint/develop/[文件路径]"
Invoke-WebRequest -Uri $url -OutFile "CONSTRAINT/rules/[文件名]"
```

**方式 2：浏览器访问 raw 链接下载**
```
https://raw.githubusercontent.com/chenranfeng8-ops/vibe-coding-constraint/develop/assets/skills/[技能名]/SKILL.md
```

**方式 3：让 AI 帮你从 GitHub 读取内容**
```
请访问 https://raw.githubusercontent.com/chenranfeng8-ops/vibe-coding-constraint/develop/assets/skills/README.md
帮我看看有哪些 Skills 适合我的 ECG 信号处理项目。
```

---

## 第 5 步：为 heartbeat 项目自建 Skill（可选进阶）

仓库中没有 ECG/信号处理相关的现成 Skill。你可以用**元技能**让 AI 为你生成：

```
请阅读 CONSTRAINT/skills/skills-skills-SKILL.md（元技能），
然后为我的 heartbeat 项目生成一个 ECG 信号处理 Skill，覆盖：
- MIT-BIH 数据集读取（wfdb 库）
- 小波去噪（pywt 库）
- R 峰检测与心拍分割
- ECG 分类标签体系（N/A/V/L/R）
- 公平性约束（AIF360 Reweighing + AdversarialDebiasing）

输出为 CONSTRAINT/skills/ecg-processing/SKILL.md
```

---

## CONSTRAINT 目录中各文件的作用速查

| 文件 | 作用 | 何时让 AI 读取 |
|---|---|---|
| `rules/强前置条件约束.md` | 编码红线（不得做什么） | AI 写出低质量代码时 |
| `rules/代码组织.md` | 模块化、命名、注释规范 | 重构代码时 |
| `rules/开发经验.md` | 变量管理、架构原则、KISS/DRY | 项目初期设计时 |
| `rules/常见坑汇总.md` | 环境配置、依赖冲突等常见问题 | 遇到环境/依赖问题时 |
| `skills/ecg-processing/SKILL.md` | ECG 领域专用技能（自建） | 需要 AI 做 ECG 相关开发时 |

---

## 一句话总结

> **不需要克隆仓库、不需要手动粘贴。**
> 把需要的 `.md` 文件下载到 `CONSTRAINT/` 目录下，
> 然后在每次对话开头告诉 AI "请先阅读 XXX 文件"，
> AI 就会自动读取并遵循其中的规则。
> 核心流程就是：**读文件 → 干活 → 更新文件 → 下次再读。**
