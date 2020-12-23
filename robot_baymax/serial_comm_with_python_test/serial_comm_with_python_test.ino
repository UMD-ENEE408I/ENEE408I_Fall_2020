/*
 * Bailey Fokin
 * 
 * ENEE408i
 * 
 * Code description:       
 *    Serial Communications Test with the base cpu
 *    (pi4/NX)
 *    depending on what the input is in the serial
 *    the robot will move 
 *    
 *    Command codes
 *    0   Halts the robot
 *    1   Wander with ping sensor
 *    2   Facial recognition (NOT USED FOR ARDUINO)
 *    3   Dance
 *    4   Forward movement
 */

 /*
  * TODO list
  * 
  * create interupt for the wander function so then you can leave the wander function
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

//ping sensors
#define R_PING 10
#define M_PING 11
#define L_PING 12

/*******************************************************************************************
 * Global Variables                                                                        *
 *******************************************************************************************/
int inches_r, inches_m, inches_l;
volatile int wander_state = LOW;

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

//Ping Functions
long microseconds_to_inches(long microseconds);
int get_distance(int pin);

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

  //Start serial communications
  Serial.begin(9600);
}

void loop() {
  
   if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);

    switch(data.toInt()) {
      case 0:
        brake(200);
        break;

      case 1:
        wander_state = HIGH;
        wander();
        break;

      case 3:
        for(int j = 0; j < 3; j++) {
          turn(100, 1);
          delay(1000);
          brake(200);
          for(int k = 0; k < 4; k++){
            turn(-100, 1);
            delay(400); 
            turn(100, 1);
            delay(400); 
          } 
        }
        brake(200);
        break;

      case 4:
        setSpeed(50);
        break;

       case 5:
        delay(1000);
        turn(200, 1);
        delay(300);
        brake(200);
        break;
      
    }
   }  
}

/*******************************************************************************************
 * Ping Sensor Functions                                                                   *
 *******************************************************************************************/
/*74 microseconds ~= 1 inch for the ping sensor's out to in signal
 * returns the distance from the ping sensor to the obj in inches
 * Divided by 2 since the total time represents the out and in signal time
 * Used in get_distance
 */
long microseconds_to_inches(long microseconds) {
  return microseconds / 74 / 2;
}

/*
 * Given a pin for one of the ping sensors, get_distance
 * sends a pulse out then in for the given ping sensor
 * returns the distance between the sensor and an obj, in inches 
 */
  //code snippet used to see the values of the sensors
  //sprintf(buff, "%3d : %3d : %3d\n", inches_r, inches_m, inches_l);
  //Serial.print(buff);
int get_distance(int pin) {
    long duration;
    int inches;
  
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
    delayMicroseconds(2);
    digitalWrite(pin, HIGH);
    delayMicroseconds(5);
    digitalWrite(pin, LOW);
  
    pinMode(pin, INPUT);
    duration = pulseIn(pin, HIGH);
  
    // convert the time into a distance
    inches = microseconds_to_inches(duration);  
  return inches;
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

void wander(void) {
  while(wander_state == HIGH) {
    inches_r = get_distance(R_PING);
    inches_m = get_distance(M_PING);
    inches_l = get_distance(L_PING);

    if (Serial.available()) {
      String data = Serial.readStringUntil('\n');
      Serial.print("You sent me: ");
      Serial.println(data);
      
      if(data.toInt() != 1){
        wander_state = LOW;
      }
    } 
  
    if (inches_m < 7){
      setSpeed(-50);
      delay(500);
  
      turn(-100,1); //turn left
      delay(500);        
    }
  
    else if (inches_r < 7) {
      turn(-50,1); //turn left
      delay(500);    
    }
    
    else if (inches_l < 7){
      turn(50,1); //turn right
      delay(500);    
    }
    
    else {
      setSpeed(50);
    }
  }
  brake(200);
}
