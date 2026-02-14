'''
导入相关包
'''
import serial
import struct
import binascii
import socket,time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
# 导入所有需要的包
import sys
sys.path.insert(1, "../")  
import numpy as np
np.random.seed(0)
from tqdm import tqdm
import scipy.special
from aif360.datasets import GermanDataset
from aif360.metrics import ClassificationMetric,BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing
from aif360.datasets import StandardDataset
from IPython.display import Markdown, display
from aif360.datasets import BinaryLabelDataset
import matlab.engine
eng = matlab.engine.start_matlab()
import wfdb
import pywt
import seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import torch
import torch.utils.data as Data
from torch import nn
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_random_state
from sklearn.utils.validation import check_is_fitted
try:
   import tensorflow as tf
   tf.compat.v1.disable_v2_behavior()
   tf.compat.v1.disable_eager_execution()
   from tensorflow import keras
  
except ImportError as error:
    from logging import warning
    warning("{}: AdversarialDebiasing will be unavailable. To install, run:\n"
            "pip install 'aif360[AdversarialDebiasing]'".format(error))

from aif360.sklearn.utils import check_inputs, check_groups
from aif360.algorithms.inprocessing import AdversarialDebiasing
import csv
RATIO=0.2
ecgClassSet = ['N', 'A', 'V', 'L', 'R']
#下位机接入电脑号可查看型号
#修改
'''
Usart = serial.Serial(
		port = '/dev/ttyUSB0',      # 串口
		baudrate=115200,            # 波特率
		timeout = 0.001 ,
        )			# 由于后续使用read在未收全数据的时候，会按照一个timeout周期时间读取数据
                                    # 波特率115200返回数据时间大概是1ms,9600下大概是10ms
                                    # 所以读取时间设置0.001s

# 判断串口是否打开成功
if Usart.isOpen():
    print("open success")
else:
    print("open failed")
# 读取串口数据
try:
    count = serial.inWaiting()
    if count > 0:
        Read_buffer = []
        Read_buffer=serial.read(40)      #根据寄存器改变   # 我们需要读取的是40个寄存器数据，即40个字节
        # Read_data()						# 前面两行可以注释，换成后面这个函数
except KeyboardInterrupt:
     if serial != None:
         print("close serial port")
         serial.close()
         '''
#matlab engine连接
def UDP(data):
        # 创建一个UDP套接字
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #  准备接收方的地址和端口
        dest_addr = ('127.0.0.1', 1347)  #ip地址是字符串，端口号是数字
        #修改ip地址端
        #  发送数据到指定的ip和端口
        data=data.encode()
        for i in range(0,len(data),1472):
            chunk = data[i:i+1472]
            udp_socket.sendto(chunk, dest_addr)
            time.sleep(1)
        #  关闭套接字
        udp_socket.close()

def  generate_multichannel_data(data,i):
    data = data.tobytes()
    if (i<5):
      channel_data=data+b","
    else:
      channel_data=data
    return channel_data   
def  generate_multichannel_data_test(data): 
    channel_data = data.tobytes()
    return channel_data  
def pre():
# 小波去噪预处理传入六组数据[6,n]
    def denoise(data, wavelet='db5'):
        print(data.shape)
        print(data)
        num_leads = data.shape[0]
        transport_data=b""
        denoisedSet = []
        lead_names = {1: "V1", 2: "V2", 3: "V3", 4: "aVR", 5: "aVL", 6: "aVF"}
        colors= ['r', 'g', 'b', 'm', 'c', 'k']
        eng.eval("figure; hold on; grid on;", nargout=0)
        for lead_idx in range(num_leads):
                current_lead = data[lead_idx, :]
                print(current_lead)
               # print(f"does current_lead contain NAN? {np.isnan(current_lead).any()}")
                signal_length = current_lead.shape[0]
                max_level = pywt.dwt_max_level(signal_length, pywt.Wavelet(wavelet).dec_len)
                level = min(9, max_level)
                coeffs = pywt.wavedec(data=current_lead, wavelet=wavelet, level=level, mode='periodization')
                detail_coeffs = coeffs[1:]
                threshold = np.nan  # 初始化阈值
                num_detail_levels_to_thresh = 3  # 对最后 3 层细节系数进行阈值处理
                if len(detail_coeffs) >= num_detail_levels_to_thresh:
                    # 从最后一层开始，找到第一个包含有效非 NaN 值的细节层来计算阈值
                    for i in range(1, len(detail_coeffs) + 1):
                        layer = detail_coeffs[-i]
                        valid_abs_coeffs = np.abs(layer[~np.isnan(layer)])
                        if valid_abs_coeffs.size > 0:
                            threshold_base = np.median(valid_abs_coeffs) / 0.6745
                            threshold = threshold_base * np.sqrt(2 * np.log(signal_length)) * 0.1 # 减小阈值因子
                            print(f"Calculated Threshold using level {len(detail_coeffs) - i + 1}: {threshold}")
                            break
                    else:
                        print("Warning: Could not calculate a valid threshold, setting to a small value.")
                        threshold = 0.01  # 设置较一个小的默认阈值
                    print(threshold)    
                    if threshold :  #当threshold>0时方可操作 
                        '''
                        if not np.isnan(threshold):
                            for i in range(len(detail_coeffs) - num_detail_levels_to_thresh, len(detail_coeffs)):
                                print(f"Before thresholding level {i}: {detail_coeffs[i][:10]}")
                                detail_coeffs[i] = pywt.threshold(detail_coeffs[i], threshold, mode='soft')
                                print(f"After thresholding level {i}: {detail_coeffs[i][:10]}")
                        '''
                        # 对中间层进行“soft”阈值处理，使用计算出的阈值
                        if not np.isnan(threshold):
                            for coeff_idx in range(1, len(coeffs)): #- num_detail_levels_to_thresh):
                                print(f"Before thresholding level {coeff_idx}: {coeffs[coeff_idx][:10]}")
                                coeffs[coeff_idx] = pywt.threshold(coeffs[coeff_idx], threshold, mode='soft')
                                print(f"After thresholding level {coeff_idx}: {coeffs[coeff_idx][:10]}")
                            rdata = pywt.waverec(coeffs=coeffs, wavelet='db5', mode='periodization')
                            print(f"Final rdata min: {np.min(rdata)}, max: {np.max(rdata)}, mean: {np.mean(rdata)}")
                           # print(f"does rdata contain NAN? {np.isnan(rdata).any()}")
                            print(rdata.shape)
                            print(f"rdata:{rdata}")
                            print(f"rdata:{type(rdata)}")
                            print(f"append rdata")
                            t=np.linspace(0,rdata.shape[1])
                            mat_t=matlab.double(t.tolist())
                            mat_y=matlab.double(rdata.tolist())
                            i=lead_idx+1
                            eng.workspace[f't_{i}']=mat_t
                            eng.workspace[f'y_{i}']=mat_y
                            eng.eval(f"data_{i} = struct('t', t_{i}, 'y', y_{i}, 'label', label_{i});", nargout=0)
                            
                            eng.eval(f"subplot(6, 1, {i});", nargout=0)  # 创建子图
                            eng.eval(f"plot(data_{i}.t, data_{i}.y, 'Color', colors({i}), 'DisplayName', data_{i}.label);", nargout=0)
                            eng.eval(f"title('Data Group {i}');", nargout=0)
                            eng.eval("xlabel('Time');", nargout=0)
                            eng.eval("ylabel('Value');", nargout=0)
                            eng.eval("legend('show');", nargout=0)
                            denoisedSet.append(rdata)
                            # print(f"denoisedSet:{type(denoisedSet)}")
                            # transport_data+=generate_multichannel_data(rdata,lead_idx)
                            # print(f"transportdata:{type(transport_data)}")
                    else:
                        denoisedSet.append(current_lead)
                        print(f"append current_lead")
                        # transport_data+=generate_multichannel_data(current_lead,lead_idx)
        eng.eval("tight_layout;", nargout=0)
        eng.quit()
        return denoisedSet
        #获取denoise数据序列shape
        #自己序列time生成
        #创建数组{(t)np.array,(denoise_set)np.array,(idx)script}
        #转换cellarray传输
        #修改getdataset
        #UDP(transport_data)
        # print(denoisedSet)                      
        # denoisedSet = np.array(denoisedSet).flatten()         
        # print(denoisedSet.shape)
  
    
    def preprocessing(data,label, protected_attribute):
        print(f"preprocessing data",data.shape)
        sample_count = data.shape[0]
        dtype = np.dtype([
            ('heartbeat', np.ndarray,(300,)),    # 特征数据
            ('age', np.int32),  # 保护属性
            ('Rclass', np.int32)        # 标签
        ])
        
        merged_data = np.zeros(sample_count, dtype=dtype)
        if type(data) != np.int32:
            print(f"oringin data type:",type(data))
        if data.shape == (sample_count, 300):
            merged_data['heartbeat'] = data
        else:
            print("Error: 'data' does not have the expected shape!")    
        print(f"merged_data",merged_data['heartbeat'])
        merged_data['age'] = np.random.choice([0, 1], sample_count)#待修改
        prot_attr= merged_data['age']
        merged_data['Rclass'] = label
  # 提取结构化数组中的数据
        heartbeat_features = merged_data['heartbeat']  # 形状 (n_samples, 300)
        protected_attributes = merged_data['age'].reshape(-1, 1)   # 形状 (n_samples, 1)
        labels = merged_data['Rclass'] # 形状 (n_samples, 1)
       # print(f"Does heartbeat_features contain NaN? {(heartbeat_features == 0).any()}")
        print(heartbeat_features .shape, labels.shape, protected_attributes.shape)
        # 定义特权组和非特权组
        privileged_groups = [{'age': 1}]
        unprivileged_groups = [{'age': 0}]
        df = pd.DataFrame(
        data=heartbeat_features,
        columns=[f'heartbeat_{i}' for i in range(300)]
    )
        df['age'] = protected_attributes           # 添加受保护属性列
        df['Rclass'] = labels    # 添加标签列
        has_zero_age = (df['age'] == 0).any()

        # 检查 'Rclass' 列是否有0值
        has_zero_rclass = (df['Rclass'] == 0).any()
       
        print(f"age列是否包含0值: {has_zero_age}")
        print(f"Rclass列是否包含0值: {has_zero_rclass}")
        print("Age=0, Rclass=0:", len(df[(df['age'] == 0) & (df['Rclass'] == 0)]))
        print("Age=0, Rclass=1:", len(df[(df['age'] == 0) & (df['Rclass'] == 1)]))
        print("Age=1, Rclass=0:", len(df[(df['age'] == 1) & (df['Rclass'] == 0)]))
        print("Age=1, Rclass=1:", len(df[(df['age'] == 1) & (df['Rclass'] == 1)]))
    # 初始化数据集
        dataset = BinaryLabelDataset(
            df=df,  # 核心参数：传入 DataFrame
            label_names=['Rclass'], 
            favorable_label=1,
            unfavorable_label=0,               # 指定标签列
            protected_attribute_names=['age'],
                 # 指定受保护属性列
            privileged_protected_attributes=[[1]]  # age=1 是特权组
        )
        print("Dataset type:", type(dataset))
    #predebasing
        metric_orig_train = BinaryLabelDatasetMetric(
        dataset,
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
        if metric_orig_train:
         RW = Reweighing(unprivileged_groups=unprivileged_groups,
                privileged_groups=privileged_groups)
         dataset_orig_train=dataset
         dataset_transf_train = RW.fit_transform(dataset_orig_train)

         metric_transf_train = BinaryLabelDatasetMetric(dataset_transf_train, 
                                               unprivileged_groups=unprivileged_groups,
                                               privileged_groups=privileged_groups)
        
    #当平均结果差异为0时： 
        statistical_parity_difference = metric_transf_train.statistical_parity_difference()

        if abs(statistical_parity_difference) < 1e-6:
         print("Statistical parity difference is close to zero, applying denoising.")
         print (f"heartbeat_features",heartbeat_features)
         rdata = denoise(heartbeat_features.flatten().reshape(1,-1))
         print (rdata)
         print(f"does rdata contain NAN?{np.isnan(rdata).any()}")              
        return  rdata,prot_attr.flatten()
   #获得用于训练网络数据集
    def getDataSet(number, X_data, Y_data, AGE, MIT=1):
    
     if MIT:
        base_dir = r'D:\heartbeat\mit-bih-arrhythmia-database-1.0.0'
        record_path = os.path.join(base_dir, str(number))
        
        try:
            # 读取心电记录和注释
            # 检查记录文件是否存在
            if not os.path.exists(record_path + '.hea'):
                print(f"记录 {number} 的 .hea 文件缺失")
                return

            # 读取心电记录
            record = wfdb.rdrecord(record_path, channel_names=['MLII'])
            if record is None:
                print(f"记录 {number} 无法读取（可能缺少MLII导联）")
                return

            # 检查信号数据是否存在
            if not hasattr(record, 'p_signal') or record.p_signal is None:
                # 尝试回退到d_signal（数字信号）
                if hasattr(record, 'd_signal') and record.d_signal is not None:
                    signal_data = record.d_signal
                else:
                    print(f"记录 {number} 无有效信号数据")
                    return
            else:
                signal_data = record.p_signal

            annotation = wfdb.rdann(record_path, 'atr')
        except FileNotFoundError:
            print(f"记录 {number} 不存在，已跳过")
            return
        except Exception as e:
            print(f"读取 {number} 时发生错误: {str(e)}")
            return
        # 展开信号并截取有效段
        rdata = record.p_signal.flatten()
        if len(rdata) < 200000:  # 确保信号长度足够
            print(f"记录 {number} 信号长度不足 1000 点（实际 {len(rdata)} 点），已跳过")
            return
        rdata = rdata[:200000]
        # 解析年龄（添加默认值）
        age = 60  # 默认年龄
        for comment in record.comments:
            if 'Age:' in comment:
                try:
                    age = int(comment.split(':')[1].strip())
                except ValueError:
                    pass
                break

        # 处理R峰注释
        Rlocation = annotation.sample
        Rclass = annotation.symbol
        # 调整循环范围（避免负值）
        start, end = 10, 5
        valid_range = len(Rclass) - end
        if valid_range <= start:
            print(f"记录 {number} 有效注释不足（总注释数 {len(Rclass)}），已跳过")
            return
        i = start
        while i < valid_range:
            # 标签匹配检查
            try:
                label = ecgClassSet.index(Rclass[i])
            except ValueError:
                i += 1
                continue
            # R峰位置检查
            r_pos = Rlocation[i]
            if r_pos < 100 or r_pos + 200 > len(rdata):
                i += 1
                continue
            # 截取心电片段
            x_train = rdata[r_pos - 100 : r_pos + 200]
            if len(x_train) != 300:
                i += 1
                continue
            # 追加数据
            X_data.append(x_train)
            Y_data.append(label)
            AGE.append(age)
            i += 1
    
    def loadData():
        numberSet = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 
                    111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 
                    122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 
                    209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 
                    222, 223, 228, 230, 231, 232, 233, 234]#几号的数据可随意抽取
        dataSet = []
        lableSet = []
        ageSet=[]
        for n in tqdm(numberSet, desc="处理心电数据", ncols=80):
            getDataSet(n, dataSet, lableSet,ageSet,True)
            #print(f"Does dataSet contain NaN? {np.isnan(dataSet).any()}")
           # print(f"记录 {n} 处理后 dataSet 长度: {len(dataSet)}")
            if len(dataSet) !=0:
             #print(f"dataSet:",type(dataSet))
             str_list = [str(num) for num in dataSet]
            # 使用逗号连接字符串列表
             #print(f"str_list:",type(str_list))
             joined_data = ','.join(str_list)
            # UDP(joined_data)
             dataSet_stacked=np.stack(dataSet,axis=0)#{[N,[1000,]]}
        ageSet= np.array(ageSet)
       # print(ageSet,lableSet)
        ageSet= np.where(ageSet >= 30, 1, 0)
        lableSet=np.array(lableSet)
        favor_lableSet=np.where(lableSet==0,0,1)
        #print(favor_lableSet)
        print(f"before preprocessing",type(dataSet_stacked),dataSet_stacked)
        dataSet,ageSet=preprocessing(dataSet_stacked,favor_lableSet,ageSet)
        print(f"after preprocessing,Does dataSet contain NaN? {np.isnan(dataSet).any()}")
        '''
        
        为成功运行代码，这里的ageSet被覆盖掉一次
        '''
            #while n==234(即全部取完后):preprocessing,standarddataset{df=data[n_numberset,rdata_n],age=[age_1,age_2,...],}返回rdata_processed=一维[]，age=[0,1,0,0]
        # 转numpy数组,打乱顺序
        print (dataSet.shape)
        dataSet = np.array(dataSet).reshape(-1, 300) 
        print(f"after reshaping,Does dataSet contain NaN? {np.isnan(dataSet).any()}")
         # 转化为二维，一行有 300 个，行数需要计算
        lableSet = np.array(lableSet).reshape(-1, 1) 
        ageSet= np.array(ageSet).reshape(-1, 1)
        print(dataSet.shape,lableSet.shape,ageSet.shape) # 转化为二维，一行有   1 个，行数需要计算
        train_ds = np.hstack((dataSet, lableSet,ageSet)) #行数相同，列数相加 # 将数据集和标签集水平堆叠在一起
        np.random.shuffle(train_ds)#打乱数据集
        # 数据集及其标签集
        X = train_ds[:, :300].reshape(-1, 300, 1)  # (92192, 300, 1)
        Y = train_ds[:, 300]  # (92192)
        AGE=train_ds[:,301]
        # 测试集及其标签集
        shuffle_index = np.random.permutation(len(X))  # 生成0-(X-1)的随机索引数组
        
        # 设定测试集的大小 RATIO是测试集在数据集中所占的比例
        test_length = int(RATIO * len(shuffle_index))
        # 测试集的长度
        test_index = shuffle_index[:test_length]
        # 训练集的长度
        train_index = shuffle_index[test_length:]
        X_test, Y_test,AGE_test = X[test_index], Y[test_index],AGE[test_index]
        X_train, Y_train,AGE_train = X[train_index], Y[train_index],AGE[train_index]
        print(f"X_train shape after pre(): {X_train.shape}")
        print(f"Does X_train contain NaN? {np.isnan(X_train).any()}")
        if np.isnan(X_train).any():
            print("First 10 rows of X_train containing NaN:")
            print(X_train[np.isnan(X_train).any(axis=(1, 2))][:10]) # 打印包含 NaN 的前 10 个样本
        return X_train, Y_train,AGE_train, X_test, Y_test,AGE_test
    return loadData()
'''
测试matlab绘图
'''

# 生成模拟心电图数据
def generate_ecg_data(num_leads=6, num_samples=1000, fs=500):
    t = np.linspace(0, num_samples/fs, num_samples)
    ecg_data = np.zeros((num_leads, num_samples))
    
    # 模拟心电图信号，使用简单的正弦波或更复杂的波形
    for i in range(num_leads):
        # 基本的ECG波形模拟，可以根据需要调整参数
        heart_rate = 60 + np.random.uniform(-10, 10)  # 随机心率
        frequency = heart_rate / 60  # 转换为频率（Hz）
        ecg_data[i, :] = np.sin(2 * np.pi * frequency * t) + 0.1 * np.random.randn(num_samples)  # 加上噪声
    
    return ecg_data, t

# 生成6组心电图数据
num_leads = 6
num_samples = 1000  # 采样点数
ecg_data, t = generate_ecg_data(num_leads, num_samples)
denoised_ecg = pre(ecg_data)
# 绘制生成的原始ECG信号
plt.figure(figsize=(10, 8))
for i in range(num_leads):
    plt.subplot(6, 1, i+1)
    plt.plot(t, ecg_data[i, :])
    plt.title(f'Lead {i+1}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

#X_real,Y_real
class CustomDataset:
    def __init__(self, features, labels, prot_attr):
        self.features = features  # 形状 (n_samples, time_steps, input_features)
        self.labels = labels      # 形状 (n_samples,)
        self.prot_attr = prot_attr  # 形状 (n_samples, 1)
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return (
            self.features[idx], 
            self.labels[idx], 
            self.prot_attr[idx],
        )
    def isna(self):
        """返回一个支持链式调用的对象"""
        class NaNChecker:
            def __init__(self, features, labels, prot_attr):
                self.features = features
                self.labels = labels
                self.prot_attr = prot_attr
                
            def any(self):
                # 检查是否存在任何 True
                def _any(data):
                    if isinstance(data, np.ndarray):
                        return data.any()
                    elif torch.is_tensor(data):
                        return data.any().item()
                    else:
                        raise TypeError(f"不支持的数据类型: {type(data)}")

                return (
                    _any(np.isnan(self.features)) if isinstance(self.features, np.ndarray) else _any(torch.isnan(self.features)) or
                    _any(np.isnan(self.labels)) if isinstance(self.labels, np.ndarray) else _any(torch.isnan(self.labels)) or
                    _any(np.isnan(self.prot_attr)) if isinstance(self.prot_attr, np.ndarray) else _any(torch.isnan(self.prot_attr))
                )

        return NaNChecker(self.features, self.labels, self.prot_attr)
    
    #fit所用的dataset是整合了数据，标签，特权标记的  
    # dataset=CustomDataset(X_train,Y_train,[]) preprocessing单独提取出来






class CustomAdversarialDebiasing(AdversarialDebiasing):
  
  def __init__(self,  unprivileged_groups,
                 privileged_groups,sess , scope_name='classifier',
                 adversary_loss_weight=0.1, num_epochs=50, batch_size=128,
                 classifier_num_hidden_units=50, debias=True,
                 random_state=None, classifier_num_input_units=1,time_steps=300,num_classes=2
                 ) : 
        
        super(CustomAdversarialDebiasing, self).__init__(
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups,
            scope_name=scope_name,
            sess=sess,
            adversary_loss_weight=adversary_loss_weight,
            num_epochs=num_epochs,
            batch_size=batch_size,
            classifier_num_hidden_units=classifier_num_hidden_units,
            debias=debias,
        )
        
        # 扩展参数
        self.classifier_num_input_units = classifier_num_input_units
        self.time_steps = time_steps 
        self.num_classes = num_classes
        self.random_state = random_state if random_state is not None else np.random.RandomState()
        self.initializer_seed = self.random_state.randint(0, 2**32 ,dtype=np.uint32) 
        # 定义TensorFlow占位符
        self.protected_attributes_ph = tf.compat.v1.placeholder(
            tf.float32, shape=[None, 1], name='protected_attributes_ph')#特权标签值
        self.keep_prob = tf.compat.v1.placeholder(tf.float32, name='keep_prob')

        self._build_custom_model()
      
  def fit(self, dataset, **kwargs):
     # Begin training
     #混洗数据
    for epoch in range(self.num_epochs):
        shuffled_ids = np.random.permutation(len(dataset))
        for i in range(len(dataset) // self.batch_size):
            batch_ids = shuffled_ids[self.batch_size * i: self.batch_size * (i + 1)]
            batch_features, batch_labels, batch_prot_attr = dataset[batch_ids]
            batch_prot_attr = np.array(batch_prot_attr).reshape(-1, 1)
            #注意dataset排列顺序features,labels,protected_attributes
            batch_feed_dict = {
                self.input_x: batch_features,
                self.input_y: batch_labels,
                self.protected_attributes_ph: batch_prot_attr,
                self.keep_prob: 0.8
            }
            if self.debias:
                _, _, clf_loss_val, adv_loss_val = self.sess.run(
                    [self.clf_min,self.adv_min, self.clf_loss, self.adv_loss],
                    feed_dict=batch_feed_dict
                )
                print("epoch {:>3d}; iter: {:>4d}; batch classifier loss: {:.4f}; adversarial loss: {:.4f}".format(
                    epoch, i, clf_loss_val, adv_loss_val))
            else:
                _, clf_loss_val = self.sess.run([self.clf_min, self.clf_loss], feed_dict=batch_feed_dict)
                print("epoch {:>3d}; iter: {:>4d}; batch classifier loss: {:.4f}".format(epoch, i, clf_loss_val))
    self.is_trained_ = True       
    return self  # 正确缩进在fit函数最外层
    #自建立主分类器
  def _build_custom_model(self):
    with tf.compat.v1.variable_scope(self.scope_name,reuse=tf.compat.v1.AUTO_REUSE):
        # 输入层
        self.input_x = tf.compat.v1.placeholder(
            tf.float32, [None, self.time_steps, self.classifier_num_input_units],
            name='input_x')
        self.input_y = tf.compat.v1.placeholder(
            tf.int32, [None], name='input_y')  
        # RNN结构
        cell = tf.compat.v1.nn.rnn_cell.BasicRNNCell(self.classifier_num_hidden_units)
        outputs, states = tf.compat.v1.nn.dynamic_rnn(
            cell, self.input_x, dtype=tf.float32)
        # 分类层
        logits = tf.compat.v1.layers.dense(
            outputs[:, -1, :], self.num_classes,
            kernel_initializer=tf.compat.v1.orthogonal_initializer())
        self.classifier_logits_ = logits 
        self._build_adversary(logits)
  def _build_adversary(self, logits):  
        # Create adversary
    with tf.compat.v1.variable_scope("adversary_model"):
        c = tf.compat.v1.get_variable('c', initializer=tf.constant(1.0))
        s = tf.sigmoid((1 + tf.abs(c)) * self.classifier_logits_)

        W2 = tf.compat.v1.get_variable('W2', [self.num_classes * 3, self.num_classes],
                               initializer=tf.initializers.glorot_uniform(seed=self.initializer_seed))
        b2 = tf.Variable(tf.zeros(shape=[self.num_classes]), name='b2')

        self.adversary_logits_ = tf.matmul(
    tf.concat([s, s * self.protected_attributes_ph, s * (1. - self.protected_attributes_ph)], axis=1),
    W2) + b2
        adv_loss = tf.reduce_mean(
            tf.nn.sparse_softmax_cross_entropy_with_logits(
                labels=tf.squeeze(tf.cast(self.protected_attributes_ph, tf.int32)),
                logits=self.adversary_logits_))

    global_step = tf.Variable(0., trainable=False)
    init_learning_rate = 0.001
    if self.adversary_loss_weight is not None:
        learning_rate = tf.compat.v1.train.exponential_decay(init_learning_rate, global_step, 1000, 0.96, staircase=True)
    else:
        learning_rate = tf.compat.v1.train.inverse_time_decay(init_learning_rate, global_step, 1000, 0.1, staircase=True)

    # 主分类器损失
    self.clf_loss = tf.reduce_mean(
        tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.input_y, logits=logits))

    # Setup optimizers
    self.clf_opt = tf.compat.v1.train.AdamOptimizer(learning_rate)
    if self.debias:
        self.adv_opt = tf.compat.v1.train.AdamOptimizer(learning_rate)

    clf_vars = [var for var in tf.compat.v1.trainable_variables() if 'classifier' in var.name or 'input_projection' in var.name]

    if self.debias:
        adv_vars = [var for var in tf.compat.v1.trainable_variables() if 'adversary_model' in var.name]
        # Compute grad wrt classifier parameters
        adv_grads = {var: grad for (grad, var) in self.adv_opt.compute_gradients(adv_loss, var_list=clf_vars)}

    normalize = lambda x: x / (tf.norm(x) + np.finfo(np.float32).tiny)

    clf_grads = []
    for (grad, var) in self.clf_opt.compute_gradients(self.clf_loss, var_list=clf_vars):
        if self.debias:
            unit_adv_grad = normalize(adv_grads[var])
            grad -= tf.reduce_sum(grad * unit_adv_grad) * unit_adv_grad
            if self.adversary_loss_weight is not None:
                grad -= self.adversary_loss_weight * adv_grads[var]
            else:
                grad -= tf.sqrt(global_step) * adv_grads[var]
        clf_grads.append((grad, var))

    self.clf_min = self.clf_opt.apply_gradients(clf_grads, global_step=global_step)
    if self.debias:
        with tf.control_dependencies([self.clf_min]):
            self.adv_min = self.adv_opt.minimize(adv_loss, var_list=adv_vars)

    self.sess.run(tf.compat.v1.global_variables_initializer())

   #输入test_data
  def decision_function(self, X):
    #检查是否已训练过
    check_is_fitted(self, [
        'classes_',          # 来自 sklearn 的规范属性
        'sess_',             # 确保会话已创建
        'is_trained_'        # 自定义训练状态标志
    ])
    #获取信息
    n_samples = X.shape[0]
    n_classes = len(self.num_classes)
    

    # 初始化分数数组（始终为二维，兼容二分类和多分类）
    scores = np.empty((n_samples, n_classes), dtype=np.float32)
    #每次选取batch个
    for batch_start in range(0, n_samples, self.batch_size):
        batch_end = min(batch_start + self.batch_size, n_samples)
        batch_ids = np.arange(batch_start, batch_end)
        
        # 兼容 DataFrame 和 ndarray
        batch_features = (
            X.iloc[batch_ids] 
            if hasattr(X, 'iloc') 
            else X[batch_ids]
        )

        batch_feed_dict = {
            self.classifier_num_input_units: batch_features,
            self.keep_prob: 1.0  # 推理时关闭 dropout
        }

        # 获取当前批次的 logits（形状为 (batch_size, n_classes)）
        batch_logits = self.sess.run(
            self.classifier_logits_, 
            feed_dict=batch_feed_dict
        )
        scores[batch_ids] = batch_logits#获取每个样本的logits
 
    return scores
  def predict_proba(self, X):
        decision = self.decision_function(X)
        decision_2d = decision
        return scipy.special.softmax(decision_2d, axis=1)
  def predict(self, X):
        scores = self.decision_function(X)
        indices = scores.argmax(axis=1)
        return ecgClassSet.index(self.classes_[indices])
#初始化时直接输入privileged_groups和unprivileged_groups
#调用fit时使用的是合成后的dataset数据
 
X_train, Y_train,AGE_train,X_test,Y_test,AGE_test=pre()
print(f"X_train shape after pre(): {X_train.shape}")
print(f"Does X_train contain NaN? {np.isnan(X_train).any()}")
'''
if np.isnan(X_train).any():
    print("First 10 rows of X_train containing NaN:")
    print(X_train[np.isnan(X_train).any(axis=(1, 2))][:10])
    print (X_train.shape)
sess = tf.compat.v1.Session()
trained_models = {}
test_models = {}
privileged_groups = [{'age': 1}]
unprivileged_groups = [{'age': 0}]
for favorable_label in ecgClassSet:
    print(f"Training model for favorable label: {favorable_label}")
    # 创建临时二元标签
    binary_labels_train = np.where(Y_train == ecgClassSet.index(favorable_label), 1, 0)   
    dataset_train=CustomDataset(X_train, binary_labels_train,AGE_train)
    binary_labels_test = np.where(Y_test == ecgClassSet.index(favorable_label), 1, 0)   
    dataset_test=CustomDataset(X_test, binary_labels_test,AGE_test)
    #无debasing
    train_undebased_model = CustomAdversarialDebiasing(privileged_groups = privileged_groups,
                            unprivileged_groups = unprivileged_groups,
                            debias=False,
                            sess=sess)
    dataset_train_pd= pd.DataFrame(
        data=dataset_train.features.reshape(-1,dataset_train.features.shape[1]),
        columns=[f'feature_{i}' for i in range(dataset_train.features.shape[1])]
    )
    dataset_train_pd['label'] = dataset_train.labels
    dataset_train_pd['prot_attr'] = dataset_train.prot_attr
    print(dataset_train_pd.columns)
    print("Unique values in Y_train:", np.unique(Y_train),np.unique( binary_labels_train))
    print("First 10 values in dataset_train.labels:", dataset_train.labels[:10])
    print("Unique values in dataset_train_pd['label']:", dataset_train_pd['label'].unique())
    dataset_origin_train = BinaryLabelDataset(
        df=dataset_train_pd,
        label_names=['label'],
        protected_attribute_names=['prot_attr'],
        favorable_label=1,
        unfavorable_label=0
    )
    model=train_undebased_model.fit(dataset_train)
    trained_models[favorable_label] = model
    test_undebased_model = CustomAdversarialDebiasing(privileged_groups = privileged_groups,
                          unprivileged_groups = unprivileged_groups,
                          debias=False,
                          sess=sess)
    dataset_test_pd= pd.DataFrame(
        data=dataset_test.features.reshape(-1,dataset_test.features.shape[1]),
        columns=[f'feature_{i}' for i in range(dataset_test.features.shape[1])]
    )
    dataset_test_pd['label'] = dataset_test.labels
    dataset_test_pd['prot_attr'] = dataset_test.prot_attr
    dataset_origin_test = BinaryLabelDataset(
        df=dataset_test_pd,
        label_names=['label'],
        protected_attribute_names=['prot_attr'],
        favorable_label=1,
        unfavorable_label=0,
    )
    model=test_undebased_model.fit(dataset_test)
    test_models[favorable_label] = model


#评价无debasing
dataset_nodebiasing_train=dataset_origin_train.copy()
dataset_nodebiasing_test=dataset_origin_test.copy()
dataset_nodebiasing_train.labels = train_undebased_model.predict(X_train)
dataset_nodebiasing_test.labels = test_undebased_model.predict(X_test)
# Metrics for the dataset from plain model (without debiasing)
display(Markdown("#### Plain model - without debiasing - dataset metrics"))
metric_dataset_nodebiasing_train = BinaryLabelDatasetMetric(dataset_nodebiasing_train, 
                                             unprivileged_groups=unprivileged_groups,
                                             privileged_groups=privileged_groups)

print("Train set: Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_dataset_nodebiasing_train.mean_difference())

metric_dataset_nodebiasing_test = BinaryLabelDatasetMetric(dataset_nodebiasing_test, 
                                             unprivileged_groups=unprivileged_groups,
                                             privileged_groups=privileged_groups)

print("Test set: Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_dataset_nodebiasing_test.mean_difference())

display(Markdown("#### Plain model - without debiasing - classification metrics"))
classified_metric_nodebiasing_test = ClassificationMetric(dataset_origin_test, 
                                                 dataset_nodebiasing_test,
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
print("Test set: Classification accuracy = %f" % classified_metric_nodebiasing_test.accuracy())
TPR = classified_metric_nodebiasing_test.true_positive_rate()
TNR = classified_metric_nodebiasing_test.true_negative_rate()
bal_acc_nodebiasing_test = 0.5*(TPR+TNR)
print("Test set: Balanced classification accuracy = %f" % bal_acc_nodebiasing_test)
print("Test set: Disparate impact = %f" % classified_metric_nodebiasing_test.disparate_impact())
print("Test set: Equal opportunity difference = %f" % classified_metric_nodebiasing_test.equal_opportunity_difference())
print("Test set: Average odds difference = %f" % classified_metric_nodebiasing_test.average_odds_difference())
print("Test set: Theil_index = %f" % classified_metric_nodebiasing_test.theil_index())



#有debasing
sess.close()
tf.reset_default_graph()
sess = tf.Session()
train_debased_model = CustomAdversarialDebiasing(privileged_groups = privileged_groups,
                          unprivileged_groups = unprivileged_groups,
                          debias=True,
                          sess=sess)
dataset_train=CustomDataset(X_train, Y_train,AGE_train)
train_debased_model.fit(dataset_train)
test_debased_model = CustomAdversarialDebiasing(privileged_groups = privileged_groups,
                          unprivileged_groups = unprivileged_groups,
                          debias=True,
                          sess=sess)
dataset_test=CustomDataset(X_test,Y_test,AGE_test)
test_debased_model.fit(dataset_test)
#评价无debasing
dataset_debiasing_train=dataset_origin_train.copy()
dataset_debiasing_test=dataset_origin_test.copy()
dataset_debiasing_train.labels = train_debased_model.predict(X_train)
dataset_debiasing_test.labels = test_debased_model.predict(X_test)
# Metrics for the dataset from plain model (without debiasing)
display(Markdown("#### Plain model - without debiasing - dataset metrics"))
print("Train set: Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_dataset_nodebiasing_train.mean_difference())
print("Test set: Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_dataset_nodebiasing_test.mean_difference())

# Metrics for the dataset from model with debiasing
display(Markdown("#### Model - with debiasing - dataset metrics"))
metric_dataset_debiasing_train = BinaryLabelDatasetMetric(dataset_debiasing_train, 
                                             unprivileged_groups=unprivileged_groups,
                                             privileged_groups=privileged_groups)

print("Train set: Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_dataset_debiasing_train.mean_difference())

metric_dataset_debiasing_test = BinaryLabelDatasetMetric(dataset_debiasing_test, 
                                             unprivileged_groups=unprivileged_groups,
                                             privileged_groups=privileged_groups)

print("Test set: Difference in mean outcomes between unprivileged and privileged groups = %f" % metric_dataset_debiasing_test.mean_difference())



display(Markdown("#### Plain model - without debiasing - classification metrics"))
print("Test set: Classification accuracy = %f" % classified_metric_nodebiasing_test.accuracy())
TPR = classified_metric_nodebiasing_test.true_positive_rate()
TNR = classified_metric_nodebiasing_test.true_negative_rate()
bal_acc_nodebiasing_test = 0.5*(TPR+TNR)
print("Test set: Balanced classification accuracy = %f" % bal_acc_nodebiasing_test)
print("Test set: Disparate impact = %f" % classified_metric_nodebiasing_test.disparate_impact())
print("Test set: Equal opportunity difference = %f" % classified_metric_nodebiasing_test.equal_opportunity_difference())
print("Test set: Average odds difference = %f" % classified_metric_nodebiasing_test.average_odds_difference())
print("Test set: Theil_index = %f" % classified_metric_nodebiasing_test.theil_index())



display(Markdown("#### Model - with debiasing - classification metrics"))
classified_metric_debiasing_test = ClassificationMetric(X_test,
                                                 dataset_debiasing_test,
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
print("Test set: Classification accuracy = %f" % classified_metric_debiasing_test.accuracy())
TPR = classified_metric_debiasing_test.true_positive_rate()
TNR = classified_metric_debiasing_test.true_negative_rate()
bal_acc_debiasing_test = 0.5*(TPR+TNR)
print("Test set: Balanced classification accuracy = %f" % bal_acc_debiasing_test)
print("Test set: Disparate impact = %f" % classified_metric_debiasing_test.disparate_impact())
print("Test set: Equal opportunity difference = %f" % classified_metric_debiasing_test.equal_opportunity_difference())
print("Test set: Average odds difference = %f" % classified_metric_debiasing_test.average_odds_difference())
print("Test set: Theil_index = %f" % classified_metric_debiasing_test.theil_index())
'''