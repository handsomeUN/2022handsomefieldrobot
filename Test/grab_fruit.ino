#include <Servo.h>
#include <Unistep2.h>

Servo myservo1;


Unistep2 stepper1(38, 39, 40, 41, 4096, 1000);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros)
Unistep2 stepper2(42, 43, 44, 45, 4096, 1000);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros)

int stepper_front = 0;
int stepper_back = 0;
int grab = 0;
char go_grab;

void setup(){
  pinMode(A1, OUTPUT);
  myservo1.attach(A1);  // attaches the servo on pin 9 to the servo object
  myservo1.write(0);
  Serial.begin(9600);
}

void loop() {
  //讀取序列埠傳入的字元
  if(Serial.available()){
    go_grab=Serial.read();
    Serial.println(go_grab);
  } 
  while(go_grab == 'g'){
        stepper1.run();
        stepper2.run();
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_front == 0 ){ // 如果stepsToGo=0，表示步進馬達已轉完應走的step了
        stepper1.move(9100);  
        stepper2.move(9100);  
        stepper_front++;
      }
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && grab == 0) {
        myservo1.write(0);
        delay(3000);
        myservo1.write(40);
        delay(3000);
        grab ++;
      }
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_back == 0 ){ // 如果stepsToGo=0，表示步進馬達已轉完應走的step了
        stepper1.move(-9100);
        stepper2.move(-9100);   
        stepper_back++;
      }
  }
  
}