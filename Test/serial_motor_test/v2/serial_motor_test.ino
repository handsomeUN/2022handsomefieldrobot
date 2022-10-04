char Receiver, STAGE, STATE, pwmL[4], pwmR[4];
int PWM_L, PWM_R;
String commandStr;

int motor_Lf = 12;
int motor_Lb = 13;
int motor_Rf = 6;
int motor_Rb = 5;

int len1 = 9;
int ren1 = 10;
int len2 = 7;
int ren2 = 8;


void setup(){
    // motor pins
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);

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
  
   if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        //Serial.println("D Arduino received");
        //Serial.println(commandStr);
        
        Receiver = commandStr[0];
        STAGE = commandStr[1];
        STATE = commandStr[2];

        if(commandStr[3] != '-'){
            pwmL[0] = commandStr[3];
            pwmL[1] = commandStr[4];
            pwmL[2] = commandStr[5];
            pwmL[3] = '\0';
            PWM_L = atoi(pwmL);
        }else{
            pwmL[0] = commandStr[4];
            pwmL[1] = commandStr[5];
            pwmL[2] = '\0';
            PWM_L = -10*atoi(pwmL);
        }

        if(commandStr[6] != '-'){
            pwmR[0] = commandStr[6];
            pwmR[1] = commandStr[7];
            pwmR[2] = commandStr[8];
            pwmR[3] = '\0';  
            PWM_R = atoi(pwmR);
        }else{
            pwmR[0] = commandStr[7];
            pwmR[1] = commandStr[8];
            pwmR[2] = '\0';
            pwmR[3] = '\0';
            PWM_R = -10*atoi(pwmR);
        }
         //Serial.println(PWM_L);
         runMotor(PWM_L,PWM_R);
    }
    
}



void runMotor(int pwm_L, int pwm_R){
  
  //Serial.println("run motor!!!");
  Serial.print("pwm L:");
  Serial.println(pwm_L);
  Serial.print("pwm R:");
  Serial.println(pwm_R);

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
