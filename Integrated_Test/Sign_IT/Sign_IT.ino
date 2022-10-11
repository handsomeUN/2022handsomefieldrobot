/* serial unavailable */
/* commandStr: Receiver/STAGE/STATE/pwmL/pwmR/frontCamLED/sideCamLED/StepperMotor/Pump */

// include all the libraries
#include <LiquidCrystal_PCF8574.h>
#include <Wire.h>
#include <Ultrasonic.h>

#include "arduino_util.h"

UTIL U;
LiquidCrystal_PCF8574 lcd(0x27);

// pins
int displayerLED_pin[3] = {29,30,31}; 
int frontCamLED_pin[3] = {32,33,34};
int sideCamLED_pin[3] = {35,36,37};
int ultra_LED[3] = {26,27,28};
int ultraLED_pin[3] = {26,27,28};
int stage_button_pin[8] = {53,46,47,48,49,50,51,52}; // STOP,N1,N2,N3,T1,T2,T3,U
int ultra_trig_pin[4] = {16,18,22,24};
int ultra_echo_pin[4] = {17,19,23,25};

int motor_Hbridge_pin[4] = {12,11,6,5};
int motor_EN_pin[4] = {7,8,9,10};

int stepper_motor_A[4] = {38,39,40,41};
int stepper_motor_B[4] = {42,43,44,45};
int pump_relay = 4;
int servo_claw = 58; // A4
int servo_camera = 59; // A5

// declarations
String commandStr;
char Receiver, STAGE, STATE, pwmL[4], pwmR[4], frontCamLED, sideCamLED, stepperMotor, pump, other;
int PWM_L, PWM_R;

Ultrasonic Ultra_L(ultra_trig_pin[0],ultra_echo_pin[0]);
Ultrasonic Ultra_R(ultra_trig_pin[3],ultra_echo_pin[3]);

void setup(){

    pinMode(displayerLED_pin[0],OUTPUT);
    pinMode(displayerLED_pin[1],OUTPUT);
    pinMode(displayerLED_pin[2],OUTPUT);
    
    pinMode(frontCamLED_pin[0],OUTPUT);
    pinMode(frontCamLED_pin[1],OUTPUT);
    pinMode(frontCamLED_pin[2],OUTPUT);

    pinMode(sideCamLED_pin[0],OUTPUT);
    pinMode(sideCamLED_pin[1],OUTPUT);
    pinMode(sideCamLED_pin[2],OUTPUT);

    pinMode(stage_button_pin[0],INPUT);
    pinMode(stage_button_pin[1],INPUT);
    pinMode(stage_button_pin[2],INPUT);
    pinMode(stage_button_pin[3],INPUT);
    pinMode(stage_button_pin[4],INPUT);
    pinMode(stage_button_pin[5],INPUT);
    pinMode(stage_button_pin[6],INPUT);
    pinMode(stage_button_pin[7],INPUT);

    
    Serial.begin(9600);
    lcd.begin(16, 2);
    lcd.setBacklight(255);
    lcd.clear();
}

void loop(){
   
   // STAGE-change buttons
   U.STAGE_change_buttons(stage_button_pin);

   if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        //Serial.println("D Arduino received");
    
      //  while(commandStr[0] != 'A'){
      //    commandStr = Serial.readStringUntil('e');
      //  }
            
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

        frontCamLED = commandStr[9];
        sideCamLED = commandStr[10];
        stepperMotor = commandStr[11];
        pump = commandStr[12];
        //other = commandStr[13];
    }

    
    
    // LCD
    lcd.setCursor(0, 0);
    lcd.print("STAGE:     ");
    lcd.setCursor(0, 1);
    lcd.print("STATE:     ");
    
    lcd.setCursor(6, 0);
    lcd.print(STAGE_char2Str(STAGE)); //STAGE_char2Str(stage));
    lcd.setCursor(6, 1);
    lcd.print(STATE_char2Str(STATE)); //STATE_char2Str(state));

    // LED
    U.LED_display_STAGE_STATE(displayerLED_pin,STAGE,STATE);
    
    if(Receiver=='A'){ // python->Arduino

        if (STAGE=='0') // STOP
        {

        }
        if (STAGE=='1') // N1
        {
            if(STATE=='1'){ // TRACK
                int L_read=0, R_read=0;
                for(int i=0;i<20;i++){
                    L_read += Ultra_L.read();
                    R_read += Ultra_R.read();
                    delay(10);
                }
                U.TRACK_checkDist(L_read/20,R_read/20);
                delay(50);
            }
        }
        if (STAGE=='2') // N2
        {
            /* code */
        }
        if (STAGE=='3') // N3
        {
            /* code */
        }
        if (STAGE=='4') // T1
        {
            /* code */
        }
        if (STAGE=='5') // T2
        {
            /* code */
        }
        if (STAGE=='6') // T3
        {
            /* code */
        }
        while (STAGE=='7') // U
        {
            /* code */
        }


    delay(100);
 
}}


String STAGE_char2Str(char stage){
    switch(stage){
        case '0':
            return "STOP       ";
        case '1':
            return "N1         ";
        case '2':
            return "N2         ";
        case '3':
            return "N3         ";
        case '4':
            return "T1         ";
        case '5':
            return "T2         ";
        case '6':
            return "T3         ";
        case '7':
            return "U          ";
    }
}


String STATE_char2Str(char state){
    switch(state){
        case '0':
            return "NON         ";
        case '1':
            return "TRACK       ";
        case '2':
            return "SLOW          ";
        case '3':
            return "DRIFT         ";
        case '4':
            return "TURN          ";
        case '5':
            return "U_TURN        ";
        case '6':
            return "TRACK_U       ";
        case '7':
            return "SWITCH        ";
        case 'S':
            return "Find SIGN!!!  ";
        case 'F':
            return "Find FRUIT!!!  ";
        case 'G':
            return "Grabbing...  ";
        case 'D':
            return "Dropping...  ";

    }
}

