#include <Wire.h>

int valor;
int ad0;

void setup() {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino DUE)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino DUE)
 
}

void loop() {
  //aguarda a entrada do setpoint//
  if (Serial.available()>1){  
    valor = Serial.parseInt(); //valor em contagem enviado ao DAC [0-4095]
    analogWrite(DAC0, valor);
    analogWrite(DAC1, 0);
    delay(5000);
    int acc = 0;
    for(int i=0; i<10; i++){
      ad0 = analogRead(A0); // ler o sensor de pressão da valvula proporcional;
      acc = acc + ad0;
      delay(500);
    }
    Serial.println(acc/10);
    Serial.println("----");
  }
  //ad0 = analogRead(A0); // ler o sensor de pressão da valvula proporcional;
  //Serial.println(ad0);
  //delay(500);
}
