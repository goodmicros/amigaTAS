~~~~
capture.py devfile            : record a series of events
playback.py devfile           : playback previously captured series of events
remoteServer.py devfile       : listen for inputs from remote client
remoteClient.py devfile server: send inputs from joystick to remote server
~~~~

intput pinout, output is mirrored
~~~~
\ 1 2 3 4 5 /
 \ 6 7 8 9 /
~~~~

pin mapping

| Pin | Name  | Input | Output |
| --- | ----- | ----- | ------ |
| 1   | UP    | A0    | 8      |
| 2   | DOWN  | A1    | 9      |
| 3   | LEFT  | A2    | 10     |
| 4   | RIGHT | A3    | 11     |
| 5   | -     | -     | -      |
| 6   | FIREA | A4    | 12     |
| 7   | -     | +5V   | +5V    |
| 8   | -     | GND   | GND    |
| 9   | FIREB | A5    | 13     |

requires https://github.com/MHeironimus/ArduinoJoystickLibrary
