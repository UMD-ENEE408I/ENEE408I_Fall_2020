/*
 * Bailey Fokin
 * 
 * ENEE408i
 * 
 * Code description:
 *    Robot, with two motors and 3 ping sensors will be able to 
 *    navigate a space with collition detection. 
 *    
 *    Rotbot will continue to move straight and will turn when ever
 *    there is a object within range of one of the 3 ping sensors
 *    
 *    Will turn right if there is something within range of the 
 *    left-most ping sensor
 *    
 *    Will turn left if there is something wihtin range of the 
 *    right-most ping sensor
 *    
 *    If something is within range of the middle sensor, the bot 
 *    will determine either to go right or left depending if there 
 *    is anything in the range of either of the sensors
 *    
 *    NOTES:
 *      MOTOR 2- right motor- is slower than the left
 *      (so the bot veers to the right)
 *        Will hopefully have this compensated for in the code
 *        
 *        the brake function may or may not work for single motor drivers
 */

/*******************************************************************************************
 * Include Statements                                                                      *
 *******************************************************************************************/
#include <stdio.h>
#include <VNH3SP30.h>


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
char buff [50];

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
//Main functions
void setup() {

  //Init motors
  motor_1.begin(M1_PWM, M1_INA, M1_INB, -1, -1);
  motor_2.begin(M2_PWM, M2_INB, M2_INA, -1, -1); 
  
  Serial.begin(9600);
}
void loop(){}

/*
void loop() {
  inches_r = get_distance(R_PING);
  inches_m = get_distance(M_PING);
  inches_l = get_distance(L_PING);

  if (inches_m < 5){
    setSpeed(-50);
    delay(500);

    turn(-100,1); //turn left
    delay(500);        
  }

  else if (inches_r < 5) {
    turn(-50,1); //turn left
    delay(500);    
  }
  
  else if (inches_l < 5){
    turn(50,1); //turn right
    delay(500);    
  }
  
  else {
    setSpeed(50);
  }
}
*/



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
/*
 * Sets the speed of both motors 
 * Used for moving the bot forward and backwards
 * range between 0 and 400
 */
void setSpeed(int speed) {
  motor_1.setSpeed(speed - COMP_SPEED);
  motor_2.setSpeed(speed);
}

/*
 * Brings the robot to a stop in a more natural way
 * range between 0 and 400
 */
void brake(int brakePower) {
  motor_1.brake(brakePower);
  motor_2.brake(brakePower);
}

/*
 * providing different speeds to the motors, you can slighty turn if need be
 * Parameter in_place determines if the robot will do a slight angle (0) or if
 * it should be turning in place (1)
 * spd > 0 (meaning its positve)  turn right
 * spd < 0 (meaning its negative) turn left
 */
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
