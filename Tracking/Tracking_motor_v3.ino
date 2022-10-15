/*

1. 右前和左前超音波，分別為(24,25),(18,19)
2. ultraLED 接(26,27,28)
3. motor接(5,6,11,12)
4. 先測試右邊
5. 可根據超音波的距離換算角度
6. 測試成功寫左邊

*/

#include <Ultrasonic.h>
int ultra_trig_pin[2] = {24,18};
int ultra_echo_pin[2] = {25,19};
int TRACK_ultra_LED[3] = {26,27,28};

int motor_Lf = 11;
int motor_Lb = 12;
int motor_Rf = 5;
int motor_Rb = 6;

int len1 = 9;
int ren1 = 10;
int len2 = 7;
int ren2 = 8;

char Receiver, STAGE, STATE, pwmL[4], pwmR[4];
int PWM_L=0, PWM_R=0;
String commandStr;

Ultrasonic Ultra_L(ultra_trig_pin[0],ultra_echo_pin[0]);
Ultrasonic Ultra_R(ultra_trig_pin[1],ultra_echo_pin[1]);


void setup(){
    
    // ultra pins
    pinMode(22,OUTPUT);
    pinMode(24,OUTPUT);
    pinMode(23,INPUT);
    pinMode(25,INPUT);

    // ultra LED pins
    pinMode(26,OUTPUT);
    pinMode(27,OUTPUT);
    pinMode(28,OUTPUT);

    // motor pins
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(11, OUTPUT);
    pinMode(12, OUTPUT);

    pinMode(len1,OUTPUT);
    pinMode(ren1,OUTPUT);
    pinMode(len2,OUTPUT);
    pinMode(ren2,OUTPUT);
    digitalWrite(len1,HIGH);
    digitalWrite(ren1,HIGH);
    digitalWrite(len2,HIGH);
    digitalWrite(ren2,HIGH);

    Serial.begin(9600);
}


void loop(){

    int L_read=0, R_read=0;
    for(int i=0;i<20;i++){
        L_read += Ultra_L.read();
        R_read += Ultra_R.read();
        delay(10);
    }
    
    Serial.print("\nDist L: ");
    Serial.println(L_read/20);
    Serial.print("Dist R: ");
    Serial.println(R_read/20);

    // if too close then hard-coded go back, turn, and go forward
    // else then keep going straight
    TRACK_checkDist(L_read/20,R_read/20);

    //delay(1000);
    
}


void TRACK_checkDist(int DistL,int DistR){

    igniteLED(TRACK_ultra_LED,'3'); // green
    Serial.print("Keep going!!!");
    runMotor(200,200); // keep going straight

    if (DistR < 16)
    {
      igniteLED(TRACK_ultra_LED,'2'); // red
      Serial.print("DistR too close!!!");
      runMotor(-150,-150); // backward
      delay(900);
      igniteLED(TRACK_ultra_LED,'6'); // Y
      runMotor(-120,120); // turning
      delay(300);
    }

    if (DistL < 16)
    {
      igniteLED(TRACK_ultra_LED,'2'); // red
      Serial.print("DistL too close!!!");
      runMotor(-150,-150); // backward
      delay(900);
      igniteLED(TRACK_ultra_LED,'6'); // Y
      runMotor(120,-120); // turning
      delay(300);
    }


    



}



void igniteLED(int LEDpins[] ,char choice){
  int R = LEDpins[0];  
  int G = LEDpins[1];  
  int B = LEDpins[2];
  
  switch(choice){
    case '0':
      light(R,G,B,0,0,0);  // light off
      break;
      
    case '1':
      light(R,G,B,255,255,255);  // white
      break;
 
    case '2':
      light(R,G,B,255,0,0);  // Red
      break;

    case '3':
      light(R,G,B,0,255,0);  // Green
      break;
     
    case '4':
      light(R,G,B,0,0,255);  // Blue
      break;
    
    case '5':
      light(R,G,B,0,255,255);  // Cyan
      break;
      
    case '6':
      light(R,G,B,255,255,0);  // Yellow
      break;
      
    case '7':
      light(R,G,B,255,0,255);  // Megenta
      break;
      
  }
}


void light(int R,int G,int B,int r,int g,int b){
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  
    if(r==0){
      digitalWrite(R,LOW);
    }
    else{
      digitalWrite(R,HIGH);
    }
    if(g==0){
      digitalWrite(G,LOW);
    }
    else{
      digitalWrite(G,HIGH);
    }
    if(b==0){
      digitalWrite(B,LOW);
    }
    else{
      digitalWrite(B,HIGH);
    }
    
  }


void runMotor(int pwm_L, int pwm_R){
  
  //Serial.println("D run motor!!!");
  if(pwm_L>0){
    analogWrite(motor_Lf,pwm_L);
    analogWrite(motor_Lb,0);
  }else{
    analogWrite(motor_Lf,0);
    analogWrite(motor_Lb,-pwm_L);
  }
  
  if(pwm_R>0){
    analogWrite(motor_Rf,pwm_R);
    analogWrite(motor_Rb,0);
  }else{
    analogWrite(motor_Rf,0);
    analogWrite(motor_Rb,-pwm_R);
  }
  
}