/*****************************************************************
* CODIGO ARDUINO DUE PARA FUNCIONAMENTO DO SOFTWARE EDP - BETA
* ----------------------------------------------------------------
* created by: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com
* Data – xx/xx/xxxx - v 1.0
******************************************************************/

/* Import das Bibliotecas */
#include <Oversampling.h>

/* Aumento da Resolução atraves
da biblioteca de Amostragens */
Oversampling adc(12, 16, 2);

/* Variaveis */
float voltA0, voltA1;

/* Inicialização setup */
void setup()
{
  Serial.begin(19200);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  analogReadResolution(12);
}

/* Loop Principal */
void loop(void){

  conexao = Serial.read();

  if  (conexao == 67){
    //caso receba C = 67 em decimal (verifica se há conexao com a porta serial)
    Serial.println("conectado");
    Serial.flush();
    cond = 1;
    }

  if (conexao == 68){
    //caso receba D = 68 em decimal (implica na desconexao com a porta serial)
    Serial.println("desconectado");
    Serial.flush();
    Serial.end();
    cond = 0;
    }

  if (conexao == 73 && cond == 1){
    //caso receba I = 73 em decimal (envia o dado do transdutor para porta serial)

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

}
