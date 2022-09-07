/* serial unavailable */
/* commandStr: Receiver/STAGE/STATE/pwmL/pwmR/frontCamLED/sideCamLED/StepperMotor/Pump */



// include all the libraries
#include <LiquidCrystal_PCF8574.h>

LiquidCrystal_PCF8574 lcd(0x27);

// pins
int displayerLED_pin[3] = {2,4,7}; //{23,25,27}; // R,G,B
int frontCamLED_pin[3] = {29,31,33}; 
int sideCamLED_pin[3] = {35,37,39}; 
//int stage_button_pin[8] = {36,22,24,26,28,30,32,34}; // STOP,N1,N2,N3,T1,T2,T3,U (Arduino mega2560)
int stage_button_pin[8] = {12,8,9,10,11,28,32,34}; // STOP,N1,N2,N3,T1,T2,T3,U


// declarations
String commandStr;
char Receiver, STAGE, STATE, pwmL[4], pwmR[4], frontCamLED, sideCamLED, stepperMotor, pump, other;
int PWM_L, PWM_R;

void setup(){
    Serial.begin(9600);
    lcd.begin(16, 2);
    lcd.setBacklight(255);
    
    lcd.setCursor(0, 0);
    lcd.print("STAGE:     ");
    lcd.setCursor(0, 1);
    lcd.print("STATE:     ");
    
}

void loop(){

    //Serial.println("A039898e");
    if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        Serial.print("From python:");
        Serial.println(commandStr);
        //commandStr = "A1011234344";
        
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
        other = commandStr[13];
    }
    
    // LCD
    // LCD_display_STAGE_STATE(STAGE,STATE);
    
    // LED
    LED_display_STAGE_STATE(STAGE,STATE);
    
    if(Receiver=='A'){ // python->arduino
        
        switch(STAGE){
            case '0': // STOP
            {
                // set commandStr: A0....
                // place the to-be-tested code here
            }
            case '1': // N1
            {
                
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
    STAGE_change_buttons();
 
}

void LCD_display_STAGE_STATE(char stage, char state){
    
    //lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("STAGE:     ");
    lcd.setCursor(0, 1);
    lcd.print("STATE:     ");
    
    lcd.setCursor(6, 0);
    lcd.print(STAGE_char2Str(stage));
    lcd.setCursor(6, 1);
    lcd.print("TRACK");

}


void LED_display_STAGE_STATE(char stage,char state){

    switch (state)
    {
    case '0': // TRACK
        igniteLED(displayerLED_pin,'3'); // green
        break;
    case '1': // TRACK_R
        igniteLED(displayerLED_pin,'5') ;// cyan
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
    case '6': // FIND_SIGN, FIND_FRUIT, FIND_CASE
        igniteLED(displayerLED_pin,'0');  
        break;
    case '7': // WATER_CASE
        igniteLED(displayerLED_pin,'7'); // megenta
        break;
    case '8': // TRACK_U
        igniteLED(displayerLED_pin,'5'); // cyan 
        break;
    case '9': // SWITCH
        igniteLED(displayerLED_pin,'1'); // white 
        break;   
    
    default:
        break;
    }

}



String STAGE_char2Str(char stage){
    switch(stage){
        case '0':
            return "STOP";
        case '1':
            return "N1";
        case '2':
            return "N2";
        case '3':
            return "N3";
        case '4':
            return "T1";
        case '5':
            return "T2";
        case '6':
            return "T3";
        case '7':
            return "U";
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

void resetLED(){
     igniteLED(displayerLED_pin,'0');
     igniteLED(frontCamLED_pin,'0');
     igniteLED(sideCamLED_pin,'0');
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

void STAGE_change_buttons(){

   if(digitalRead(stage_button_pin[1])==HIGH | digitalRead(stage_button_pin[2])==HIGH ){
       digitalWrite(13,HIGH);
   }else{
       digitalWrite(13,LOW);
   }




     if(digitalRead(stage_button_pin[0])==HIGH){ // STOP
      delay(200);
      if(digitalRead(stage_button_pin[0])==HIGH){
          Serial.println("D change STAGE");  
          Serial.println("P100aaaawwe");
          digitalWrite(13,HIGH);
      }
    } 
    
   if(digitalRead(stage_button_pin[1])==HIGH){ // N1
      delay(200);
      if(digitalRead(stage_button_pin[1])==HIGH){
          Serial.println("D change STAGE");  
          Serial.println("P110aaaawwe");
      }
    }

     if(digitalRead(stage_button_pin[2])==HIGH){ // N2
      delay(200);
      if(digitalRead(stage_button_pin[2])==HIGH){
          Serial.println("D change STAGE");  
          Serial.println("P120aaaawwe");
          digitalWrite(13,HIGH);
      }
    } 

   if(digitalRead(stage_button_pin[3])==HIGH){ // N3
      delay(200);
      if(digitalRead(stage_button_pin[3])==HIGH){
          Serial.println("D change STAGE");  
          Serial.println("P130aaaawwe");
      }
    }

     if(digitalRead(stage_button_pin[4])==HIGH){ // T1
      delay(200);
      if(digitalRead(stage_button_pin[4])==HIGH){
          Serial.println("D change STAGE");  
          Serial.println("P140aaaawwe");
          digitalWrite(13,HIGH);
      }
    } 
    
}