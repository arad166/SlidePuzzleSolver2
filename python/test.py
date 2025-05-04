import serial
import time

# Arduinoと接続しているCOMポートに変更してください
ser = serial.Serial('COM6', 9600)
time.sleep(2)  # Arduinoリセット待ち

def set_servo(index, angle, speed):
    if not (0 <= index <= 2):
        raise ValueError("index must be 0, 1, or 2")
    if not (0 <= angle <= 180):
        raise ValueError("angle must be between 0 and 180")
    if not (1 <= speed <= 255):
        raise ValueError("speed should be 1~255 (higher is faster)")

    ser.write(bytes([index, angle, speed]))
    
while True:
    index,angle,speed = map(int, input("Enter index, angle, speed (0-2, 0-180, 1-255): ").split())
    set_servo(index, angle, speed)