# Heartbeat 项目 AI Agent 行为规则

> 本文件为 AI Agent 提供项目操作手册与约束清单。
> AI 在每次对话开始时**必须**先读取本文件和 `memory-bank/` 目录下所有文件。

---

## 1. 项目概述

**Heartbeat** 是一个 ECG（心电图）信号处理与公平性分析项目，核心功能：
- 从 MIT-BIH 心律失常数据库读取心电数据
- 小波去噪预处理（db5 小波）
- R 峰检测与心拍分割（300 采样点/心拍）
- 基于 AIF360 的公平性约束（Reweighing + Adversarial Debiasing）
- RNN 分类器（N/A/V/L/R 五分类）
- 串口数据采集 + UDP 传输 + MATLAB 可视化

**技术栈：** Python, PyTorch, TensorFlow 1.x (兼容模式), AIF360, wfdb, pywt, MATLAB Engine, NumPy, Pandas, scikit-learn

---

## 2. 必须遵守的规则

### 写代码前
- [ ] 完整阅读 `memory-bank/` 里所有文件
- [ ] 阅读 `memory-bank/progress.md` 了解当前进度
- [ ] 确认当前要做的任务在 `memory-bank/implementation-plan.md` 中有对应步骤

### 写代码时
- [ ] 严格模块化，**禁止单体巨文件**（单文件不超过 300 行）
- [ ] 函数单一职责，每个函数只做一件事
- [ ] 使用有意义的变量名（`ecg_signal` 不用 `data`，`denoised_signal` 不用 `rdata`）
- [ ] 为复杂逻辑添加注释，说明"为什么"而非"做什么"
- [ ] 不得硬编码路径，使用 `os.path.join()` 和配置变量
- [ ] 不得重复导入（当前 heartbeat.py 中 numpy 被导入了 3 次）
- [ ] 不得引入未使用的依赖

### 写完代码后
- [ ] 更新 `memory-bank/progress.md` 记录完成了什么
- [ ] 更新 `memory-bank/architecture.md` 说明新文件/修改的作用
- [ ] 在我确认测试通过前**不要**开始下一步

---

## 3. 项目特定约束

### 数据集
- MIT-BIH 数据路径：`D:\heartbeat\mit-bih-arrhythmia-database-1.0.0`
- ECG 分类标签：`['N', 'A', 'V', 'L', 'R']`
- 心拍长度：300 采样点（R 峰前 100 + R 峰后 200）
- 测试集比例：`RATIO = 0.2`

### 公平性
- 保护属性：年龄（age），阈值 30 岁
- 特权组：`age >= 30`（编码为 1）
- 非特权组：`age < 30`（编码为 0）
- 去偏方法：预处理（Reweighing）+ 训练中（Adversarial Debiasing）

### MATLAB 联动
- 用于信号可视化（6 导联子图）
- 通过 `matlab.engine` 调用

---

## 4. 参考文档位置

| 需要什么 | 读哪个文件 |
|---|---|
| AI 行为规则 | `AGENTS.md`（本文件） |
| 当前进度 | `memory-bank/progress.md` |
| 架构说明 | `memory-bank/architecture.md` |
| 实施计划 | `memory-bank/implementation-plan.md` |
| 编码红线 | `CONSTRAINT/rules/强前置条件约束.md` |
| 模块化规范 | `CONSTRAINT/rules/代码组织.md` |
| 开发经验 | `CONSTRAINT/rules/开发经验.md` |
| 常见问题 | `CONSTRAINT/rules/常见坑汇总.md` |
| 操作手册 | `CONSTRAINT/vibe-coding-实战示例.md` |

---

## 5. Git 提交规范

```
feat|fix|docs|refactor: scope - summary

示例：
- feat: preprocessing - add wavelet denoise module
- fix: dataset - handle missing MLII lead gracefully
- refactor: model - extract adversarial debiasing to model.py
- docs: memory-bank - update progress after step 3
```
