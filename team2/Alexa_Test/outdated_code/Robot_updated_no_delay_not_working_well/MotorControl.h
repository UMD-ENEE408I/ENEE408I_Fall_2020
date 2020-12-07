#ifndef MotorControl_h
#define MotorControl_h

#include "Arduino.h"

class MotorControl{
  public:
    byte _INA_pin;
    byte _PWM_pin;
    byte _INB_pin;
    int _PWM_val; // 0 - 255

  public:
    // Constructor
    MotorControl(byte INA_pin,byte PWM_pin, byte INB_pin);
    // methods
    void setMode();
    void setPWM(int PWM_val);
    void forward();
    void backward();
    void halt();
};
#endif
