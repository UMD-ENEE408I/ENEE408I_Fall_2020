/*
 * Bailey Fokin
 * 
 * ENEE408i
 * 
 * Code description:        
 *    This code should be used to test individual motor drivers
 */

const int INA = 2;
const int INB = 3;
const int PWM_PIN = 4;


void setup(){

pinMode(INA, OUTPUT);
pinMode(INB, OUTPUT);
pinMode(PWM_PIN, OUTPUT);
Serial.begin(9600);

}

void loop(){
  setM1spd(-10);
   

}

void setM1spd(int spd)
{
  unsigned char reverse = 0;

  analogWrite(PWM_PIN, spd * 51 / 80);

  if (spd < 0) {
    spd = -spd;  // Make spd a positive quantity
    reverse = 1;  // Preserve the direction
  }
  
  if (spd > 400)  spd = 400;

  if (spd == 0) {
    digitalWrite(INA,LOW);   // Make the motor coast no
    digitalWrite(INB,LOW);   // matter which direction it is spinning.
  }
  
  else if (reverse) {
    digitalWrite(INA,LOW);
    digitalWrite(INB,HIGH);
  }
  
  else {
    digitalWrite(INA,HIGH);
    digitalWrite(INB,LOW);
  }
}
