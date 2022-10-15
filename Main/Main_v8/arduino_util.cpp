#include "arduino_util.h"
#include <LiquidCrystal_PCF8574.h>
#include <Arduino.h>
#include <Wire.h>

UTIL::UTIL(){
}

UTIL::~UTIL(){}

String UTIL::STAGE_char2Str(char stage){
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


String UTIL::STATE_char2Str(char state){
    switch(state){
        case '0':
            return "TRACK         ";
        case '1':
            return "TRACK_R       ";
        case '2':
            return "SLOW          ";
        case '3':
            return "DRIFT         ";
        case '4':
            return "TURN          ";
        case '5':
            return "U_TURN        ";
        case '6':
            return "FIND          ";
        case '7':
            return "WATER_CASE    ";
        case '8':
            return "TRACK_U       ";
        case '9':
            return "SWITCH        ";
    }
}

void UTIL::LED_display_STAGE_STATE(int displayerLED_pin[],char stage,char state){

    switch (state)
    {
    case '0': // NON
        igniteLED(displayerLED_pin,'1'); // no light
        break;
    case '1': // TRACK
        igniteLED(displayerLED_pin,'3');// green
        break;
    case '2': // SLOW
        igniteLED(displayerLED_pin,'2'); // red
        break;
    case '3': // DRIFT
        igniteLED(displayerLED_pin,'6'); // yellow
        break;
    case '4': // TURN
        igniteLED(displayerLED_pin,'4'); // blue 
        break;
    case '5': // U_TURN
        igniteLED(displayerLED_pin,'4'); // blue 
        break;
    case '6': // TRACK_U
        igniteLED(displayerLED_pin,'5'); // cyan 
        break;
    case '7': // SWITCH
        igniteLED(displayerLED_pin,'1'); // white 
        break;   
    case 'S': // SIGN
        //igniteLED(displayerLED_pin,'1'); // white 
        break;   
    case 'F': // FRUIT
        //igniteLED(displayerLED_pin,'1'); // white 
        break;   
    case 'G': // GRAB
        igniteLED(displayerLED_pin,'7'); // megenta 
        break;   
    case 'D': // DROP
        igniteLED(displayerLED_pin,'7'); // megenta 
        break;   
    
    default:
        break;
    }

}


void UTIL::igniteLED(int LEDpins[] ,char choice){
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

void UTIL::light(int R,int G,int B,int r,int g,int b){
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

void UTIL::resetLED(int displayerLED_pin[],int frontCamLED_pin[],int sideCamLED_pin[]){
     igniteLED(displayerLED_pin,'0');
     igniteLED(frontCamLED_pin,'0');
     igniteLED(sideCamLED_pin,'0');
}

void UTIL::STAGE_change_buttons(int stage_button_pin[]){

   if(analogRead(stage_button_pin[0])>1020 | analogRead(stage_button_pin[1])>1020 | analogRead(stage_button_pin[2])>1020 | analogRead(stage_button_pin[3])>1020 | 
             analogRead(stage_button_pin[4]>1020) ){
       digitalWrite(13,HIGH);
   }else{
       digitalWrite(13,LOW);
   }

    if(analogRead(stage_button_pin[0])>1020){ // STOP
      digitalWrite(13,HIGH);
      delay(100);
      if(analogRead(stage_button_pin[0])>1020){
          //Serial.println("D change STAGE to: STOP");  
          Serial.println("P10xx");          
      }
      digitalWrite(13,LOW);
    }
    
   if(analogRead(stage_button_pin[1])>1020){ // N1
      delay(100);
      if(analogRead(stage_button_pin[1])>1020){
          //Serial.println("D change STAGE to: N1");  
          Serial.println("P11xx");
      }
    }

     if(analogRead(stage_button_pin[2])>1020){ // N2
      delay(100);
      if(analogRead(stage_button_pin[2])>1020){
          //Serial.println("D change STAGE to: N2");  
          Serial.println("P12xx");
          digitalWrite(13,HIGH);
      }
    } 

   if(analogRead(stage_button_pin[3])>1020){ // N3
      delay(100);
      if(analogRead(stage_button_pin[3])>1020){
          //Serial.println("D change STAGE to: N3 ");  
          Serial.println("P13xx");
      }
    }

     if(analogRead(stage_button_pin[4])>1020){ // T1
      delay(100);
      if(analogRead(stage_button_pin[4])>1020){
          //Serial.println("D change STAGE to: T1"); 
          Serial.println("P14xx");
          digitalWrite(13,HIGH);
      }
    } 

     if(analogRead(stage_button_pin[5])>1020){ // T2
      delay(100);
      if(analogRead(stage_button_pin[5])>1020){
          //Serial.println("D change STAGE to: T2"); 
          Serial.println("P15xx");
          digitalWrite(13,HIGH);
      }
    } 

     if(analogRead(stage_button_pin[6])>1020){ // T3
      delay(100);
      if(analogRead(stage_button_pin[6])>1020){
          //Serial.println("D change STAGE to: T3"); 
          Serial.println("P16xx");
          digitalWrite(13,HIGH);
      }
    } 

     if(analogRead(stage_button_pin[7])>1020){ // U
      delay(100);
      if(analogRead(stage_button_pin[7])>1020){
          //Serial.println("D change STAGE to: U"); 
          Serial.println("P17xx");
          digitalWrite(13,HIGH);
      }
    } 
}
