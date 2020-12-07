#include "Ultrasonic.h"

//Class Constructor
Ultrasonic_Sensor::Ultrasonic_Sensor(int echo, int trig)
{
  _echo = echo;
  _trig = trig;
}

double Ultrasonic_Sensor::getdistance_cm()
{
  long duration;
  double distance;

  pinMode(_trig, OUTPUT);
  pinMode(_echo, INPUT);

  // Clear the _trig by setting it LOW:
  digitalWrite(_trig, LOW);
  delayMicroseconds(5);
  // Trigger the sensor by setting the _trig high for 10 microseconds:
  digitalWrite(_trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(_trig, LOW);
  // Read the echoPin, pulseIn() returns the duration (length of the pulse) in microseconds:
  duration = pulseIn(_echo, HIGH);
  // Calculate the distance:
  distance = duration * 0.034 / 2;

  return distance;
}
