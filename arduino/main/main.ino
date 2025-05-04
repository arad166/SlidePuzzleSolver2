#include <VarSpeedServo.h>

VarSpeedServo servos[3];
int positions[3] = {90, 90, 90};  // 初期位置

void setup() {
  Serial.begin(9600);
  servos[0].attach(9);  // Servo 0
  servos[1].attach(10); // Servo 1
  servos[2].attach(11); // Servo 2

  // 初期位置に移動
  for (int i = 0; i < 3; i++) {
    servos[i].write(positions[i], 0, true); // 速度0=瞬時移動, true=ブロッキング
  }
}

void loop() {
  if (Serial.available() >= 3) {
    int index = Serial.read();
    int angle = Serial.read();
    int speed = Serial.read(); // 1〜255（VarSpeedServoの速度設定）

    if (index >= 0 && index < 3 && angle >= 0 && angle <= 180 && speed > 0 && speed <= 255) {
      servos[index].write(angle, speed, false); // false=ノンブロッキング
      positions[index] = angle;
    }
  }

  // 必要であれば他の処理をここに書く（非同期制御が可能）
}
