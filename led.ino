#define RED 8
#define GREEN 9
#define BLUE 10

byte byteRead;

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    byteRead = Serial.read();
    if (byteRead >= (byte)'0' &  byteRead <= (byte)'9') {
      byteRead = byteRead - (byte)'0';
      if (byteRead & 0x01) {
        digitalWrite(BLUE, HIGH);
      } else {
        digitalWrite(BLUE, LOW);
      }
      
      if (byteRead & 0x02) {
        digitalWrite(GREEN, HIGH);
      } else {
        digitalWrite(GREEN, LOW);
      }
      
      if (byteRead & 0x04) {
        digitalWrite(RED, HIGH);
      } else {
        digitalWrite(RED, LOW);
      }
      Serial.write("Mode ");
      Serial.write(byteRead+(byte)'0');
      Serial.write(" OK\n");
    }
  }
}

void cycle() {
  digitalWrite(RED, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);  
  digitalWrite(RED, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(GREEN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000); 
  digitalWrite(GREEN, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(BLUE, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);
  digitalWrite(BLUE, LOW);   // turn the LED on (HIGH is the voltage level)
}

void nope() {
  delay(1000);
}

