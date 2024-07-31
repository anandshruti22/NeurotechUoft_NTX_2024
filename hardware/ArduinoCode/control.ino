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
     delay(1000);
     neuroServoIndex.write(90);
     neuroServoMiddle.write(90);
     neuroServoRing.write(90);
     neuroServoPinky.write(90);

     //Write to thumb
     neuroServoThumb.write(180);
     delay(800);
     neuroServoThumb.write(90);
   }
   else if (data == '0'){
    bool flagIndex    = closed(readIndex);
    bool flagMiddle   = closed(readMiddle);
    bool flagRing     = closed(readRing);
    bool flagPinky    = closed(readPinky);
    int counter = 0;

    while((!(flagIndex && flagMiddle && flagRing && flagPinky)) && counter < 130){
      if(!flagIndex){
        neuroServoIndex.write(0);
        delay(5);
        neuroServoIndex.write(90);
        flagIndex    = closed(readIndex);Serial.println(counter);
      }
      if(!flagMiddle){
        neuroServoMiddle.write(0);
        delay(2);
        neuroServoMiddle.write(90);
        flagMiddle    = closed(readMiddle);
      }
      if(!flagRing){
        neuroServoRing.write(0);
        delay(2);
        neuroServoRing.write(90);
        flagRing    = closed(readRing);
      }
      if(!flagPinky){
        neuroServoPinky.write(0);
        delay(2);
        neuroServoPinky.write(90);
        flagPinky    = closed(readPinky);
      }
      counter++;
      
    }

     //Write to thumb
     neuroServoThumb.write(0);
     delay(800);
     neuroServoThumb.write(90);
   }
 }
}