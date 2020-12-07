/*
 * ENEE408i Fall 2020 Team 2 Amazon Alexa Test -- Yuchen Zhou
 */

#include "MotorControl.h"
#include "Arduino.h"



// command definiton
#define Forward 1
#define Backward 2
#define Left 3
#define Right 4
#define Stop 0

// Motor
  //left motor
  #define INA_1  2
  #define PWM_1  3
  #define INB_1  4
  //right motor
  #define INA_2  5
  #define PWM_2  6
  #define INB_2  7

//objects
  MotorControl Left_Motor(INA_1,PWM_1,INB_1);
  MotorControl Right_Motor(INA_2,PWM_2,INB_2);

String incoming_command;
byte incoming_command_dec;

void setup() {
  Left_Motor.setMode();
  Right_Motor.setMode();
  Serial.begin(9600);

}
  
void loop() {
    if (Serial.available() > 0){
        incoming_command = Serial.readStringUntil('\n');
        incoming_command_dec = convert_command();
        Serial.println("Y"+ incoming_command + "Y" + String(incoming_command_dec));
        command_exe(incoming_command_dec);
    }else{
      Serial.println("Halted");
      halt();
    }

}

// Command Convert
byte convert_command(){
  if(incoming_command == "Forward"){
    return Forward;
  }else if((incoming_command == "Backward")){
    return Backward;
  }else if((incoming_command == "Left")){
    return Left;
  }else if((incoming_command == "Right")){
    return Right;
  }else if((incoming_command == "Stop")){
    return Stop;
  }else{
    return 100;
  }
}

// Command execute
void command_exe(int command){
  switch(command){
    case Forward:
      forward(40,1000);
      break;
    case Backward:
      backward(40,1000);
      break;
    case Left:
      left(40,1000);
      break;
    case Right:
      right(40,1000);
      break;
    case Stop:
      halt();
      break;
    default:
      break;
  }
}

// moving functions
void forward(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.forward();
  Right_Motor.backward();
  delay(time_);
}

void backward(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.backward();
  Right_Motor.forward();
  delay(time_);
}

void left(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.backward();
  Right_Motor.backward();
  delay(time_);
}

void right(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.forward();
  Right_Motor.forward();
  delay(time_);
}

void halt(){
  Left_Motor.halt();
  Right_Motor.halt();
}
