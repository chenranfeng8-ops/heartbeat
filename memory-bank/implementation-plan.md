# 实施计划

## 目标
将 heartbeat.py（888 行单体文件）重构为模块化项目结构。

---

## 第 1 步：拆分导入和配置 → config.py
- 将所有常量（RATIO、ecgClassSet、数据路径等）提取到 `config.py`
- 清理重复导入（numpy 被导入 3 次）
- **验证**：`python -c "from config import *; print(ECG_CLASS_SET)"` 无报错

## 第 2 步：拆分串口/网络工具 → communication.py
- 提取 `UDP()` 函数
- 提取串口配置代码（当前已注释，保留为可选功能）
- 提取 `generate_multichannel_data()` 和 `generate_multichannel_data_test()`
- **验证**：`python -c "from communication import UDP"` 无报错

## 第 3 步：拆分信号预处理 → preprocessing.py
- 提取 `denoise()` 函数（小波去噪）
- 提取 `preprocessing()` 函数（AIF360 Reweighing）
- 去除 `pre()` 的嵌套函数结构，改为模块级函数
- **验证**：用模拟数据调用 `denoise()`，输出形状正确

## 第 4 步：拆分数据集加载 → dataset.py
- 提取 `getDataSet()` 函数
- 提取 `loadData()` 函数
- 提取 `CustomDataset` 类
- 提取 `generate_ecg_data()` 函数
- **验证**：`loadData()` 能成功加载 MIT-BIH 数据并返回训练/测试集

## 第 5 步：拆分模型定义 → model.py
- 提取 `CustomAdversarialDebiasing` 类
- 清理 TensorFlow 兼容性代码
- **验证**：模型可实例化，不报错

## 第 6 步：拆分训练/评估流程 → train.py
- 提取训练循环代码
- 提取评估指标打印代码
- 分离有/无 debiasing 的训练流程
- **验证**：`python train.py` 能运行完整训练流程

## 第 7 步：创建主入口 → main.py
- 协调所有模块的调用流程
- 添加命令行参数支持（可选）
- **验证**：`python main.py` 一键运行全流程

---

## 注意事项
- 每步完成后运行验证，确认不引入新 bug
- 每步完成后更新 `progress.md` 和 `architecture.md`
- 保留原始 `heartbeat.py` 作为备份参考
