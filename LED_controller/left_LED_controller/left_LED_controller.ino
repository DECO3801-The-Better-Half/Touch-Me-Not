#include <CapacitiveSensor.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 11
#define LED_COUNT 120
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

const int lampPin = A5;
const int NUMBER_OF_SENSORS = 4;
CapacitiveSensor Sensor1 = CapacitiveSensor(2, 3);
CapacitiveSensor Sensor2 = CapacitiveSensor(4, 5);
CapacitiveSensor Sensor3 = CapacitiveSensor(6, 7);
CapacitiveSensor Sensor4 = CapacitiveSensor(8, 9);
CapacitiveSensor sensors[4] = {Sensor1, Sensor2, Sensor3, Sensor4};
int thresholds[] = {1000, 1000, 1000, 1000, 800};
//define variables for capactive sensor values
long values[4];

//define colour varibles using RGB values
uint32_t pink = strip.Color(255, 50, 70);
uint32_t purple = strip.Color(144, 0, 206);
uint32_t green = strip.Color(0,255, 0);
uint32_t dark_green = strip.Color(255,255, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t orange = strip.Color(255,60,5);
uint32_t yellow = strip.Color(255, 211, 30);
uint32_t none = strip.Color(0, 0, 0);

//define each object's LEDs that light up when it is tocuhed
// int plant1[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23};
// int plant2[] = {24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47};
// int flower[] = {48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71};
// int dragonfly [] = {72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95};
int lamp[] = {96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119};

int plant1[] = {0,1,2,3,16,17,18,19,32,33,34,35,48,49,50,51,64,65,66,67,80,81,82,83};
int plant2[] = {4,5,6,7,20,21,22,23,36,37,38,39,52,53,54,55,68,69,70,71,84,85,86,87};
int flower[] = {8,9,10,11,24,25,26,27,40,41,42,43,56,57,58,59,72,73,74,75,88,89,90,91};
int dragonfly [] = {12,13,14,15,28,29,30,31,44,45,46,47,60,61,62,63,76,77,78,79,92,93,94,95};

void setup() {
  Serial.begin(9600);
  strip.begin(); //always needed
  strip.show(); // 0 data => off.
  strip.setBrightness(200); // ~50%
  int n = strip.numPixels();
}

void loop() {

//read all sensor values
 for (int i = 0; i < NUMBER_OF_SENSORS; i = i + 1) {
      values[i] = sensors[i].capacitiveSensor(100);
      sensors[i].set_CS_Timeout_Millis(500);
      sensors[i].set_CS_AutocaL_Millis(10000);
    }
//plant 1 LED response
led_response(values[0], thresholds[0], plant1, green);

//plant 2 LED response
led_response(values[1], thresholds[1], plant2, dark_green);

//flower LED response
led_response(values[2], thresholds[2], flower, pink);

//dragonfly LED response
led_response(values[3], thresholds[3], dragonfly, orange);

//lamp LED response
led_response(analogRead(lampPin), thresholds[4], lamp, yellow);

//push this loops data to the strip to be shown
 strip.show();

int lampValue = analogRead(lampPin);

    Serial.print(lampValue);
    Serial.print(" ");
    Serial.print(values[0]);
    Serial.print(" ");
    Serial.print(values[1]);
    Serial.print(" ");
    Serial.print(values[2]);
    Serial.print(" ");
    Serial.print(values[3]);
    Serial.println();
}

void led_response(int sensor_value, int threshold, int leds[], uint32_t colour) {
  if (sensor_value > threshold || sensor_value == -2) {
    for (int i = 0; i < 24; i ++){
      strip.setPixelColor(leds[i], colour);
    }
    
  } else {
    for (int i= 0; i < 24; i++){
      strip.setPixelColor(leds[i], none);
    }
  }
}