#include <Stepper.h>
#include <Wire.h>

int valor;
int ad0;
Stepper mp(200, 8, 9, 10, 11);  //Função definição do motor de passo

void setup() {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino DUE)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino DUE)
  mp.setSpeed(30);  //Velocidade da rotação do motor de passo em rpm
  mp.step(0);  //Inicia com o motor com zero passos
 
}

void loop() {
  //aguarda a entrada do setpoint//
  if (Serial.available()>1){  
    valor = Serial.parseInt();
    mp.step(floor(valor));
  }
  ad0 = analogRead(A0);
  Serial.println(ad0);
  delay(500);
}
