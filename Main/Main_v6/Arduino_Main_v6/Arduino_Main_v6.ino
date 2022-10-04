/* serial unavailable */
/* commandStr: Receiver/STAGE/STATE/pwmL/pwmR/frontCamLED/sideCamLED/StepperMotor/Pump */

// include all the libraries
#include <LiquidCrystal_PCF8574.h>
#include "arduino_util.h"

UTIL U;
LiquidCrystal_PCF8574 lcd(0x27);

// pins
int displayerLED_pin[3] = {29,30,31}; 
int frontCamLED_pin[3] = {32,33,34};
int sideCamLED_pin[3] = {35,36,37};
int ultraLED_pin[3] = {26,27,28};
int stage_button_pin[8] = {53,8,47,48,49,50,51,52}; // STOP,N1,N2,N3,T1,T2,T3,U
int ultra_trig_pin[2] = {22,24};
int ultra_echo_pin[2] = {23,25};

int motor_Lf = 13, motor_Lb = 12, motor_Rf = 6, motor_Rb = 5;
int len1 = 9, ren1 = 10, len2 = 7, ren2 = 8;

int stepper_motor_A[4] = {8,9,10,11};
int stepper_motor_B[4] = {38,39,40,41};
int pump_relay = 7;
int servo_claw = 58; // A4
int servo_camera = 59; // A5

// declarations
String commandStr;
char Receiver, STAGE, STATE, pwmL[4], pwmR[4], frontCamLED, sideCamLED, stepperMotor, pump, other;
int PWM_L, PWM_R;

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

    
    pinMode(11,OUTPUT);
    pinMode(12,OUTPUT);
    pinMode(13,OUTPUT);
    pinMode(14,OUTPUT);

    pinMode(15,INPUT);
    pinMode(16,INPUT);
    pinMode(17,INPUT);
    pinMode(18,INPUT);

    Serial.begin(9600);
    lcd.begin(16, 2);
    lcd.setBacklight(255);
}

void loop(){

   if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        //Serial.println("D Arduino received");
        
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
    U.LCD_display_STAGE_STATE(lcd,STAGE,STATE);

    // LED
    U.LED_display_STAGE_STATE(displayerLED_pin,STAGE,STATE);
    
    if(Receiver=='A'){ // python->arduino
        
        switch(STAGE){
            case '0': // STOP
            {
                // set commandStr: A0....
                // place the to-be-tested code here
            }
            case '1': // N1
            {
                if(STATE==0){ // TRACK
                }
            }
            case '2': // N2
            {
                
            }
            case '3': // N3
            {
                
            }
            case '4': // T1
            {
                
            }
            case '5': // T2
            {
                
            }
            case '6': // T3
            {
                
            }
            case '7': // U
            {
                
            }
        }
        
    }

    // STAGE-change buttons
    U.STAGE_change_buttons(stage_button_pin);
    delay(100);
 
}
