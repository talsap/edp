#include <Oversampling.h>

Oversampling adc(12, 16, 2); 
float voltA0, voltA1;

void setup()
{
  Serial.begin(19200);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  analogReadResolution(12);
}

void loop()
{
  voltA0 = map(analogRead(A0), 0, 4095, 0, 330);
  Serial.print(voltA0/100);
  Serial.print(" ");
  Serial.print(adc.read(A0));
  Serial.print(" - ");

  voltA1 = map(analogRead(A1), 0, 4095, 0, 330);
  Serial.print(voltA1/100);
  Serial.print(" ");
  Serial.println(adc.read(A1));
  delay(10);
}
