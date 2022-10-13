#include <Servo.h>
#include <Unistep2.h>
Servo myservo0;
Servo myservo1;


Unistep2 stepper1(38, 39, 40, 41, 4096, 1000);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros)
Unistep2 stepper2(42, 43, 44, 45, 4096, 1000);// IN1, IN2, IN3, IN4, 總step數, 每步的延遲(in micros)

char color; 
int watering =0; 
int stepper_front = 0;
int stepper_front_ag = 0;
int stepper_initial=0;
int stepper_back = 0;


void setup(){
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  myservo0.attach(A0);  
  myservo0.write(90);
  myservo1.attach(A1);  // attaches the servo on pin A0 to the servo object
  myservo1.write(0);
  digitalWrite(4,LOW);
  Serial.begin(9600);
}

void loop() {
  //讀取序列埠傳入的字元
    if(Serial.available()){                   //決定顏色 紅藍不用再伸 黑黃要
      color = Serial.read();
      Serial.println(color);
    } 
      stepper1.run();
      stepper2.run();

    if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_front == 0 ){   //原先伸長 到紅藍位置
        stepper1.move(9100);        // can change
        stepper2.move(9100);  
        stepper_initial++;
    }

    while(color =='r' || color =='b'){
      //stepper1.run();       //不確定要不要註解...
      //stepper2.run();
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_front == 0 ){ 
        stepper1.move(9100);  
        stepper2.move(9100);  
        stepper_front++;
      }
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && watering == 0 ){
        digitalWrite(4,HIGH);
        delay(38000);
        digitalWrite(4,LOW);
        watering ++;
      }
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_back == 0 ){ // 如果stepsToGo=0，表示步進馬達已轉完應走的step了
        stepper1.move(-9100);
        stepper2.move(-9100);   
        stepper_back++;
      }
    }
 
    while(color =='k' || color =='y'){
      //stepper1.run();       //不確定要不要註解...
      //stepper2.run();
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_front_ag == 0 ){ // 如果stepsToGo=0，表示步進馬達已轉完應走的step了
        stepper1.move(900);   //can change
        stepper2.move(900);  
        stepper_front_ag++;
      }
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && watering == 0 ){
        digitalWrite(4,HIGH);
        delay(38000);
        digitalWrite(4,LOW);
        watering ++;
      }
      if(stepper1.stepsToGo() == 0 && stepper2.stepsToGo() == 0 && stepper_back == 0 ){ // 如果stepsToGo=0，表示步進馬達已轉完應走的step了
        stepper1.move(-10000);    //can change stepper_front_ag + stepper_initial
        stepper2.move(-10000);   
        stepper_back++;
      }
    }

  }