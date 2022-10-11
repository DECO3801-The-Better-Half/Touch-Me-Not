int knobValue0 = 0;
int knobValue1 = 0;
int knobValue2 = 0;
int knobValue3 = 0;
int knobValue4 = 0;

void setup() {
  Serial.begin(9600);

}

void loop() {
  knobValue0 = analogRead(0);
  knobValue1 = analogRead(1);
  knobValue1 = analogRead(2);
  knobValue1 = analogRead(3);
  knobValue1 = analogRead(4);
     
  Serial.print(knobValue0);
  Serial.print(" ");
  Serial.print(knobValue1);
  Serial.print(" ");
  Serial.print(knobValue2);
  Serial.print(" ");
  Serial.print(knobValue3);
  Serial.print(" ");
  Serial.print(knobValue4);
  Serial.println();
  
  
  delay(5);
}
