/*
 * Bailey Fokin
 * 
 * ENEE408i
 * 
 * Code description:
 *      This code, using 3 ping sensors, will read sensor values and     
 *      will print the values (in inches) how far an object is from 
 *      a sensor.
 *      
 *      NOTE: this works for 3pin ping sensors If you have 4 ping sensors
 *      You will need to modify the code.
 *      I think the pinMode(pin, OUTPUT); should be the echo pin
 *      I think the pinMode(pin, INPUT);  should be the trig pin
 */

#include <stdio.h>


int inches_r, inches_m, inches_l;
char buff [50];
// this constant won't change. It's the pin number of the sensor's output:
const int right_ping = 10;
const int mid_ping = 11;
const int left_ping = 12;

void setup() {
  
  // initialize serial communication:
  Serial.begin(9600);
}

void loop() {
  
  inches_r = get_distance(right_ping);
  inches_m = get_distance(mid_ping);
  inches_l = get_distance(left_ping);

  sprintf(buff, "%3d : %3d : %3d\n", inches_r, inches_m, inches_l);
  Serial.print(buff);


  delay(100);
}

long microsecondsToInches(long microseconds) {
  return microseconds / 74 / 2;
}

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
    inches = microsecondsToInches(duration);  
  return inches;
}
