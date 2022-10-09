int knobValue = 0;

void setup() {
  Serial.begin(9600);

}

void loop() {
  knobValue = analogRead(0);
  Serial.println(knobValue);

  delay(5);
}
