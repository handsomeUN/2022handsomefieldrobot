char Receiver, STAGE, STATE, pwmL[4], pwmR[4];
int PWM_L, PWM_R;
String commandStr;
const int motor_Lf=60, motor_Lb=61, motor_Rf=62, motor_Rb=63; // A6,A7,A8,A9

void setup(){
    // motor pins
    pinMode(60, OUTPUT);
    pinMode(61, OUTPUT);
    pinMode(62, OUTPUT);
    pinMode(63, OUTPUT);
}


void loop(){

   if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        //Serial.println("D Arduino received");
        //Serial.println(commandStr);
        
        Receiver = commandStr[0];
        STAGE = commandStr[1];
        STATE = commandStr[2];

        pwmL[0] = commandStr[3];
        pwmL[1] = commandStr[4];
        pwmL[2] = commandStr[5];
        pwmL[3] = '\0';
        PWM_L = atoi(pwmL);

        pwmR[0] = commandStr[6];
        pwmR[1] = commandStr[7];
        pwmR[2] = commandStr[8];
        pwmR[3] = '\0';
        PWM_R = atoi(pwmR);
/* 
        frontCamLED = commandStr[9];
        sideCamLED = commandStr[10];
        stepperMotor = commandStr[11];
        pump = commandStr[12]; */
        //other = commandStr[13];
    }

    runMotor(PWM_L,PWM_R);
}



void runMotor(int pwm_L, int pwm_R){
  
  Serial.println("D run motor!!!");
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
