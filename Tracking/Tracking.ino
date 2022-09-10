int ultra_trig_pin[4] = {11,12,13,14};
int ultra_echo_pin[4] = {15,16,17,18};
const int a_b_boundary=10,b_c_boundary=30,c_d_boundary=60;
char Receiver, STAGE, STATE, pwmL[4], pwmR[4];
int PWM_L, PWM_R;
String commandStr;

void setup(){

    pinMode(11,OUTPUT);
    pinMode(12,OUTPUT);
    pinMode(13,OUTPUT);
    pinMode(14,OUTPUT);

    pinMode(15,INPUT);
    pinMode(16,INPUT);
    pinMode(17,INPUT);
    pinMode(18,INPUT);
}


void loop(){

    //Serial.println("A039898e");
   if(Serial.available()){
        commandStr = Serial.readStringUntil('e');
        //Serial.println("D Arduino received");
        //Serial.println(commandStr);
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
/* 
        frontCamLED = commandStr[9];
        sideCamLED = commandStr[10];
        stepperMotor = commandStr[11];
        pump = commandStr[12]; */
        //other = commandStr[13];
    }
    char A,B,C,D;
    int A_read = get_distance(ultra_trig_pin[0],ultra_echo_pin[0]);
    int B_read = get_distance(ultra_trig_pin[1],ultra_echo_pin[1]);
    int C_read = get_distance(ultra_trig_pin[2],ultra_echo_pin[2]);
    int D_read = get_distance(ultra_trig_pin[3],ultra_echo_pin[3]);
    
    if(A_read<a_b_boundary)
        A = 'a';
    else if(A_read<b_c_boundary)
        A = 'b';
    else if(A_read<c_d_boundary)
        A = 'c';
    else
        A = 'd';

    if(B_read<a_b_boundary)
        B = 'a';
    else if(B_read<b_c_boundary)
        B = 'b';
    else if(B_read<c_d_boundary)
        B = 'c';
    else
        B = 'd';

    if(C_read<a_b_boundary)
        C = 'a';
    else if(C_read<b_c_boundary)
        C = 'b';
    else if(C_read<c_d_boundary)
        C = 'c';
    else
        C = 'd';

    if(D_read<a_b_boundary)
        D = 'a';
    else if(D_read<b_c_boundary)
        D = 'b';
    else if(D_read<c_d_boundary)
        D = 'c';
    else
        D = 'd';

    String info = "P00001";
    info += A;
    info += B;
    info += C;
    info += D;
    info += 'e';
    Serial.println(info);  

}


int get_distance(int trigPin,int echoPin){

    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    int duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    int distance = duration * 0.034 / 2;
    return distance;
}