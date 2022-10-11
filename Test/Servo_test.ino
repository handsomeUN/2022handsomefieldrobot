#include <Servo.h>

Servo Armservo1; 
//Servo Armservo2;

void setup() {
    Serial.begin(9600);
    Armservo1.attach(3);
    
}

void loop() {


    Armservo1.write(0);
    delay(1000);
    Armservo1.write(40);
    delay(1000);
  // Armservo1.write(60);
  //  Armservo2.write(60);
}
