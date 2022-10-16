#include <CapacitiveSensor.h>
#include <Adafruit_NeoPixel.h>

#define LED_PIN 3
#define LED_COUNT 120
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
CapacitiveSensor Sensor1 = CapacitiveSensor(9, 6);
CapacitiveSensor Sensor2 = CapacitiveSensor(5, 10);

//define variables for capactive sensor values
long val1;
long val2;

//define colour varibles using RGB values
uint32_t pink = strip.Color(242, 90, 186);
uint32_t purple = strip.Color(144, 50, 206);
uint32_t none = strip.Color(0, 0, 0);

//define each object's LEDs that light up when it is tocuhed
int plant1[] = {1,2,5,6,9,10,13,14,17,18,22,23,26,27,30,31,34,35,38,39};
int plant2[] = {3,4,7,8,11,12,15,16,19,20,24,25,28,29,32,33,36,37,40};

void setup() {
Serial.begin(9600);
strip.begin(); //always needed
strip.show(); // 0 data => off.
strip.setBrightness(255); // ~20% (max = 255)
int n = strip.numPixels();
}

void loop() {

val1 = Sensor1.capacitiveSensor(30);
val2 = Sensor2.capacitiveSensor(30);

Serial.print(val1);
Serial.println();
Serial.print(val2);
Serial.println();

//If plant/sensor 1 is touched light up its 20 specified LEDs in pink
if (val1 > 500) {
  for (int i = 0; i < 20; i ++){
    strip.setPixelColor(plant1[i], pink);
  }
  
} else {
  for (int i= 0; i < 20 ; i++){
    strip.setPixelColor(plant1[i], none);
  }
}

//If plant/sensor 2 is touched light up its 20 specified LEDs in purple
if (val2 > 500) {
  for (int i = 0; i < 20; i ++){
    strip.setPixelColor(plant2[i], purple);
  }
  
} else {
  for (int i= 0; i < 20; i++){
    strip.setPixelColor(plant2[i], none);
  }
}

//push this loops data to the strip to be shown
 strip.show();

delay(10);
}
