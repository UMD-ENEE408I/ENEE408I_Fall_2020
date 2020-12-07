#include "MotorControl.h"

//Class Constructor
MotorControl::MotorControl(byte INA_pin, byte PWM_pin, byte INB_pin)
{
      _INA_pin = INA_pin;
      _INB_pin = INB_pin;
      _PWM_pin = PWM_pin;

}

void MotorControl::setMode(){
  pinMode(_INA_pin, OUTPUT);
  pinMode(_INB_pin, OUTPUT);
  pinMode(_PWM_pin, OUTPUT);
}

void MotorControl::setPWM(int PWM_val){
  _PWM_val = PWM_val;
  analogWrite(_PWM_pin, _PWM_val);
}

void MotorControl::forward(){
  digitalWrite(_INA_pin, HIGH);
  digitalWrite(_INB_pin, LOW);    
  
}

void MotorControl::backward(){
  digitalWrite(_INA_pin, LOW);
  digitalWrite(_INB_pin, HIGH);    
  
}

void MotorControl::halt(){
   digitalWrite(_INA_pin, LOW);
   digitalWrite(_INB_pin, LOW);
}
