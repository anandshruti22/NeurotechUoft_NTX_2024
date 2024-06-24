#include <Servo.h>


//For 5 continuous servo motors:
Servo neuroServo1;
Servo neuroServo2;
Servo neuroServo3;
Servo neuroServo4;
Servo neuroServoThumb;




int pins1 = 9; //pin connection
int pins2 = 10; //pin connection
int pins3 = 11; //pin connection
int pins4 = 12; //pin connection
int pins5 = 2; //pin connection


void setup() {
 // put your setup code here, to run once:
 Serial.begin(9600);
 neuroServo1.attach(pins1);
 neuroServo2.attach(pins2);
 neuroServo3.attach(pins3);
 neuroServo4.attach(pins4);
 neuroServoThumb.attach(pins5);
}


void loop() {
 // put your main code here, to run repeatedly:


 if (Serial.available()){
   char data = Serial.read();
   if (data == '1'){
     neuroServo1.write(180);
     neuroServo2.write(180);
     neuroServo3.write(180);
     neuroServo4.write(180);
     delay(2000);
     neuroServoThumb.write(180);
     delay(1500);
     neuroServoThumb.write(92);
     delay(1000);
     neuroServo1.write(92);
     neuroServo2.write(92);
     neuroServo3.write(92);
     neuroServo4.write(92);
   }
   else if (data == '0'){
     neuroServo1.write(0);
     neuroServo2.write(0);
     neuroServo3.write(0);
     neuroServo4.write(0);
     delay(2000);
     neuroServoThumb.write(0);
     delay(1500);
     neuroServoThumb.write(92);
     delay(1000);
     neuroServo1.write(92);
     neuroServo2.write(92);
     neuroServo3.write(92);
     neuroServo4.write(92);
   }
 }
}

