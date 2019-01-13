/* device mode configuration */
#define TAS 1
#define USBJOYSTICK 2
int mode = 0;

/* USB Joystick configuration */
#include "Joystick.h"
Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID,JOYSTICK_TYPE_JOYSTICK,
  2, 0,                  // Button Count, Hat Switch Count
  true, true, false,     // X and Y, but no Z Axis
  false, false, false,   // No Rx, Ry, or Rz
  false, false,          // No rudder or throttle
  false, false, false);  // No accelerator, brake, or steering

/* input/output name configuration */
#define BUTTONS 6
#define UP 0
#define DOWN 1
#define LEFT 2
#define RIGHT 3
#define FIREA 4
#define FIREB 5

/* input configuration */
int joystickPins[BUTTONS]={
  A0, //Up
  A1, //Down
  A2, //Left
  A3, //Right
  A4, //FireA
  A5  //FireB
};

/* output configuration */
int consolePins[BUTTONS]={
  8, //Up
  9, //Down
  10, //Left
  11, //Right
  12, //FireA
  13  //FireB
};

void setup() {
  //setup input and output
  for(int i = 0; i<BUTTONS; i++){
    pinMode(consolePins[i],OUTPUT);
    digitalWrite(consolePins[i],HIGH);
    pinMode(joystickPins[i],INPUT);
    digitalWrite(joystickPins[i],HIGH);
  }

  //check for TAS mode
  if(!digitalRead(joystickPins[FIREA]))
    mode = TAS;

  //check if usb joystick is needed
  if(!digitalRead(joystickPins[FIREB])){
    mode |= USBJOYSTICK;
    Joystick.setXAxisRange(-1,1);
    Joystick.setYAxisRange(-1,1);
    Joystick.begin(false);
  }

  //open serial
  Serial.begin(115200);
}

void loop() {
  //variables for holding input and output state
  uint8_t input = 0;
  static uint8_t output = 0;
  
  //read input
  for(int i = 0; i<BUTTONS; i++)
    input |= digitalRead(joystickPins[i]) << i;
    
  //send input state over serial if it has changed
  static uint8_t previousInput = input;
  if(input != previousInput){
    Serial.write(input);
    previousInput = input;
  }

  //try to read input from serial if in TAS mode
  if(mode & TAS && Serial.available())
    output = Serial.read();
  else
    output = input;
        
  //update output
  for(int i = 0; i< BUTTONS; i++)
    digitalWrite(consolePins[i], ((~output>>i) & 1));

  //update output for joystick if needed
  if(mode & USBJOYSTICK){
    Joystick.setXAxis(-1*((~output>>LEFT)&1)+1*((~output>>RIGHT)&1));
    Joystick.setYAxis(-1*((~output>>UP)&1)+1*((~output>>DOWN)&1));
    Joystick.setButton(0,(~output>>FIREA)&1);
    Joystick.setButton(1,(~output>>FIREB)&1);
    Joystick.sendState();
  }
}
