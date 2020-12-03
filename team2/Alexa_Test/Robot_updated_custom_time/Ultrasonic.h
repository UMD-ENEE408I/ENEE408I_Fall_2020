#ifndef Ultrasonic_h
#define Ultrasonic_h

#include "Arduino.h"

class Ultrasonic_Sensor
{
  // Constructor
  public:
    Ultrasonic_Sensor(int echo, int trig);
    double getdistance_cm();
  private:
    int _echo;
    int _trig;
};
#endif
