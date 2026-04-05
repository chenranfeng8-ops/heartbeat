# 架构说明

## 文档新增（2026-04-05）

### 文件：软件说明书.md

| 内容 | 说明 |
|---|---|
| 文档类型 | 用户向软件说明书 |
| 覆盖范围 | 系统概览、安装运行、功能操作、故障排除、安全维护 |
| 章节结构 | 按 7 个核心部分组织，支持检索式阅读 |
| 配图策略 | 每个关键操作提供截图占位，便于后续补图 |
| 表达风格 | 去技术化描述，强调“用户动作 + 成功判据” |

## 当前架构（单体 heartbeat.py）

### 文件：heartbeat.py（888 行）

| 行号 | 内容 | 职责 |
|---|---|---|
| 1-56 | 导入语句 | 导入所有依赖（有重复导入） |
| 57-96 | 串口配置（已注释） | 串口数据采集（未启用） |
| 97-111 | `UDP()` | UDP 数据发送 |
| 112-121 | `generate_multichannel_data()` | 多通道数据序列化 |
| 122-200 | `pre()` → `denoise()` | 小波去噪（db5，9 层分解） |
| 201-290 | `pre()` → `preprocessing()` | AIF360 公平性预处理（Reweighing） |
| 291-400 | `pre()` → `getDataSet()` | MIT-BIH 数据读取与心拍分割 |
| 401-450 | `pre()` → `loadData()` | 数据加载、打乱、训练/测试集划分 |
| 451-480 | ECG 模拟数据生成 + 调用 | 测试用模拟数据 |
| 481-530 | `CustomDataset` 类 | 自定义数据集（features + labels + prot_attr） |
| 531-700 | `CustomAdversarialDebiasing` 类 | 自定义对抗去偏模型（RNN + Adversary） |
| 701-888 | 训练与评估流程（大部分已注释） | 模型训练、预测、公平性指标评估 |

### 存在的问题
- 所有代码在一个文件中，难以维护
- `pre()` 函数内嵌套定义了 4 个子函数，作用域混乱
- numpy 被导入 3 次
- 硬编码路径 `D:\heartbeat\mit-bih-arrhythmia-database-1.0.0`
- 变量命名不清晰（`rdata`、`n`、`t`）

## 目标架构（重构后）

```
heartbeat/
├── config.py              ← 常量、路径、超参数
├── communication.py       ← UDP 发送、串口通信
├── preprocessing.py       ← 小波去噪、AIF360 公平性预处理
├── dataset.py             ← MIT-BIH 数据读取、CustomDataset
├── model.py               ← CustomAdversarialDebiasing 模型
├── train.py               ← 训练循环、评估指标
├── main.py                ← 主入口
├── AGENTS.md              ← AI 规则
├── CONSTRAINT/            ← 约束与参考文档
└── memory-bank/           ← 记忆库
```
