#ifndef PINS_H
#define PINS_H
#define ALARM_PIN          -1


/****************************************************************************************
* Arduino Mega pin assignment
*
****************************************************************************************/
  
  //////////////////FIX THIS//////////////
  #ifndef __AVR_ATmega1280__
   #ifndef __AVR_ATmega2560__
   #error Oops!  Make sure you have 'Arduino Mega' selected from the 'Tools -> Boards' menu.
   #endif
  #endif
  
  
  #define X_STEP_PIN         54
  #define X_DIR_PIN          55
  #define X_ENABLE_PIN       38
  #define X_MIN_PIN           3
  #define X_MAX_PIN          -1   //2 //Max endstops default to disabled "-1", set to commented value to enable.
  
  #define Y_STEP_PIN         60
  #define Y_DIR_PIN          61
  #define Y_ENABLE_PIN       56
  #define Y_MIN_PIN          14
  #define Y_MAX_PIN          -1   //15
  
  #define Z_STEP_PIN         46
  #define Z_DIR_PIN          48
  #define Z_ENABLE_PIN       62
  #define Z_MIN_PIN          18 //18
  #define Z_MAX_PIN          -1 //19
  
  #define E_STEP_PIN         26
  #define E_DIR_PIN          28
  #define E_ENABLE_PIN       24
  
  #define E_1_STEP_PIN         36
  #define E_1_DIR_PIN          34
  #define E_1_ENABLE_PIN       30
  
  #define SDPOWER            -1
  #define SDSS               -1
  #define LED_PIN            13
  #define FAN_PIN            9
  #define PS_ON_PIN          12
  #define KILL_PIN           -1
  #define ALARM_PIN          -1
  
  #define HEATER_0_PIN       10
  #define HEATER_1_PIN       8
  #define TEMP_0_PIN         13   // ANALOG NUMBERING
  #define TEMP_1_PIN         14   // ANALOG NUMBERING
  #define TEMP_2_PIN         15   // ANALOG NUMBERING
  
  #define LED_BACKLIGHT_PIN       10
  #define LED_BACKLIGHT2_PIN      8
  

//List of pins which to ignore when asked to change by gcode, 0 and 1 are RX and TX, do not mess with those!
const int sensitive_pins[] = {0, 1, X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN, X_MIN_PIN, X_MAX_PIN, Y_STEP_PIN, Y_DIR_PIN, Y_ENABLE_PIN, Y_MIN_PIN, Y_MAX_PIN, Z_STEP_PIN, Z_DIR_PIN, Z_ENABLE_PIN, Z_MIN_PIN, Z_MAX_PIN, E_STEP_PIN, E_DIR_PIN, E_ENABLE_PIN, LED_PIN, PS_ON_PIN, HEATER_0_PIN, HEATER_1_PIN, FAN_PIN, TEMP_0_PIN, TEMP_1_PIN};

#endif


