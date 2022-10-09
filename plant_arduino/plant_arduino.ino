/* Adapted from XOPA ART https://www.dropbox.com/s/yl2rqcrgcoy2iwq/ArduinoPlantTouch.pdf?dl=0 */

#include <CapacitiveSensor.h>
#include <Adafruit_NeoPixel.h>
#define LED_PIN 6
#define LED_COUNT 120
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
CapacitiveSensor Sensor1 = CapacitiveSensor(8, 9);

long val1;

void setup()
{
Serial.begin(9600);
strip.begin(); //always needed
strip.show(); // 0 data => off.
strip.setBrightness(50); // ~20% (max = 255)
int n = strip.numPixels();
}

void
loop()
{
val1 = Sensor1.capacitiveSensor(30);

Serial.print(val1);;
Serial.println();

if (val1 > 500) {
  strip.setBrightness(100);
} else {
  strip.setBrightness(0);
  
}
int n = strip.numPixels();
for (int i = 0; i < n; i++)
   {
   int pixelHue = (i * 65536L / n);
   strip.setPixelColor(i,
   strip.gamma32(strip.ColorHSV(pixelHue))
   );
 }

 strip.show();



delay(10);
}
