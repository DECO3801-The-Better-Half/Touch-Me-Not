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
int thresholds[] = {200, 200, 200, 200, 800};
//define variables for capactive sensor values
long values[4];

//define colour varibles using RGB values
uint32_t pink = strip.Color(242, 90, 186);
uint32_t purple = strip.Color(144, 50, 206);
uint32_t green = strip.Color(0,255, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t yellow = strip.Color(255, 211, 30);
uint32_t none = strip.Color(0, 0, 0);

//define each object's LEDs that light up when it is tocuhed
int plant1[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23};
int plant2[] = {24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47};
int flower[] = {48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71};
int water [] = {72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95};
int lamp[] = {96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119};


void setup() {
Serial.begin(9600);
strip.begin(); //always needed
strip.show(); // 0 data => off.
strip.setBrightness(255); // 100%
int n = strip.numPixels();
}

void loop() {

 for (int i = 0; i < NUMBER_OF_SENSORS; i = i + 1) {
      values[i] = sensors[i].capacitiveSensor(20);
      sensors[i].set_CS_Timeout_Millis(20);
    }
//If plant/sensor 1 is touched light up its 20 specified LEDs in pink
// if (values[0] > 200) {
//   for (int i = 0; i < 20; i ++){
//     strip.setPixelColor(plant1[i], pink);
//   }
  
// } else {
//   for (int i= 0; i < 20 ; i++){
//     strip.setPixelColor(plant1[i], none);
//   }
// }
led_response(values[0], thresholds[0], plant1, pink);
//If plant/sensor 2 is touched light up its 20 specified LEDs in purple
// if (values[1] > 200) {
//   for (int i = 0; i < 20; i ++){
//     strip.setPixelColor(plant2[i], purple);
//   }

// } else {
//   for (int i= 0; i < 20; i++){
//     strip.setPixelColor(plant2[i], none);
//   }
// }

led_response(values[1], thresholds[1], plant2, purple);
led_response(values[2], thresholds[2], plant2, green);
led_response(values[3], thresholds[3], plant2, blue);
led_response(analogRead(lampPin), thresholds[4], plant2, yellow);
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

    delay(40);
}

void led_response(int sensor_value, int threshold, int leds[], uint32_t colour) {
  if (sensor_value > threshold) {
    for (int i = 0; i < 24; i ++){
      strip.setPixelColor(leds[i], colour);
    }
    
  } else {
    for (int i= 0; i < 24; i++){
      strip.setPixelColor(leds[i], none);
    }
  }
}