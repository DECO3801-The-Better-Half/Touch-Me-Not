int button1 = 2;
int button2 = 3;
int button3 = 4;
int ptPin = 0;
int knobValue = 0;

boolean reading1;
boolean reading2;
boolean reading3;

void setup() {
  // put your setup code here, to run once:
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);

  digitalWrite(button1, HIGH);
  digitalWrite(button2, HIGH);
  digitalWrite(button3, HIGH);

  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  reading1 = !digitalRead(button1); 
  reading2 = !digitalRead(button2);
  reading3 = !digitalRead(button3);
  knobValue = analogRead(ptPin);
  
  delay(15);

  Serial.print(reading1);
  Serial.print(",");
  Serial.print(reading2);
  Serial.print(",");
  Serial.print(reading3);
  Serial.print(",");
  Serial.print(knobValue);
  Serial.println();

}
