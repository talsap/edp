#include <Wire.h>

int valor;
int ad2;

void setup() {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino DUE)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino DUE)
 
}

void loop() {
  //aguarda a entrada do setpoint//
  if (Serial.available()>1){  
    valor = Serial.parseInt(); //valor em mbar
    analogWrite(DAC0, valor);
  }
  ad2 = analogRead(A2);
  Serial.println(ad2);
  delay(500);
}
