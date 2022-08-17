int button1 = 2;
int button2 = 3;
int button3 = 4;
int ptPin0 = 0;
int ptPin1 = 1;
int knobValue1 = 0;
int knobValue2 = 0;

boolean reading1;
boolean reading2;
boolean reading3;
boolean reading4;

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
  
  knobValue1 = analogRead(ptPin0);
  knobValue2 = analogRead(ptPin1);
  
  
  delay(5);

  Serial.print(reading1);
  Serial.print(",");
  Serial.print(reading2);
  Serial.print(",");
  Serial.print(reading3);
  Serial.print(",");
  Serial.print(knobValue1);
  Serial.print(",");
  Serial.print(knobValue2);
  Serial.println();

}
