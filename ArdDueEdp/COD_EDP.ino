/*******************************************************************
*           Código arduino para o software EDP - Beta              *
* ---------------------------------------------------------------- *
* created by: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com     *
* Data – 25/02/2021 - v 1.0                                        *
********************************************************************/
/* Import from Libraries */
#include <Wire.h>
#include <Oversampling.h>

#define ADC_16BIT_MAX   65536

Oversampling adc(12, 16, 2); 

/* Variables */
int condConect = 0;
float ad0, ad1, vd0, vd1, bit_Voltage;
float InputRange_code = 3.3f;
unsigned char conexao, leitura;

/* Initialization serial */
void setup(void) {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  bit_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1);
}

/* Main */
void loop(void) {
  
  conexao = Serial.read();
  
  switch(conexao){
/*******************************************************************/
    case 'C':
      //caso receba C (verifica se há conexao com a porta serial)
      Serial.println("conectado");
      Serial.flush();
      condConect = 1;
      break;

/*******************************************************************/  
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
      if(condConect == 1){
        //caso receba I (acessa o ensaio da norma DNIT134)

        //***********************//
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
            goto sensor;
            }
          }
        break;

        //***********************//
        sensor:
        while(true){
          leitura = Serial.read();
          Serial.println("sensor");
          Serial.flush();
          delay(5);
          if(leitura == 'd'){
            break;
            }
          
          }
       
        
      }
      
/*******************************************************************/
/************************* norma DNIT... ***************************/  
/*******************************************************************/  
    case 'G':
      if(condConect == 1){
        //caso receba I (acessa o ensaio da norma ...)
        Serial.println("Ainda falta complementar");
      }

/*******************************************************************/
/*******************************************************************/  
/*******************************************************************/ 
   
   }/*switch*/

}/*void*/
