import serial
import time
import solve

# Arduinoのポートを指定
arduino = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Arduinoとの接続待ち

x_angles = [60, 85, 120, 150]
y_angles = [(45,143), (37,125), (35,105), (22,75)]
speed = 30  # モーターの速度

# dir = 0:右, 1:下, 2:左, 3:上
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

def send_angles(x_angle, y0_angle, y1_angle):
    """角度をArduinoに送信"""
    arduino.write(bytes([2, y1_angle, speed]))
    arduino.write(bytes([0, x_angle, 100]))
    arduino.write(bytes([1, y0_angle, speed]))

def move(y, x, dir):
    """(y, x) を dir 方向に1マス移動"""
    print(f"  開始位置: ({y}, {x}), 方向: {dir}")
    
    angle0 = (x_angles[x], y_angles[y][0], y_angles[y][1])
    angle0_f = (x_angles[x], y_angles[y][0]+20, y_angles[y][1])
    send_angles(*angle0_f)
    time.sleep(1)
    send_angles(*angle0)
    time.sleep(0.5)

    y += dy[dir]
    x += dx[dir]
    angle1 = (x_angles[x] + dx[dir]*30, y_angles[y][0], y_angles[y][1] - dy[dir]*15)
    angle1_f = (x_angles[x] + dx[dir]*30, y_angles[y][0]+20, y_angles[y][1] - dy[dir]*15)
    send_angles(*angle1)
    time.sleep(0.5)
    send_angles(*angle1_f)
    time.sleep(0.3)

def init():
    """初期位置に移動"""
    print("初期位置に移動中...")
    send_angles(
        (x_angles[1]+x_angles[2]) // 2,
        (y_angles[1][0]+y_angles[2][0]) // 2 + 20,
        (y_angles[1][1]+y_angles[2][1]) // 2
    )
    time.sleep(1)

def final():
    print("完成の舞")
    for _ in range(5):
        send_angles(150,(y_angles[1][0]+y_angles[2][0]) // 2 + 20,(y_angles[1][1]+y_angles[2][1]) // 2)
        time.sleep(0.5)
        send_angles(50,(y_angles[1][0]+y_angles[2][0]) // 2 + 20,(y_angles[1][1]+y_angles[2][1]) // 2)
        time.sleep(0.5)
    
def main():
    print("==== システム開始 ====")
    print("パス計算中...")
    path = solve.solve_puzzle()
    total_steps = len(path)
    print(f"パス取得完了。全 {total_steps} ステップ。")

    init()
    for i, (y, x, dir) in enumerate(path):
        remaining = total_steps - i
        print(f"\n--- ステップ {i+1}/{total_steps} | 残り {remaining - 1} ステップ ---")
        try:
            move(y, x, dir)
        except ValueError:
            print("無効な入力です。形式: (y, x, dir)")
        except KeyboardInterrupt:
            print("\n操作が中断されました。終了します。")
            break
        
    final()
    print("\n==== 操作完了。Arduinoとの接続を終了します。 ====")
    arduino.close()

if __name__ == "__main__":
    main()
