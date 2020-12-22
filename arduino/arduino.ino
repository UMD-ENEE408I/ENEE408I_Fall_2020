int trig_R = 2;    // TRIG pin
int trig_M = 4;
int trig_L = 6;

int echo_R = 3;    // ECHO pin
int echo_M = 5; 
int echo_L = 7; 

int RVS_L = 13;   // Left motor driver
int FWD_L = 12;   // B=RVS, A=FWD
int PWM_L = 10;

int RVS_R = 11;    // Right motor driver
int FWD_R = 8;
int PWM_R = 9;

int wall=50;

float dist_L, dist_M, dist_R;

void getSensorL(){
  digitalWrite(trig_L, HIGH);
  delayMicroseconds(60);
  digitalWrite(trig_L, LOW);
  dist_L = 0.017* pulseIn(echo_L, (HIGH));
}

void getSensorM(){
  digitalWrite(trig_M, HIGH);
  delayMicroseconds(60);
  digitalWrite(trig_M, LOW);
  dist_M = 0.017* pulseIn(echo_M, HIGH);
}

void getSensorR(){
  digitalWrite(trig_R, HIGH);
  delayMicroseconds(60);
  digitalWrite(trig_R, LOW);
  dist_R = 0.017* pulseIn(echo_R, HIGH);
}

void getAllSensors(){
  getSensorL();
  getSensorM();
  getSensorR();
}

void printSensorL(){
  Serial.print("Left sensor distance: ");
  Serial.print(dist_L);
  Serial.println(" cm.");
}

void printSensorM(){
  Serial.print("Middle sensor distance: ");
  Serial.print(dist_M);
  Serial.println(" cm.");
}

void printSensorR(){
  Serial.print("Right sensor distance: ");
  Serial.print(dist_R);
  Serial.println(" cm.");
}

void printAllSensors(){
  printSensorL();
  printSensorM();
  printSensorR();
}

void leftVolt(int val){
  analogWrite(PWM_L,val);
}

void rightVolt(int val){
  analogWrite(PWM_R,val);
}

void leftDir(char d){
  if(d=='F'){
    digitalWrite(RVS_L,LOW);
    digitalWrite(FWD_L,HIGH);
  }
  else if(d=='R'){
    digitalWrite(FWD_L,LOW);
    digitalWrite(RVS_L,HIGH);
  }
  else{
    digitalWrite(FWD_L,LOW);
    digitalWrite(RVS_L,LOW);
  }
}

void rightDir(char d){
  if(d=='F'){
    digitalWrite(RVS_R,LOW);
    digitalWrite(FWD_R,HIGH);
  }
  else if(d=='R'){
    digitalWrite(FWD_R,LOW);
    digitalWrite(RVS_R,HIGH);
  }
  else{
    digitalWrite(FWD_R,LOW);
    digitalWrite(RVS_R,LOW);
  }
}

void goForward(){
  rightDir('F');
  leftDir('F');
}

void goBackward(){
  rightDir('R');
  leftDir('R');
}

void stopAll(){
  leftDir('S');
  rightDir('S');
}

void turnLeft(){
  leftDir('R');
  rightDir('F');
  delay(500);
  stopAll();
}

void turnRight(){
  leftDir('F');
  rightDir('R');
  delay(500);
  stopAll();
}

void turnAround(){
  turnRight();
  turnRight();
}

bool checkWall(){
  if(dist_L<wall || dist_M<wall || dist_R<wall){
    return true;
  }
  return false;
}


void chooseDir(){
  if(dist_L>dist_R){
    turnLeft();
  }
  else{
    turnRight();
  }
}

void dancing(){
  int turns = 1;
  
  while(!Serial.available()){
    getAllSensors();
    printAllSensors();
    if(checkWall()){
      chooseDir();
    }
    goForward();
    delay(300);
    stopAll();
    delay(300);
    goBackward();
    delay(300);
    while(turns <= 3 & !Serial.available()){
      turnLeft();
      delay(100);
      turnRight();
      delay(100);
      turns = turns + 1;
    }
  turns = 1;
  }
}

void wander(){
  while(!Serial.available()){
    getAllSensors();
    //printAllSensors();
    goForward();
    if(checkWall()){
      stopAll();
      delay(300);
      goBackward();
      delay(300);
      chooseDir();
    }
  }
}

void setup() {
  Serial.begin (9600);

  pinMode(trig_L, OUTPUT);
  pinMode(trig_M, OUTPUT);
  pinMode(trig_R, OUTPUT);

  pinMode(echo_L, INPUT);
  pinMode(echo_M, INPUT);
  pinMode(echo_R, INPUT);
  
  pinMode(RVS_L, OUTPUT);
  pinMode(FWD_L, OUTPUT);
  pinMode(PWM_L, OUTPUT);

  pinMode(RVS_R, OUTPUT);
  pinMode(FWD_R, OUTPUT);
  pinMode(PWM_R, OUTPUT);

  leftVolt(50);
  rightVolt(50);
}

void loop() {
  getAllSensors();
  //printAllSensors();
  //if(checkWall()){
    //chooseDir();
  if (Serial.available()) {
    int incoming_serial = Serial.read();
    switch(incoming_serial){
      case 'f':
        goForward();
        break;
      case 'b':
        goBackward();
        break;
      case 'l':
        turnLeft();
        break;
      case 'r':
        turnRight();
        break;
      case 's':
        stopAll();
        break;
      case 'w':
        wander();
        break;
      case 'd':
        dancing();
        break;
      default:
        break;
    }
  }
}
