import numpy as np
from rknnlite.api import RKNNLite
import cv2
# mycode.py
import logging

# 确保日志级别为大写
logging.addLevelName(logging.WARNING, 'WARNING')
logging.addLevelName(logging.INFO, 'INFO')
logging.addLevelName(logging.DEBUG, 'DEBUG')
logging.addLevelName(logging.ERROR, 'ERROR')

# 再导入PyTorch
import torch

import torch.nn.functional as F
import serial
import time
import threading
from datetime import datetime

import serial
import time
import random

class SerialSender:
    """串口数据发送类，用于向Windows端发送模拟传感器数据"""
    
    def __init__(self, port='/dev/ttyFIQ0', baudrate=115200, timeout=1, write_timeout=1):
        """
        初始化串口发送器
        
        :param port: 串口设备路径（默认 '/dev/ttyFIQ0'）
        :param baudrate: 波特率（默认 115200）
        :param timeout: 读超时时间（秒）
        :param write_timeout: 写超时时间（秒）
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.write_timeout = write_timeout
        self.ser = None  # 串口对象
        self.running = False  # 发送状态标记

    def connect(self):
        """连接串口设备"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.write_timeout
            )
            print(f"已连接到串口: {self.ser.name}")
            # 等待串口稳定
            time.sleep(2)
            return True
        except serial.SerialException as e:
            print(f"串口连接失败: {e}")
            print("提示: 请检查设备是否连接，或执行 'sudo chmod 666 {self.port}' 赋予权限")
            return False

    def generate_sensor_data(self):
        """生成模拟传感器数据（可重写以实现自定义数据）"""
        # 模拟温度（25±3℃）和湿度（60±5%）
        temp = 25 + random.uniform(-3, 3)
        hum = 60 + random.uniform(-5, 5)
        return temp, hum

    def format_message(self, temp, hum):
        """格式化发送消息（可重写以修改数据格式）"""
        return f"TEMP:{temp:.1f},HUM:{hum:.1f}%\n"

    def start_sending(self, interval=5):
        """
        开始发送数据
        
        :param interval: 发送间隔（秒）
        """
        if not self.ser or not self.ser.is_open:
            print("请先调用 connect() 连接串口")
            return
        
        self.running = True
        counter = 0
        print("，按 Ctrl+C 停止...")
        
        try:
            while self.running:
                # 生成并格式化数据
                temp, hum = self.generate_sensor_data()
                message = self.format_message(temp, hum)
                
                # 发送数据
                self.ser.write(message.encode('utf-8'))
                print(f"接收[{counter}]: {message.strip()}")
                
                counter += 1
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n用户中断发送")
        except serial.SerialTimeoutException:
            print("发送超时，可能设备已断开连接")
        finally:
            self.stop_sending()

    def stop_sending(self):
        """停止发送并关闭串口"""
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("串口已关闭")








class SerialReceiver:
    def __init__(self, port="/dev/ttyS9", baudrate=9600, timeout=1):
        """初始化串口接收类"""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.is_running = False
        self.receive_thread = None
        self.data_callback = None
        self.buffer = bytearray()  # 数据缓冲区

    def set_data_callback(self, callback):
        """设置数据接收回调函数"""
        self.data_callback = callback

    def open(self):
        """打开串口连接"""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"成功连接到串口: {self.port} @ {self.baudrate}bps")
            return True
        except serial.SerialException as e:
            print(f"串口连接失败: {e}")
            return False

    




    def start_receiving(self):
        """开始接收数据线程"""
        if not self.serial or not self.serial.is_open:
            if not self.open():
                return False
        
        self.is_running = True
        self.receive_thread = threading.Thread(target=self._receive_loop)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        print("开始接收数据...")
        return True

    def _receive_loop(self):
        """数据接收循环"""
        while self.is_running:
            try:
                if self.serial.in_waiting > 0:
                    # 读取所有可用数据
                    data = self.serial.read(self.serial.in_waiting)
                    self.buffer.extend(data)
                    
                    # 打印原始接收数据（用于调试）
                    print(f"接收到数据片段: {data.hex(' ')}")
                    print(f"当前缓冲区: {self.buffer.hex(' ')} (长度: {len(self.buffer)})")
                    
                    # 查找帧头0xaa的所有位置
                    frame_heads = [i for i, b in enumerate(self.buffer) if b == 0xaa]
                    
                    # 处理所有可能的完整帧
                    while frame_heads and (frame_heads[0] + 4 < len(self.buffer)):
                        start_idx = frame_heads[0]
                        end_idx = start_idx + 5
                        
                        # 检查是否有完整的5字节帧
                        if end_idx <= len(self.buffer):
                            frame = self.buffer[start_idx:end_idx]
                            
                            # 验证帧头和长度
                            if len(frame) == 5 and frame[0] == 0xaa:
                                hex_str = ' '.join([f"{b:02X}" for b in frame])
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                # 调用回调函数
                                if self.data_callback:
                                    self.data_callback(timestamp, frame, hex_str)
                                
                                # 从缓冲区移除已处理的帧
                                self.buffer = self.buffer[end_idx:]
                                print(f"已处理帧，剩余缓冲区: {self.buffer.hex(' ')}")
                            else:
                                # 不是有效帧，丢弃到下一个帧头
                                next_head = next((i for i in frame_heads[1:] if i > start_idx), None)
                                if next_head:
                                    self.buffer = self.buffer[next_head:]
                                    print(f"丢弃无效帧，跳到下一个帧头")
                                else:
                                    self.buffer = self.buffer[start_idx+1:]  # 至少跳过当前无效帧头
                                    print(f"丢弃无效帧头")
                        else:
                            # 没有足够数据形成完整帧，等待更多数据
                            break
                        
                        # 更新帧头列表
                        frame_heads = [i for i, b in enumerate(self.buffer) if b == 0xaa]
                    
                    # 如果缓冲区过长但没有完整帧，清空
                    if len(self.buffer) > 10 and not frame_heads:
                        print(f"警告: 缓冲区数据过长且无帧头，清空缓冲区: {self.buffer.hex(' ')}")
                        self.buffer.clear()
                
                # 超时处理（如果长时间没有新数据）
                time.sleep(0.01)  # 减少CPU占用
                
            except Exception as e:
                print(f"接收数据时出错: {e}")
                time.sleep(0.1)

    def stop(self):
        """停止接收并关闭串口"""
        self.is_running = False
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join(1.0)
        
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("串口已关闭")

def print_received_data(timestamp, raw_data, hex_data):
    """数据接收回调函数示例"""
    print(f"[{timestamp}] 收到完整帧: {hex_data}")
    print(f"[{timestamp}] 原始数据: {list(raw_data)}")
    
    
    # Load training data statistics
    stats = np.load('train_stats.npy', allow_pickle=True).item()
    feat_mean = stats['mean']
    feat_std = stats['std']

    def generate_test_sample():
    	#test_feat = np.array([50,8.3,8.55E-05,9.16,32.5], dtype=np.float32)
    	#test_feat = np.array([7.988241309,33.5506135,15.30547035,43.13650307,0.019171779],  dtype=np.float32)
        test_feat = np.array([8.718947576,29.22971236,19.58042101,42.44608499,0.024834055], 	dtype=np.float32)
    	#test_feat = np.random.randn(5).astype(np.float32)
        test_feat = (test_feat - feat_mean) / feat_std  # Standardize
        padded = np.pad(test_feat, (0, 4), constant_values=0)
        kernel = padded.reshape(3, 3).astype(np.float32)
        kernel = torch.from_numpy(kernel).unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, 3, 3)
        base_img = torch.randn(1, 1, 100, 100).float()  # Shape: (1, 1, 100, 100)
        test_img = F.conv2d(base_img, kernel, padding=0)  # Shape: (1, 1, 98, 98)
    	# Convert NCHW to NHWC for RKNN
        test_img = test_img.permute(0, 2, 3, 1).numpy()  # Shape: (1, 98, 98, 1)
        return test_img

	# Initialize RKNN runtime
    rknn = RKNNLite()
    ret = rknn.load_rknn('fault_diagnosis_cnn.rknn')

    ret = rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0)
    if ret != 0:
     print(f"初始化失败: {ret}")
    else:
     print("RKNN 初始化成功")

	# Perform inference
    input_data = generate_test_sample()  # Shape: (1, 98, 98, 1)
    outputs = rknn.inference(inputs=[input_data])
	# Softmax后处理
    def softmax(x):
     x_exp = np.exp(x - np.max(x, axis=1, keepdims=True))
     return x_exp / np.sum(x_exp, axis=1, keepdims=True)

    probs = softmax(outputs[0])
    predicted_class = np.argmax(probs[0])
    confidence = probs[0][predicted_class]
    class_names = ['正常', '中低温过热', '高温过热',
               '局部放电', '低能放电', '高能放电']



    print('✓ RKNN模型推理成功！')

	
    print(f'输入形状: {input_data.shape} | 输出概率和: {probs[0].sum():.4f}')
    print(f'预测故障: {class_names[predicted_class]} | 置信度: {confidence:.2%}')
	# Parse results

    print('✓ RKNN模型推理成功！')

	# Release resources
    rknn.release()
    sender = SerialSender(port='/dev/ttyFIQ0')  # 先创建类实例
    is_connected = sender.connect()  # 调用连接方法，获取布尔值（连接状态）

    if is_connected:
        # 只有连接成功时，才调用实例的方法
        sender.start_sending()
    else:
        print("连接失败，无法发送数据")


if __name__ == "__main__":
    
    receiver = SerialReceiver(port="/dev/ttyS9")
    
    
    # 设置回调函数
    receiver.set_data_callback(print_received_data)
    
    # 开始接收数据
    if receiver.start_receiving():
        try:
            # 保持主线程运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        finally:
            # 停止接收并清理资源
            receiver.stop()
    else:
        print("无法启动串口接收")
