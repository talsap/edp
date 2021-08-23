/*******************************************************************
*             Arduino código para EDP software - Beta              *
* ---------------------------------------------------------------- *
* Criado por: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com     *
* Data – 14/06/2021 - v 1.0                                        *
********************************************************************/

/* Bibliotecas */
#include <Stepper.h>  //biblioteca para controlar motor de passos
#include <Oversampling.h>  //biblioteca de alteração da resolução

#define AR_12BIT_MAX   4096 //valor da resolucao do arduino
#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino com Oversampling

Oversampling adc(12, 16, 2); //aumentar a resolução do adc de 12bit para 16bit

/* Variavéis */
const int pinAplicador = 12; //pino do aplicador de golpes
int condConect = 0; //Condicao para conecxao com o software
int condicao = 2; //Condicao para iniciar o motor de passos
int frequencia; //Valor condicao para intervalo da frequencia
int contadorG = 1; //Valor que conta os golpes dentro da função *Intervalo de tempo do aplicador*
int nGolpe = 0; //numpero de golpes
int nTime = 0; //parte inteira do tempo
int ntotalGolpes; //Numero total de golpes por estagio
int statuS = 0; //(0 ou 1)(ok ou n_ok) mado de avisar erro de pressao do aplicador
int setpoint1; //Valor de entrada para o setpoint1 em milibar (0 - 10.000)mBar
int setpoint2; //Valor de entrada para o setpoint2 em milibar (0 - 10.000)mBar
int botoes; //Acoes do botoes pausar, parar e continuar o ensaio
int ad0; //valor analógico do LVDT1
int ad1; //valor analógico do LVDT2
int ad2; //valor analógico do sensor de pressão (Aplicador)
int ad3; //valor analógico do sensor de pressão (Camara)
float bit12_Voltage; //Usado para a conversao de bits ~ volts
float bit16_Voltage; //Usado para a conversao de bits ~ volts
float InputRange_code = 3.3f; //valor do ImputRange 3.3V
float ValMilivolt; //Valor do sensor de pressao em mBar
float setpointM; //Valor do setpointM
float setpointC; //Valor do setpointC  
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
long resultTempo[1];
unsigned long currentMillis; //variacao do tempo em milisegundos
unsigned long initialMillis; //tempo incial dinamico
unsigned char conexao;  //tipos de conexoes
unsigned char leitura;  //ler dado na porta serial

/* Estrutura da função S */
struct S{
  long t;
  int n;
};

Stepper mp(200, 8, 9, 10, 11); //Funcao definicao do motor de passos

/* Inicializacao da serial */
void setup(void) {
  Serial.begin(115200); //velocidade de cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino due)
  analogReference(AR_DEFAULT); //Define a tensao de 3.3Volts como sendo a padrao
  analogWrite(DAC0, 1); //pino responsavel em alterar a pressao de (Camara)
  pinMode(A0, INPUT); //pino LVDT1
  pinMode(A2, INPUT); //pino LVDT2
  pinMode(A4, INPUT); //pino Sensor de pressão (Aplicador)
  pinMode(A6, INPUT); //pino Sensor de pressão (Camara)
  pinMode(pinAplicador, OUTPUT);  //configura o pinAplicador
  mp.setSpeed(30); //velocidade de rotacao do motor de passos em rpm
  mp.step(0);  //inicia o motor de passos com zero passos
  bit12_Voltage = (InputRange_code)/(AR_12BIT_MAX - 1); //fator de convercao bit~voltagem
  bit16_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1); //fator de convercao bit~voltagem
  setpointM = 340/3.3f;   //setpointM inicia sendo o menor valor admissível (referente ao motor)
  setpointC = 10*255/3300;   //setpoint inicia sendo o menor valor admissível (referente a camara)
}

/* Principal */

void loop(void) {
  conexao:
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
        Serial.println("DNIT134");
        serialFlush();
        while(true){
          if(Serial.available()>0){
            leitura = Serial.read();
            if(leitura == 'B'){
              Serial.println("BREAK");
              serialFlush();
              goto conexao;
            }
            if(leitura == 'E'){
              Serial.println("CAMARA");
              serialFlush();
              goto camara;
            }
            if(leitura == 'M'){              
              Serial.println("MOTOR");
              serialFlush();
              goto motor;
            }
            if(leitura == 'G'){              
              Serial.println("GOLPES");
              serialFlush();
              goto golpes;
            }
            if(leitura == 'J'){              
              imprimir();
              serialFlush();
            }
            if(leitura == 'I'){
              Serial.println("IMPRIMIR");
              serialFlush();
              while(true){
                if(Serial.available()>0){
                  leitura = Serial.read();
                  if(leitura == 'S'){
                    goto sensorLVDTDNIT134;  
                  }
                }
                else{
                  imprimir();
                }
              }
            }
          }
        }
        break;
        
        //***********************//
        camara:
        //CAMARA DE PRESSAO//
        while(true){
          ad3 = analogRead(A6);
          vd3 = ad3*bit12_Voltage*1000;
          
          if (Serial.available()>1){
            setpoint2 = Serial.parseInt();    //valor em mbar
            if(setpoint2 > 5){
              Serial.print("CHEGOU="); 
              Serial.print(setpoint2);
              Serial.print("/SENSOR=");
              Serial.println(vd3*3.3f);
              serialFlush();
              setpointC = setpoint2*255/3300;   //valor em contagem
              analogWrite(DAC0, setpointC);
            }
            if(setpoint2 == 3){
              goto sensorLVDTDNIT134;
            }
          }
          else{
            //imprimir();
          }
        }
        break;
        
        //***********************//
        motor:
        //MOTOR DE PASSOS//
        while(true){
          ad2 = analogRead(A4);
          vd2 = ad2*bit12_Voltage*1000;
          
          if(Serial.available()>0){
            setpoint1 = Serial.parseInt();
            if(setpoint1 > 5){   
              Serial.print("CHEGOU="); 
              Serial.print(setpoint1);
              Serial.print("/SENSOR=");
              Serial.println(vd2*3.3f);
              serialFlush();
              condicao = 1;
            }
            if(setpoint1 == 3){
              digitalWrite(8, LOW);
              digitalWrite(9, LOW);
              digitalWrite(10, LOW);
              digitalWrite(11, LOW);
              condicao = 2;
              goto sensorLVDTDNIT134;
            }
            if(setpoint1 == 2){
              digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
              delay(100);
              digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
              delay(900);
              digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
              delay(100);
              digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
              delay(900);
              digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
              delay(100);
              digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
              setpoint1 = 120;
            }
            else{
              setpointM = setpoint1/3.3f;     //valor do setpoint em milibar (0 - 10.000)mBar
            }
          }
          
          //INTERVALO DE PRESSAO NAO OK//
          if((vd2 > 1.05*setpointM || vd2 < 0.95*setpointM) && condicao == 1){
            condicao = 0;
          }
          
          //INTERVALO DE PRESSAO OK//
          if(vd2 < 1.02*setpointM && vd2 > 0.98*setpointM){
            Serial.println("o");
            mp.step(0);
            condicao = 1;
          }         
            
          if(condicao == 0){
            Serial.println("n");
            mp.step(floor((setpointM - vd2)));
          }
        }
        break;

        //***********************//
        golpes:
        //RESPONSAVEL EM COLETAR A QUANTIDADE TOTAL DE GOLPES//
        while(true){ 
          if(Serial.available()> 0){
            ntotalGolpes = Serial.parseInt();
            if(ntotalGolpes > 0){
              Serial.print("NGOLPES="); 
              Serial.println(ntotalGolpes);
              serialFlush();
              break;
            }
            if(ntotalGolpes == -3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        //RESPONSAVEL EM COLETAR A FREQUENCIA DOS GOLPES//
        while(true){
          if(Serial.available()>0){
            frequencia = Serial.parseInt();
            if(frequencia > 0){
              Serial.print("FREQ="); 
              Serial.println(frequencia);
              serialFlush();
              break;
            }
            if(frequencia == -3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        
        currentMillis = millis(); //Tempo atual em ms
        initialMillis = currentMillis;  //Tempo inicial
        
        while(true){
          while(true){
            if((currentMillis - initialMillis)% 10 == 0 && (currentMillis - initialMillis)!= 0){
              imprimir();
              break;
            }
            else{
              delay(1);
              currentMillis = millis(); //Tempo atual em ms
            }
          }
          
          S resultTempo = tempo(nTime, frequencia, initialMillis);
          initialMillis = resultTempo.t;
          nTime = resultTempo.n;
          
          if(nGolpe == ntotalGolpes){
            while(currentMillis - initialMillis <= 990){
              currentMillis = millis(); //Tempo atual em ms
              while(true){
                if((currentMillis - initialMillis)% 10 == 0 && (currentMillis - initialMillis)!= 0){
                  imprimir();
                  break;
                }
                else{
                  delay(1);
                  currentMillis = millis(); //Tempo atual em ms
                }
              }
            }
            initialMillis = currentMillis;
            nGolpe = 0;
            nTime = 0;
            contadorG = 1;
            goto sensorLVDTDNIT134;
          }        
          
          
          if (Serial.available()> 0){  
            //aguarda o valor na serial e se for 3 "para" o ensaio//
            botoes = Serial.parseInt();
            if(botoes == 3){
              pararEnsaio:
              nGolpe = 0;
              nTime = 0;
              statuS = 0;
              currentMillis = millis();
              initialMillis = currentMillis;
              goto sensorLVDTDNIT134;
            }
            //aguarda o valor na serial. e se for 4 pausa o ensaio//
            if(botoes == 4){
              float guardavalor;
              guardavalor = float(currentMillis - initialMillis);
              while(true){
                imprimir();
                if (Serial.available()> 0){
                  botoes = Serial.parseInt();
                  //aguarda o valor na serial. e se for 2 continua o ensaio de onde parou//
                  if(botoes == 2){
                    currentMillis = millis();
                    initialMillis = currentMillis-guardavalor;
                    break;
                  }
                  //aguarda o valor na serial. e se for 3 "para" o ensaio//
                  if(botoes == 3){
                    goto pararEnsaio;
                  }
                }
              }
            }
          }
          
        }/*while*/
        break;
      }/*if(condConect == 1)*/
      
    /*******************************************************************/
    /************************* norma DNIT... ***************************/  
    /*******************************************************************/  
    case 'G':
      //caso receba G (acessa o ensaio da norma ...)
      if(condConect == 1){
        Serial.println("Ainda falta complementar");
        serialFlush();
      }
      break;
    
    /*******************************************************************/
    /*******************************************************************/  
    /*******************************************************************/ 
   
   }/*switch*/

}/*void*/

/* Imprimir dados na tela */
void imprimir(){
  ad0 = adc.read(A0); 
  ad1 = adc.read(A2); 
  vd0 = ad0*bit16_Voltage; 
  vd1 = ad1*bit16_Voltage; 
  ad2 = analogRead(A4);  
  ad3 = analogRead(A6); 
  vd2 = ad2*bit12_Voltage*1000; 
  vd3 = ad3*bit12_Voltage*1000;
  
  //INTERVALO DE PRESSAO NAO OK//
  if(vd2 > 1.05*setpointM && vd2 < 0.95*setpointM){
     statuS = 1;  //INFORMA QUE O ENSAIO FOI PARADO//
  }

  Serial.print(float(nTime)+float(currentMillis - initialMillis)/1000, 3);
  Serial.print(",");
  Serial.print(ad0);
  Serial.print(",");
  Serial.print(ad1);
  Serial.print(",");
  Serial.print(vd0);
  Serial.print(",");
  Serial.print(vd1);
  Serial.print(",");
  Serial.print(vd2*3.3f);
  Serial.print(",");
  Serial.print(vd3*3.3f);
  Serial.print(",");
  Serial.print(statuS);
  Serial.print(",");
  Serial.println(nGolpe);
  Serial.flush();
}/* Imprimir dados na tela */

/* Limpa o buffer serial */
void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}/* Limpa o buffer serial */

/* Intervalo de tempo do aplicador */
S tempo(int nTime, int frequencia, long initialMillis){
  currentMillis = millis(); //Tempo atual em ms
  switch(frequencia){
    case 1:
      if(currentMillis - initialMillis < intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo09){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;
      
    case 2:
      if(currentMillis - initialMillis < intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo05){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo05 && (currentMillis - initialMillis) <= intervalo05 + intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo05 + intervalo01){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;
            
    case 3:
      if(currentMillis - initialMillis < intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo04){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo04 && (currentMillis - initialMillis) <= intervalo04 + intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo04 + intervalo01 && (currentMillis - initialMillis) <= 2*intervalo04){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo04 && (currentMillis - initialMillis) <= 2*intervalo04+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > 2*intervalo04+intervalo01){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;
              
    case 4:
      if(currentMillis - initialMillis < intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador  
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) <= intervalo03){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo03 && (currentMillis - initialMillis) <= intervalo03+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo03+intervalo01 && (currentMillis - initialMillis) <= 2*intervalo03){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo03 && (currentMillis - initialMillis) <= 2*intervalo03+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > 2*intervalo03+intervalo01 && (currentMillis - initialMillis) <= 3*intervalo03){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo03 && (currentMillis - initialMillis) <= 3*intervalo03+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > 3*intervalo03+intervalo01){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 4){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;
              
    case 5:
      if(currentMillis - initialMillis < intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) <= intervalo02){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo02 && (currentMillis - initialMillis) <= intervalo02+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > intervalo02+intervalo01 && (currentMillis - initialMillis) <= 2*intervalo02){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo02 && (currentMillis - initialMillis) <= 2*intervalo02+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > 2*intervalo02+intervalo01 && (currentMillis - initialMillis) <= 3*intervalo02){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo02 && (currentMillis - initialMillis) <= 3*intervalo02+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > 3*intervalo02+intervalo01 && (currentMillis - initialMillis) <= 4*intervalo02){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 4){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 4*intervalo02 && (currentMillis - initialMillis) <= 4*intervalo02+intervalo01){
        digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
      }
      if((currentMillis - initialMillis) > 4*intervalo02+intervalo01){
        digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        if(contadorG == 5){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo09){
        initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
        nTime++;
        contadorG = 1;
      }
      break;
  }/*switch*/
  return {initialMillis, nTime};    
}/* Intervalo de tempo do aplicador */
