/* Adapted from XOPA ART https://www.dropbox.com/s/yl2rqcrgcoy2iwq/ArduinoPlantTouch.pdf?dl=0 */

#include <CapacitiveSensor.h>
CapacitiveSensor Sensor1 = CapacitiveSensor(4, 6);
CapacitiveSensor Sensor2 = CapacitiveSensor(8, 10);

long val1;
long val2;
int pos;

void setup()
{
Serial.begin(9600);
}

void
loop()
{
val1 = Sensor1.capacitiveSensor(30);
val2 = Sensor2.capacitiveSensor(30);

Serial.print(val1);
Serial.print(" ");
Serial.print("\t");

Serial.print(val2);
Serial.print(" ");
Serial.print("\t");

Serial.println();
delay(2);

if (val1 >= 100 && pos == 0)
{
pos = 1;
delay(50);
}

else if (val1 >= 100 && pos == 1)
{
pos = 0;
delay(50);
}

if (val2 >= 100 && pos == 0)
{
pos = 1;
delay(50);
}

else if (val2 >= 100 && pos == 1)
{
pos = 0;
delay(50);
}
delay(10);
}
