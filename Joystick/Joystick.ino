#define MIRROR 0
#define TAS 1
int mode = MIRROR;

#define BUTTONS 6
#define UP 0
#define DOWN 1
#define LEFT 2
#define RIGHT 3
#define FIREA 4
#define FIREB 5

int joystickPins[BUTTONS]={
  A0, //Up
  A1, //Down
  A2, //Left
  A3, //Right
  A4, //FireA
  A5  //FireB
};

int consolePins[BUTTONS]={
  8, //Up
  9, //Down
  10, //Left
  11, //Right
  12, //FireA
  13  //FireB
};

void setup() {
  //configure inputs and outputs
  for(int i = 0; i<BUTTONS; i++){
    pinMode(consolePins[i],OUTPUT);
    digitalWrite(consolePins[i],HIGH);
    pinMode(joystickPins[i],INPUT);
    digitalWrite(joystickPins[i],HIGH);
  }

  //check for TAS mode
  if(!digitalRead(joystickPins[FIREA]))
    mode = TAS;

  Serial.begin(115200);
}

void loop() {
  uint8_t input = 0;
  static uint8_t output = 0;
  
  //read input
  for(int i = 0; i<BUTTONS; i++)
    input |= digitalRead(joystickPins[i]) << i;
    
  //update changes over serial
  static uint8_t previousInput = input;
  if(input != previousInput){
    Serial.write(input);
    previousInput = input;
  }

  //mirror input to output unless in TAS mode
  if(mode != TAS)
    output = input;
  else if(Serial.available())
    output = Serial.read();
        
  //update output
  for(int i = 0; i< BUTTONS; i++)
    digitalWrite(consolePins[i], ((~output>>i) & 1));
}
