#include <CapacitiveSensor.h>
#include <Adafruit_NeoPixel.h>

const int lampPin = A5;

#define LED_PIN 11
#define LED_COUNT 120

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

uint32_t green = strip.Color(0,255, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t none = strip.Color(0, 0, 0);

//define each object's LEDs that light up when it is tocuhed
int plant1[] = {1,2,5,6,9,10,13,14,17,18,22,23,26,27,30,31,34,35,38,39};
int plant2[] = {3,4,7,8,11,12,15,16,19,20,24,25,28,29,32,33,36,37,40};

const int NUMBER_OF_SENSORS = 4;
CapacitiveSensor Sensor1 = CapacitiveSensor(2, 3);
CapacitiveSensor Sensor2 = CapacitiveSensor(4, 5);
CapacitiveSensor Sensor3 = CapacitiveSensor(6, 7);
CapacitiveSensor Sensor4 = CapacitiveSensor(8, 9);

CapacitiveSensor sensors[4] = {Sensor1, Sensor2, Sensor3, Sensor4};

long values[4];

void setup() {
   Serial.begin(9600);
   strip.begin(); //always needed
   strip.show(); // 0 data => off.
   strip.setBrightness(255); // ~20% (max = 255)
   int n = strip.numPixels();

}

void loop() {

    
    for (int i = 0; i < NUMBER_OF_SENSORS; i = i + 1) {
      values[i] = sensors[i].capacitiveSensor(20);
      sensors[i].set_CS_Timeout_Millis(20);
    }
  
    if (values[0] > 200) {
      for (int i = 0; i < 20; i ++){
        strip.setPixelColor(plant1[i], green);
       }
    } else {
      for (int i = 0; i < 20; i ++){
        strip.setPixelColor(plant1[i], none);
       }
    }

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
