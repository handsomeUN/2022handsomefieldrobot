char Num; 
void setup() {
 pinMode(8,OUTPUT);
 Serial.begin(9600);
}

void loop() {
  //讀取序列埠傳入的字元
  if(Serial.available()){
    Num=Serial.read();
    Serial.println(Num);
  } 
  delay(10);
  if(Num=='1'){
    digitalWrite(8,LOW); //低電平觸發，LOW時繼電器觸發
  }
  else{
    digitalWrite(8,HIGH);
  }
}