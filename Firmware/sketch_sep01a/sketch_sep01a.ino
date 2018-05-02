#define LED_1 8
#define LED_2 11

#define MOTOR_A_1 5
#define MOTOR_A_2 10

#define MOTOR_B_1 6
#define MOTOR_B_2 9

#define PROG_LED 13

struct MotorData{
  int pin1;
  int pin2;
}motorLeft, motorRight;

bool led1On = false;
bool led2On = false;
bool progLedOn = false;

bool ledToggleOn = true;
long ledToggleTime = 1000;

void ledsSetup(){
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(PROG_LED, OUTPUT);

  ledsSet(false, false);
}

void ledSet(int pin, bool on){
  if(on){
    digitalWrite(pin, HIGH);  
  }else{
    digitalWrite(pin, LOW);  
  }
}

void ledsSet(bool firstOn, bool secondOn){
  ledSet(LED_1, firstOn);
  ledSet(LED_2, secondOn);

  led1On = firstOn;
  led2On = secondOn;
}

void ledsToggleFast(){
  ledToggleTime = 200;
}

void ledsToggleSlow(){
  ledToggleTime = 1000;
}

void ledsToggle(){
  static long lastToggle = 0;
  static bool firstOn = false;
  static bool secondOn = false;
  
  if(!ledToggleOn){
    return;
  }
  
  if((millis() - lastToggle) >= ledToggleTime){
    lastToggle = millis();

    firstOn = !firstOn;
    secondOn = !secondOn;
    progLedOn = !progLedOn;

    ledSet(LED_1, (firstOn && led1On));
    ledSet(LED_2, (secondOn && led2On));

    ledSet(PROG_LED, progLedOn);
  }
}

void motorSetup(MotorData motor){
  pinMode(motor.pin1, OUTPUT);
  pinMode(motor.pin2, OUTPUT);

  motorBrake(motor);
}

void motorForward(MotorData motor){
  digitalWrite(motor.pin1, HIGH);
  digitalWrite(motor.pin2, LOW);

  
}

void motorBackward(MotorData motor){
  digitalWrite(motor.pin1, LOW);
  digitalWrite(motor.pin2, HIGH);
}

void motorBrake(MotorData motor){
  digitalWrite(motor.pin1, LOW);
  digitalWrite(motor.pin2, LOW);
}

void robotForward(){
  motorForward(motorLeft);
  motorForward(motorRight);

  ledsToggleFast();
  ledsSet(true, true);
}

void robotBackward(){
  motorBackward(motorLeft);
  motorBackward(motorRight);

  ledsSet(false, false);
}

void robotLeft(){
  motorForward(motorLeft);
  motorBackward(motorRight);

  ledsToggleFast();
  ledsSet(true, false);
}

void robotRight(){
  motorBackward(motorLeft);
  motorForward(motorRight);

  ledsToggleFast();
  ledsSet(false, true);
}

void robotBrake(){
  motorBrake(motorLeft);
  motorBrake(motorRight);

  ledsToggleSlow();
  ledsSet(true, true);
}

void setup() {
  Serial.begin(9600);
  
  motorLeft.pin1 = MOTOR_A_1;
  motorLeft.pin2 = MOTOR_A_2;

  motorRight.pin1 = MOTOR_B_1;
  motorRight.pin2 = MOTOR_B_2;

  ledsSetup();

  motorSetup(motorLeft);
  motorSetup(motorRight);

  robotBrake();
}

void loop() {
  if(Serial.available() > 0){
    char direction = Serial.read();
    Serial.flush();
    
    switch(direction){
      case 'a':{
        robotLeft();
      }break;  

      case 'w':{
        robotForward();
      }break;

      case 's':{
        robotBackward();
      }break;

      case 'd':{
        robotRight();
      }break;

      default:{
        robotBrake();  
      }
    }
  }
  
  ledsToggle();
}


//Looking to add 
//motor stop when not pressed
//Mapping controls to a gamepad controller
