/*
 * Bailey Fokin
 * 
 * ENEE408i
 * 
 * Code description:       
 *    Serial Communications Test with the base cpu
 *    (pi4/NX)
 *    depending on what the input is in the serial
 *    the robot will move slightly
 *    
 *    Command code number
 *    0   Halts the robot
 *    1   wanders using ping sensors
 *    2   facerecognition (NOT USED HERE)
 *    3   dance
 *    4   forward
 */

 /*******************************************************************************************
 * Include Statements                                                                      *
 *******************************************************************************************/
#include <stdio.h>
#include <VNH3SP30.h>
#include "baymax.h"


/*******************************************************************************************
 * Define Statements                                                                       *
 *******************************************************************************************/
//compensation value : used to subtract from motor 1 to make the motors equal
#define COMP_SPEED 10

//motor 1 pins
#define M1_PWM 3    
#define M1_INA 4    
#define M1_INB 5

//motor 2 pins
#define M2_PWM 6
#define M2_INA 7
#define M2_INB 8 


/*******************************************************************************************
 * Objects                                                                                 *
 *******************************************************************************************/
VNH3SP30 motor_1;
VNH3SP30 motor_2; 

/*******************************************************************************************
 * Function Prototypes                                                                     *
 *******************************************************************************************/
//Main Functions
void setup(void);
void loop(void);

//Motor Functions
void turn(int spd, int in_place);
void brake(int brakePower);
void setSpeed(int speed);


/*******************************************************************************************
 * Void setup/ Void Loop                                                                   *
 *******************************************************************************************/
void setup() {
  //Init motors
  motor_1.begin(M1_PWM, M1_INA, M1_INB, -1, -1);
  motor_2.begin(M2_PWM, M2_INB, M2_INA, -1, -1); 
  
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  
   if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
    
    
    if (data == "forward") {
      setSpeed(50);
    }
    
    else if(data == "reverse") {
      setSpeed(-50);
    }
    
    else if(data == "right"){
      turn(50,1); //turn left      
    }
    
    else if(data == "left") {
      turn(-50,1); //turn left
    }
    
    else if(data == "brake") {
      brake(200);
    }
   }  
}


/*******************************************************************************************
 * Motor Constroller Functions                                                             *
 *******************************************************************************************/

void setSpeed(int speed) {
  if (speed < 0) {
    motor_1.setSpeed(speed + COMP_SPEED);
  }
  else {
    motor_1.setSpeed(speed - COMP_SPEED); 
  }
  motor_2.setSpeed(speed);
}

void brake(int brakePower) {
  motor_1.brake(brakePower);
  motor_2.brake(brakePower);
}

void turn(int spd, int in_place) {
  //turn in place
  if (in_place) {
    motor_1.setSpeed(spd);
    motor_2.setSpeed(-spd);    
  }

  //doing a slight turn 
  else {
    int currentSpeed = (motor_1.speed + motor_2.speed) / 2;
    
    motor_1.setSpeed(currentSpeed + spd);
    motor_2.setSpeed(currentSpeed - spd); 
  }
}
