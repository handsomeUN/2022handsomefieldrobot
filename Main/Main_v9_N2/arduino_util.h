#ifndef UTIL_H

#define UTIL_H


#include <Arduino.h>
#include <LiquidCrystal_PCF8574.h>
#include <Wire.h>

class UTIL {

public:

UTIL();
~UTIL();

//void LCD_display_STAGE_STATE(
//LiquidCrystal_PCF8574 LCD,char stage, char state);
String STAGE_char2Str(char stage);
String STATE_char2Str(char state);
void igniteLED(int LEDpins[] ,char choice);
void LED_display_STAGE_STATE(int displayerLED_pin[],char stage,char state);
void light(int R,int G,int B,int r,int g,int b);
void resetLED(int displayerLED_pin[],int frontCamLED_pin[],int sideCamLED_pin[]);
void STAGE_change_buttons(int stage_button_pin[]);
void TRACK_checkDist(int DistL,int DistR);
void runMotor(int pwm_L, int pwm_R);
};

 

#endif
