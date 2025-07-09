import serial
import time
import threading
from datetime import datetime

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



if __name__ == "__main__":
    # 使用方法示例
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