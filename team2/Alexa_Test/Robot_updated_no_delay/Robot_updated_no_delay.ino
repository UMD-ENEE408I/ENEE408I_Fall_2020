/*
 * ENEE408i Fall 2020 Team 2 Robot Combined -- Yuchen Zhou
 */

#include "MotorControl.h"
#include "Arduino.h"
#include "Ultrasonic.h"

// Pins Assignment
  // Ultrasonic Sensor
  #define trigPin_left 14
  #define echoPin_left 15
  #define trigPin_middle 16
  #define echoPin_middle 17
  #define trigPin_right 18
  #define echoPin_right 19

// command definiton
 #define Forward 1
 #define Backward 2 
 #define Left 3
 #define Right 4
 #define SELF_DRI 5
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
  Ultrasonic_Sensor Ultrasonic_Sensor_left(echoPin_left,trigPin_left);
  Ultrasonic_Sensor Ultrasonic_Sensor_middle(echoPin_middle,trigPin_middle);
  Ultrasonic_Sensor Ultrasonic_Sensor_right(echoPin_right,trigPin_right);

const double STOP_DISTANCE_FRONT = 15; // cm
const double STOP_DISTANCE_SIDE   = 15; // cm
  
//measure
  double left_dis;
  double middle_dis;
  double right_dis;

  String origin_incoming_command;
  byte incoming_command_dec;

  char incoming_command[20];
  char duration[20];
  int duration_int = 1000; // default value

  unsigned long s_time;
  unsigned long e_time1;
  unsigned long e_time2;
  unsigned long e_time3;
  unsigned long e_time4;
  unsigned long e_time5;

void setup() {
  Left_Motor.setMode();
  Right_Motor.setMode();
  Serial.begin(9600);

}
  
void loop() {
    if (Serial.available() > 0){
        s_time = millis();
        origin_incoming_command = Serial.readStringUntil('\n');
        e_time1 = millis();
        process_command();
        e_time2 = millis();
        incoming_command_dec = convert_command();
        e_time3 = millis();
        command_exe(incoming_command_dec);
        e_time4 = millis();
        Serial.println(String(e_time1 - s_time) + " " + String(e_time2 - s_time) + " " + String(e_time3 - s_time) + " " + String(e_time4 - s_time));
          //Serial.println("Dec" + String(incoming_command_dec));
        /*if(safe_check()== 1){
          //Serial.println("safe to execute command");
          command_exe(incoming_command_dec);
        }else{
          //Serial.println("trying to find a safe position...");
          obstacle_avoidance_handlder_until_safe();
        }*/
        
    }/*else{
    }
      halt();
    }*/

}

// process command
void process_command(){
   char buf[50];
   origin_incoming_command.toCharArray(buf, sizeof(buf));
   if(buf[0] == '1'){ // if the command specifies a duration 
      sscanf(buf+2, "%s %s", incoming_command,duration);
      duration_int = int(atof(duration)*1000.0);
      //Serial.println("Arduino Process...");
   }else{
      sscanf(buf, "%s", incoming_command);
      //Serial.println("Life is good...");
   }
}

// safe check()
int safe_check(){
  get_all_distance();
  if ((left_dis >= STOP_DISTANCE_SIDE) &&  (right_dis >= STOP_DISTANCE_SIDE) && (middle_dis >= STOP_DISTANCE_FRONT)) return 1;
  else return 0;
}

// Command Convert
byte convert_command(){
  if(String(incoming_command) == "Forward"){
    //Serial.println("Executing...Forward");
    return Forward;
  }else if((String(incoming_command) == "Backward")){
    //Serial.println("Executing...Backward");
    return Backward;
  }else if((String(incoming_command)== "Left")){
    //Serial.println("Executing...Left");
    return Left;
  }else if((String(incoming_command) == "Right")){
    //Serial.println("Executing...Right");
    return Right;
  }else if((String(incoming_command) == "Stop")){
    //Serial.println("Executing...Stop");
    return Stop;
  }else if((String(incoming_command) == "Self_Driving")){
    return SELF_DRI; 
  }else{
    return 100;
  }
}

// Command execute
void command_exe(int command){
  //Serial.println("Executing..." + String(command));
  switch(command){
    case Forward:
      forward(60, duration_int);
      break;
    case Backward:
      backward(60, duration_int);
      break;
    case Left:
      left(60, duration_int);
      break;
    case Right:
      right(60, duration_int);
      break;
    case Stop:
      halt();
      break;
    case SELF_DRI:
      self_driving();
      break;
    default:
      halt();
      break;
  }
}


void self_driving(){
    do{
      get_all_distance();
        // keep moving forward when no obstacle is detected
      if((left_dis >= STOP_DISTANCE_SIDE) &&  (right_dis >= STOP_DISTANCE_SIDE) && (middle_dis >= STOP_DISTANCE_FRONT)){
        forward(60,10);       // moving forward for 10 ms  
        //Serial.println("forward");
        get_all_distance();   // detect all distance
      }else{
        halt();
        //Serial.println("Obstacle");
        obstacle_avoidance_handler();
      }
  }while(!Serial.available());
}


void obstacle_avoidance_handler(){
  if(middle_dis < STOP_DISTANCE_FRONT){
    if(left_dis >= STOP_DISTANCE_SIDE && right_dis >= STOP_DISTANCE_SIDE){  // flat wall
      if(left_dis >= right_dis){
        backward(60,1000);
        right(60,500);
      }else{
        backward(60,1000);
        left(60,500);
      }
    }else if(left_dis >=  STOP_DISTANCE_SIDE){
      backward(60,1000);
      left(60,500);
    }else if(right_dis >= STOP_DISTANCE_SIDE){
      backward(60,1000);
      right(60,500);
    }else{
      backward(60,1000);
      right(60,1000);
    }
  }

  else if(left_dis < STOP_DISTANCE_SIDE){
      right(60,200);
  }else{
      left(60,200);
  }
}


void obstacle_avoidance_handlder_until_safe(){
  do{
      if(middle_dis < STOP_DISTANCE_FRONT){
        if(left_dis >= STOP_DISTANCE_SIDE && right_dis >= STOP_DISTANCE_SIDE){  // flat wall
          if(left_dis >= right_dis){
            backward(60,1000);
            right(60,500);
          }else{
            backward(60,1000);
            left(60,500);
          }
        }else if(left_dis >=  STOP_DISTANCE_SIDE){
          backward(60,1000);
          left(60,500);
        }else if(right_dis >= STOP_DISTANCE_SIDE){
          backward(60,1000);
          right(60,500);
        }else{
          backward(60,1000);
          right(60,1000);
        }
      }
      else if(left_dis < STOP_DISTANCE_SIDE){
          right(60,200);
      }else{
          left(60,200);
      }
  }while(!safe_check());
}

void get_all_distance(){
  left_dis = Ultrasonic_Sensor_left.getdistance_cm();
  middle_dis = Ultrasonic_Sensor_middle.getdistance_cm();
  right_dis = Ultrasonic_Sensor_right.getdistance_cm();
}



// moving functions
void forward(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.forward();
  Right_Motor.backward();
  //delay(time_);
}

void backward(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.backward();
  Right_Motor.forward();
  //delay(time_);
}

void left(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.backward();
  Right_Motor.backward();
  //delay(time_);
}

void right(int PWM_speed, int time_){
  Left_Motor.setPWM(PWM_speed);
  Right_Motor.setPWM(PWM_speed+5);
  Left_Motor.forward();
  Right_Motor.forward();
  //delay(time_);
}

void halt(){
  Left_Motor.halt();
  Right_Motor.halt();
}
