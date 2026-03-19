# 技术栈说明

## 编程语言
- Python 3.x

## 核心依赖

### 信号处理
| 库 | 用途 |
|---|---|
| `wfdb` | MIT-BIH 心律失常数据库读取 |
| `pywt` (PyWavelets) | 小波变换去噪 |
| `numpy` | 数值计算 |
| `scipy` | 科学计算（softmax 等） |

### 机器学习 / 深度学习
| 库 | 用途 |
|---|---|
| `torch` (PyTorch) | 自定义 Dataset |
| `tensorflow` 1.x 兼容模式 | RNN 模型 + Adversarial Debiasing |
| `keras` (via tf) | 层定义 |
| `scikit-learn` | 数据预处理、评估工具 |

### 公平性
| 库 | 用途 |
|---|---|
| `aif360` | AI Fairness 360 —— 公平性指标 + 去偏算法 |
| `aif360.algorithms.preprocessing.Reweighing` | 预处理去偏 |
| `aif360.algorithms.inprocessing.AdversarialDebiasing` | 训练中去偏 |

### 数据处理
| 库 | 用途 |
|---|---|
| `pandas` | DataFrame 构建（BinaryLabelDataset 输入） |
| `csv` | CSV 文件读写 |

### 可视化
| 库 | 用途 |
|---|---|
| `matplotlib` | Python 端绘图 |
| `seaborn` | 统计可视化 |
| `matlab.engine` | MATLAB 引擎（信号可视化） |

### 通信
| 库 | 用途 |
|---|---|
| `serial` (pyserial) | 串口数据采集 |
| `socket` | UDP 数据传输 |

### 其他
| 库 | 用途 |
|---|---|
| `tqdm` | 进度条 |
| `struct` / `binascii` | 数据格式转换 |

## 数据集
- MIT-BIH Arrhythmia Database v1.0.0
- 路径：`D:\heartbeat\mit-bih-arrhythmia-database-1.0.0`
- 48 条半小时双导联心电记录

## 运行环境
- OS: Windows
- IDE: VS Code
- MATLAB: 需安装并配置 matlab.engine for Python
