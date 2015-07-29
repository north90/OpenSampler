#ifndef CONFIGURATION_H
#define CONFIGURATION_H

// added code for OpenSampler
long timeout_time_for_fan_pin=60;

//// Calibration variables
// X, Y, Z, E steps per unit - TR8-8mm per rotation, 200steps per rotation: 
// 0.04mm per full step= 25 steps per mm
// at 1/16 microsteps: 25*8=200 usteps per mm IN THEORY.. 
//in practice the X-Axis TR8 aint quite 8
// so 400mm turns out to be 403 (1% off!) So 198.5 steps per mm
//float axis_steps_per_unit[] = {80, 80, 400, 200}; 
float axis_steps_per_unit[] = {160, 160, 800, 200}; 

//// Endstop Settings
#define ENDSTOPPULLUPS // Comment this out (using // at the start of the line) to disable the endstop pullup resistors
// The pullups are needed if you directly connect a mechanical endswitch between the signal and ground pins.
//If your axes are only moving in one direction, make sure the endstops are connected properly.
//If your axes move in one direction ONLY when the endstops are triggered, set [XYZ]_ENDSTOP_INVERT to true here:
const bool X_ENDSTOP_INVERT = false;
const bool Y_ENDSTOP_INVERT = false;
const bool Z_ENDSTOP_INVERT = false;

// This determines the communication speed of the printer
#define BAUDRATE 115200

//// ADVANCED SETTINGS - to tweak parameters

// For Inverting Stepper Enable Pins (Active Low) use 0, Non Inverting (Active High) use 1
#define X_ENABLE_ON 0
#define Y_ENABLE_ON 0
#define Z_ENABLE_ON 0
#define E_ENABLE_ON 0

// Disables axis when it's not being used.
const bool DISABLE_X = false;
const bool DISABLE_Y = false;
const bool DISABLE_Z = false;
const bool DISABLE_E = false;

// Inverting axis direction
const bool INVERT_X_DIR = false;
const bool INVERT_Y_DIR = false;
const bool INVERT_Z_DIR = false;
const bool INVERT_E_DIR = false;

//// ENDSTOP SETTINGS:
// Sets direction of endstops when homing; 1=MAX, -1=MIN
#define X_HOME_DIR -1
#define Y_HOME_DIR -1
#define Z_HOME_DIR -1

const bool min_software_endstops = false; //If true, axis won't move to coordinates less than zero.
const bool max_software_endstops = true;  //If true, axis won't move to coordinates greater than the defined lengths below.
const int X_MAX_LENGTH = 322;
const int Y_MAX_LENGTH = 140;
const int Z_MAX_LENGTH = 100;

//// MOVEMENT SETTINGS
const int NUM_AXIS = 4; // The axis order in all axis related arrays is X, Y, Z, E
float max_feedrate[] = {8000, 8000, 3000, 3000};
float homing_feedrate[] = {3000,3000,2000};
bool axis_relative_modes[] = {false, false, false, false};

// Min step delay in microseconds. If you are experiencing missing steps, try to raise the delay microseconds, but be aware this
// If you enable this, make sure STEP_DELAY_RATIO is disabled.
//#define STEP_DELAY_MICROS 1

// Step delay over interval ratio. If you are still experiencing missing steps, try to uncomment the following line, but be aware this
// If you enable this, make sure STEP_DELAY_MICROS is disabled. (except for Gen6: both need to be enabled.)
//#define STEP_DELAY_RATIO 0.25

// Comment this to disable ramp acceleration
#define RAMP_ACCELERATION

//// Acceleration settings
#ifdef RAMP_ACCELERATION
// X, Y, Z, E maximum start speed for accelerated moves. E default values are good for skeinforge 40+, for older versions raise them a lot.
float max_start_speed_units_per_second[] = {1.0,1.0,1.0,1.0};
long max_acceleration_units_per_sq_second[] = {500,500,150,150}; // X, Y, Z and E max acceleration in mm/s^2 for printing moves or retracts
long max_travel_acceleration_units_per_sq_second[] = {500,500,150,150}; // X, Y, Z max acceleration in mm/s^2 for travel moves
#endif

// Machine UUID
// This may be useful if you have multiple machines and wish to identify them by using the M115 command. 
// By default we set it to zeros.
char uuid[] = "00000000-0000-0000-0000-000000000000";

// Uncomment the following line to enable debugging. You can better control debugging below the following line
//#define DEBUG
#ifdef DEBUG
  //#define DEBUG_PREPARE_MOVE //Enable this to debug prepare_move() function
  //#define DEBUG_BRESENHAM //Enable this to debug the Bresenham algorithm
  //#define DEBUG_RAMP_ACCELERATION //Enable this to debug all constant acceleration info
  //#define DEBUG_MOVE_TIME //Enable this to time each move and print the result
#endif

#endif
