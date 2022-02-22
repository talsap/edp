/*******************************************************************
*             Arduino código para EDP software - Beta              *
* ---------------------------------------------------------------- *
* Criado por: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com     *
* Data – 22/02/2022 - calibração                                   *
********************************************************************/

/* Bibliotecas */
#include <Oversampling.h>  //biblioteca de alteração da resolução

#define AR_12BIT_MAX   4096 //valor da resolucao do arduino DUE
#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino com Oversampling
#define num1   10 //número de iterações da média móvel 1
#define num2   10 //número de iterações da média móvel 2

Oversampling adc(12, 16, 2); //aumentar a resolução do adc de 12bit para 16bit (apenas arduino DUE)

/* Variavéis */
int i; //indicador
int ad0; //valor analógico do LVDT1
int ad1; //valor analógico do LVDT2
int ad2; //valor analógico do LVDT3
int ad3; //valor analógico do LVDT4
float bit12_Voltage; //Usado para a conversao de bits ~ volts
float bit16_Voltage; //Usado para a conversao de bits ~ volts
float InputRange_code = 3.3f; //valor do ImputRange 3.3V
unsigned char conexao;  //tipos de conexoes

/* Inicializacao da serial */
void setup() {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino DUE)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino DUE)
  analogReference(AR_DEFAULT); //Define a tensao de 3.3Volts como sendo a padrao (apenas no arduino DUE)
  pinMode(A4, INPUT); //pino LVDT1
  pinMode(A6, INPUT); //pino LVDT2
  pinMode(A8, INPUT); //pino LVDT3
  pinMode(A9, INPUT); //pino LVDT4
  bit12_Voltage = (InputRange_code)/(AR_12BIT_MAX - 1); //fator de convercao bit~voltagem
  bit16_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1); //fator de convercao bit~voltagem
}

/* Principal */
void loop() {
  conexao:
  conexao = Serial.read();

  switch(conexao){
    case 'a':
      for(i = 0; i < 10; i++){
        ad0 = adc.read(A4);
        Serial.println(ad0);
        delay(500);
        if(i==9) Serial.println("----");
        }
      break;
    case 'b':
      for(i = 0; i < 10; i++){
        ad1 = adc.read(A6);
        Serial.println(ad1);
        delay(500);
        if(i==9) Serial.println("----");
        }
      break;
    case 'c':
      for(i = 0; i < 10; i++){
        ad2 = adc.read(A8);
        Serial.println(ad2);
        delay(500);
        if(i==9) Serial.println("----");
        }
      break;
    case 'd':
      for(i = 0; i < 10; i++){
        ad3 = adc.read(A9);
        Serial.println(ad3);
        delay(500);
        if(i==9) Serial.println("----");
        }
      break;
    }/*switch Principal*/
}/*void Principal*/
