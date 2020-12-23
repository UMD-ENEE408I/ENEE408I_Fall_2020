#ifndef MOTORS_H
#define MOTORS_H    

/*******************************************************************************************
 * Motor Constroller Functions                                                             *
 *******************************************************************************************/
/*
 * Sets the speed of both motors 
 * Used for moving the bot forward and backwards
 * range between 0 and 400
 */
void setSpeed(int speed);

/*
 * Brings the robot to a stop in a more natural way
 * range between 0 and 400
 */
void brake(int brakePower);

/*
 * providing different speeds to the motors, you can slighty turn if need be
 * Parameter in_place determines if the robot will do a slight angle (0) or if
 * it should be turning in place (1)
 * spd > 0 (meaning its positve)  turn right
 * spd < 0 (meaning its negative) turn left
 */
void turn(int spd, int in_place);



#endif // MOTORS_H  
