/* Adapted from XOPA ART https://www.dropbox.com/s/yl2rqcrgcoy2iwq/ArduinoPlantTouch.pdf?dl=0 */

#include <CapacitiveSensor.h>
#include <Adafruit_NeoPixel.h>
#define LED_PIN 5
#define LED_COUNT 120
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
CapacitiveSensor Sensor1 = CapacitiveSensor(9, 6);
CapacitiveSensor Sensor2 = CapacitiveSensor(3, 10);

//define variables for capactive sensor values
long val1;
long val2;

//define colour varibles using RGB values
uint32_t green = strip.Color(0,255, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t none = strip.Color(0, 0, 0);

//define each object's LEDs that light up when it is tocuhed
int plant1[] = {1,2,5,6,9,10,13,14,17,18,22,23,26,27,30,31,34,35,38,39};
int plant2[] = {3,4,7,8,11,12,15,16,19,20,24,25,28,29,32,33,36,37,40};

void setup() {
Serial.begin(9600);
strip.begin(); //always needed
strip.show(); // 0 data => off.
strip.setBrightness(50); // ~20% (max = 255)
int n = strip.numPixels();
}

void loop() {

val1 = Sensor1.capacitiveSensor(30);
val2 = Sensor2.capacitiveSensor(30);

Serial.print(val1);
Serial.println();
Serial.print(val2);
Serial.println();

//If plant/sensor 1 is touched light up its 20 specified LEDs in green
if (val1 > 500) {
  for (int i = 0; i < 20; i ++){
    strip.setPixelColor(plant1[i], green);
  }
  
} else {
  for (int i= 0; i < 20 ; i++){
    strip.setPixelColor(plant1[i], none);
  }
}

//If plant/sensor 2 is touched light up its 20 specified LEDs in blue
if (val2 > 500) {
  for (int i = 0; i < 20; i ++){
    strip.setPixelColor(plant2[i], blue);
  }
  
} else {
  for (int i= 0; i < 20; i++){
    strip.setPixelColor(plant2[i], none);
  }
}

//set LEDs to a visable brightness
 strip.setBrightness(100);

//push this loops data to the strip to be shown
 strip.show();

delay(10);
}
