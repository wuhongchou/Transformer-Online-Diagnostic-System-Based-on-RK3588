# 单片机（Ubuntu）端代码
import serial
import time
import random

def send_data_to_windows():
    """通过串口ttyUSB0向Windows发送数据"""
    try:
        # 打开串口（Ubuntu系统中通常为ttyUSB0）
        ser = serial.Serial(
            port='/dev/ttyFIQ0',  # 单片机的串口设备名
            #port='/dev/ttyS9', 
            baudrate=115200,        # 波特率，需与Windows端一致
            timeout=1,
            write_timeout=1
        )
        print(f"已连接到串口: {ser.name}")
        
        # 等待串口稳定
        time.sleep(2)
        
        print("开始发送数据到Windows，按 Ctrl+C 停止...")
        counter = 0
        
        while True:
            # 生成模拟数据（可根据实际需求修改）
            # 示例：模拟温度和湿度传感器数据
            temp = 25 + random.uniform(-3, 3)  # 温度波动范围
            hum = 60 + random.uniform(-5, 5)   # 湿度波动范围
            
            # 构建发送消息（格式可自定义）
            message = f"TEMP:{temp:.1f},HUM:{hum:.1f}%\n"
            
            # 发送数据
            ser.write(message.encode('utf-8'))
            print(f"发送: {message.strip()}")
            
            counter += 1
            time.sleep(1)  # 每秒发送一次
    
    except serial.SerialException as e:
        print(f"串口错误: {e}")
        print("提示: 请确保串口设备正确连接，并且有读写权限")
        print("可尝试: sudo chmod 666 /dev/ttyUSB0")
    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        # 确保关闭串口
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("串口已关闭")

if __name__ == "__main__":
    send_data_to_windows()
