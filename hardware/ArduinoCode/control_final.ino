#include <Servo.h>

//For 5 continuous servo motors:
Servo neuroServoIndex;
Servo neuroServoMiddle;
Servo neuroServoRing;
Servo neuroServoPinky;
Servo neuroServoThumb;


int pinsIndex   = 9;    //pin connection
int pinsMiddle  = 10;   //pin connection
int pinsRing    = 11;   //pin connection
int pinsPinky   = 12;   //pin connection
int pinsThumb   = 2;    //pin connection


int readIndex   = A0;
int readMiddle  = A1;
int readRing    = A2;
int readPinky   = A3;


void setup() {
 // put your setup code here, to run once:
 Serial.begin(9600);
 pinMode(LED_BUILTIN, OUTPUT);
 neuroServoIndex.attach(pinsIndex);
 neuroServoMiddle.attach(pinsMiddle);
 neuroServoRing.attach(pinsRing);
 neuroServoPinky.attach(pinsPinky);
 neuroServoThumb.attach(pinsThumb);

 pinMode(readIndex, INPUT);
 pinMode(readMiddle, INPUT);
 pinMode(readRing, INPUT);
 pinMode(readPinky, INPUT);

 if(closed(readIndex)){
  Serial.println("Index Ready");
 }
 else{
  Serial.println("Index NOT Ready");
 }
 if(closed(readMiddle)){
  Serial.println("Middle Ready");
 }
 else{
  Serial.println("Middle NOT Ready");
 }
 if(closed(readRing)){
  Serial.println("Ring Ready");
 }
 else{
  Serial.println("Ring NOT Ready");
 }
 if(closed(readPinky)){
  Serial.println("Pinky Ready");
 }
 else{
  Serial.println("Pinky NOT Ready");
 }
}

bool closed(int finger) {
  int r1 = analogRead(finger);
  int r2 = analogRead(finger);
  int r3 = analogRead(finger);

  if(r1 > 1000 && r2 > 1000 && r3 > 1000){
    Serial.println("yes");
    return true;
  }
  else{
    return false;
  }
}

void contract(int sig, Servo motor, int del, bool flag){
  int count = 0;
  while(!flag && count < 200){
    motor.write(0);
    delay(del);
    motor.write(90);
    flag    = closed(sig);
    bool temp_flag = closed(sig);
    flag = flag + temp_flag;
    count++;    
  }
}

void loop() {

 if (Serial.available()){
   char data = Serial.read();
   if (data == '1'){
     //Write to index, middle, ring, and pinky fingers
     digitalWrite(LED_BUILTIN, HIGH);
     neuroServoIndex.write(180);
     neuroServoMiddle.write(180);
     neuroServoRing.write(180);
     neuroServoPinky.write(180);
     delay(900);
     neuroServoIndex.write(90);
     neuroServoMiddle.write(90);
     delay(300);
     neuroServoPinky.write(90);
     delay(200);
     neuroServoRing.write(90);

     //Write to thumb
     neuroServoThumb.write(180);
     delay(400);
     neuroServoThumb.write(90);
   }
   else if (data == '0'){
    bool flagIndex    = closed(readIndex);  Serial.println((int)flagIndex);
    bool flagMiddle   = closed(readMiddle); Serial.println((int)flagMiddle);
    bool flagRing     = closed(readRing);   Serial.println((int)flagRing);
    bool flagPinky    = closed(readPinky);  Serial.println((int)flagPinky);

    contract(readPinky, neuroServoPinky, 4, flagPinky);
    contract(readRing, neuroServoRing, 6, flagRing);
    contract(readMiddle, neuroServoMiddle, 4, flagMiddle);
    contract(readIndex, neuroServoIndex, 6, flagIndex);
    // int counter = 0;

    // while((!(flagIndex && flagMiddle && flagRing && flagPinky)) && counter < 200){
    //   if(!flagIndex){
    //     neuroServoIndex.write(0);
    //     delay(8);
    //     neuroServoIndex.write(90);
    //     flagIndex    = closed(readIndex);
    //   }
    //   if(!flagMiddle){
    //     neuroServoMiddle.write(0);
    //     delay(4);
    //     neuroServoMiddle.write(90);
    //     flagMiddle    = closed(readMiddle);
    //           Serial.println(counter);
    //   }
    //   if(!flagRing){
    //     neuroServoRing.write(0);
    //     delay(4);
    //     neuroServoRing.write(90);
    //     flagRing    = closed(readRing);
    //   }
    //   if(!flagPinky){
    //     neuroServoPinky.write(0);
    //     delay(4);
    //     neuroServoPinky.write(90);
    //     flagPinky    = closed(readPinky);
    //   }
    //   counter++;
    //   // Serial.println(counter);
    // }

     //Write to thumb
     neuroServoThumb.write(0);
     delay(400);
     neuroServoThumb.write(90);
   }
 }
}