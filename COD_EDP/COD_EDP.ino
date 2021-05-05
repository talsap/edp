/*******************************************************************
*               Arduino code for EDP software - Beta               *
* ---------------------------------------------------------------- *
* Creado por: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com     *
* Data – 05/05/2021 - v 1.0                                        *
********************************************************************/

/* Import das Bibliotecas */
#include <Wire.h>
#include <Stepper.h>
#include <Oversampling.h> 

#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino

Oversampling adc(12, 16, 2); //motor de passos

/* Variables */

const int pinAplicador = 12; //pino do apolicador de golpes
int condConect = 0; //Condicao para conecxao com o software
int condicao = 1; //Condicao para o aplicador de golpes
float bit_Voltage; //Usado para a conversao de bit ~ volts
float InputRange_code = 3.3f; //valor do ImputRange 3.3V
float val; //valor analogico do sensor de pressao
float ValMilivolt; //valor do sensor de pressao em mBar
float setpoint; //setpoint
float setponit1; //valor de entrada esperado para o setpoint
float camara; //valor da pressao na camara
float valor;
float ad0;
float ad1;
float vd0;
float vd1;
long intervalo01 = 100; //100 milseg Freq.
long intervalo09 = 1000; //1Hz 01-09
long intervalo05 = 500; //2Hz 01-04-01-04
long intervalo04 = 333; //3Hz 01-0233-01-0233-01-0233
long intervalo03 = 250; //4Hz 01-015-01-015-01-015-01-015
long intervalo02 = 200; //5Hz 01-01-01-01-01-01-01-01-01-01
unsigned long currentMillis; //variacao do tempo em milisegundos
unsigned char conexao;  //tipos de conexoes
unsigned char leitura;

Stepper mp(200, 8, 9, 10, 11); //Funcao definicao do motor de passos

/* Inicializacao da serial */
void setup(void) {
  Serial.begin(115200);
  analogReadResolution(12);
  analogWrite(DAC0, 15);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(pinAplicador, OUTPUT);  //configura o pinAplicador
  mp.setSpeed(30); //velocidade de rotacao do motor de passos em rpm
  mp.step(0);  //inicia o motor de passos com zero passos 
  bit_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1);
}

/* Principal */
void loop(void) {
  
  conexao = Serial.read();
  
  switch(conexao){
    /*************************************************************/
    case 'C':
      //caso receba C (verifica se há conexao com a porta serial)
      Serial.println("conectado");
      Serial.flush();
      condConect = 1;
      break;

    /*************************************************************/  
    case 'D':
      //caso receba D (implica na desconexao com a porta serial)
      Serial.println("desconectado");
      Serial.flush();
      Serial.end();
      condConect = 0;
      break;
      
    /*******************************************************************/
    /************************* norma DNIT134 ***************************/  
    /*******************************************************************/
    case 'I':  
      //caso receba I (acessa o ensaio da norma DNIT134)
      if(condConect == 1){  
        //****************************//
        sensorLVDTDNIT134:
        while(true){
          leitura = Serial.read();
          ad0 = adc.read(A0);
          ad1 = adc.read(A1);
          vd0 = adc.read(A0)*bit_Voltage;
          vd1 = adc.read(A1)*bit_Voltage;
          Serial.print(ad0);
          Serial.print(" , ");
          Serial.print(ad1);
          Serial.print(" , ");
          Serial.print(vd0);
          Serial.print(" , ");
          Serial.println(vd1);
          Serial.flush();
          delay(5);
          if(leitura == 'd'){
            break;
            }
          if(leitura == 's'){
            goto motor;
            }
          }
        break;

        //***********************//
        motor:
        while(true){
          leitura = Serial.read();
          Serial.println("motor");
          Serial.flush();
          delay(5);
          if(leitura == 'd'){
            break;
            }
          
          }
        
      }
      break;
      
    /*******************************************************************/
    /************************* norma DNIT... ***************************/  
    /*******************************************************************/  
    case 'G':
      //caso receba G (acessa o ensaio da norma ...)
      if(condConect == 1){
        Serial.println("Ainda falta complementar");
      }
      break;
    /*******************************************************************/
    /*******************************************************************/  
    /*******************************************************************/ 
   
   }/*switch*/

}/*void*/
