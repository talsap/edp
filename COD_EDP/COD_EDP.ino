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

#define AR_12BIT_MAX   4096 //valor da resolucao do arduino
#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino com Oversampling

Oversampling adc(12, 16, 2); //motor de passos

/* Variables */

const int pinAplicador = 12; //pino do apolicador de golpes
int condConect = 0; //Condicao para conecxao com o software
int condicao = 1; //Condicao para o aplicador de golpes
int setpoint1; //Valor de entrada para o setpoint em milibar (0 - 10.000)mBar
float bit12_Voltage; //Usado para a conversao de bits ~ volts
float bit16_Voltage; //Usado para a conversao de bits ~ volts
float InputRange_code = 3.3f; //valor do ImputRange 3.3V
float ValMilivolt; //Valor do sensor de pressao em mBar
float setpoint; //Valor do setpoint 
float camara; //valor da pressao na camara
float valor;
float ad0; //valor analógico do LVDT1
float ad1; //valor analógico do LVDT2
float ad2; //valor analógico do sensor de pressão (Aplicador)
float ad3; //valor analógico do sensor de pressão (Camara)
float vd0; //valor em voltagem do LVDT1
float vd1; //valor em voltagem do LVDT2
float vd2; //valor do sensor de pressão em mBar (Aplicador)
float vd3; //valor do sensor de pressão em mBar (Camara)
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
  Serial.begin(115200); //velocidade de cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino due)
  analogWrite(DAC0, 15); //pino responsavel em alterar a pressao de (Camara)
  pinMode(A0, INPUT); //pino LVDT1
  pinMode(A1, INPUT); //pino LVDT2
  pinMode(A2, INPUT); //pino Sensor de pressão (Aplicador)
  pinMode(A3, INPUT); //pino Sensor de pressão (Camara)
  pinMode(pinAplicador, OUTPUT);  //configura o pinAplicador
  mp.setSpeed(30); //velocidade de rotacao do motor de passos em rpm
  mp.step(0);  //inicia o motor de passos com zero passos
  bit12_Voltage = (InputRange_code)/(AR_12BIT_MAX - 1); //fator de convercao bit~voltagem
  bit16_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1); //fator de convercao bit~voltagem
  setpoint = 0;   //setpoint inicia sendo o valor zero
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
          vd0 = ad0*bit16_Voltage; 
          vd1 = ad1*bit16_Voltage; 
          ad2 = analogRead(A2);  
          ad3 = analogRead(A3); 
          vd2 = ad2*bit12_Voltage*1000; 
          vd3 = ad3*bit12_Voltage*1000; 
          Serial.print(ad0);
          Serial.print(" , ");
          Serial.print(ad1);
          Serial.print(" , ");
          Serial.print(vd0);
          Serial.print(" , ");
          Serial.print(vd1);
          Serial.print(" , ");
          Serial.print(vd2);
          Serial.print(" , ");
          Serial.println(vd3);
          Serial.flush();
          delay(5);
          if(leitura == 'B'){
            break;
            }
          if(leitura == 'M'){
            goto motor;
            }
          }
        break;

        //***********************//
        motor:
        while(true){
          leitura = Serial.read();
          ad0 = adc.read(A0); 
          ad1 = adc.read(A1); 
          vd0 = ad0*bit16_Voltage; 
          vd1 = ad1*bit16_Voltage; 
          ad2 = analogRead(A2);  
          ad3 = analogRead(A3); 
          vd2 = ad2*bit12_Voltage*1000; 
          vd3 = ad3*bit12_Voltage*1000; 
          Serial.print(ad0);
          Serial.print(" , ");
          Serial.print(ad1);
          Serial.print(" , ");
          Serial.print(vd0);
          Serial.print(" , ");
          Serial.print(vd1);
          Serial.print(" , ");
          Serial.print(vd2);
          Serial.print(" , ");
          Serial.println(vd3);
          Serial.flush();
          delay(5);
          if(leitura == 'B'){
            break;
            }
            
          if(Serial.available()>1){
            setpoint1 = Serial.parseInt();
            setpoint = setpoint1/3.3;
            condicao = 0;
            }
            
          //INTERVALO DE PRESSÃO OK//
          if(vd2 < 1.05*setpoint && vd2 > 0.95*setpoint){
            Serial.println("ok");
            mp.step(0);
            }
            
          //INTERVALO DE PRESSÃO NÃO OK//
          if(condicao == 0){
            Serial.println("no_ok");
            mp.step(floor(setpoint - vd2));
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
