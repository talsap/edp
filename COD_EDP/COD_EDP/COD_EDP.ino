/*******************************************************************
*             Arduino código para EDP software - Beta              *
* ---------------------------------------------------------------- *
* Criado por: Tarcisio Sapucaia - tarcisiosapucaia27@gmail.com     *
* Data – 14/06/2021 - v 1.0                                        *
********************************************************************/

/* Bibliotecas */
#include <Stepper.h>  //biblioteca para controlar motor de passos
#include <Oversampling.h>  //biblioteca de alteração da resolução
#include <waveforms.h>  //biblioteca que gera a função (1-cos)/2

#define AR_12BIT_MAX   4096 //valor da resolucao do arduino
#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino com Oversampling

Oversampling adc(12, 16, 2); //aumentar a resolução do adc de 12bit para 16bit

/* Variavéis */
const int pinAplicador = 12; //pino do aplicador de golpes DNIT134
const int pinAplicadorr = 7; //pino do aplicador de golpes DNIT135
int condConect = 0; //Condicao para conecxao com o software
int condicao = 2; //Condicao para iniciar o motor de passos
int conditionEnsaio = 0; //Condicao de Ensaio (0 - DNIT134 | 1 - DNIT135)
int frequencia; //Valor condicao para intervalo da frequencia
int contadorG = 1; //Valor que conta os golpes dentro da função *Intervalo de tempo do aplicador*
int nGolpe = 0; //numpero de golpes
int nTime = 0; //parte inteira do tempo
int ntotalGolpes; //Numero total de golpes por estagio
int statuS = 0; //(0 ou 1)(ok ou n_ok) mado de avisar erro de pressao do aplicador
int botoes; //Acoes do botoes pausar, parar e continuar o ensaio
int ad0; //valor analógico do LVDT1
int ad1; //valor analógico do LVDT2
int ad2; //valor analógico do sensor de pressão (Aplicador)
int ad3; //valor analógico do sensor de pressão (Camara)
int i; //indicador temporal da funcao waveforms
int setpoint1; //Valor de entrada para o setpoint1 em milibar (0 - 10.000)mBar
int setpoint2; //Valor de entrada para o setpoint2 em milibar (0 - 10.000)mBar
float setpointB; //Valor do setpointB
float setpointC; //Valor do setpointC
float setpointD; //Valor do setpointD
float setpointM; //Valor do setpointM
float bit12_Voltage; //Usado para a conversao de bits ~ volts
float bit16_Voltage; //Usado para a conversao de bits ~ volts
float InputRange_code = 3.3f; //valor do ImputRange 3.3V
float ValMilivolt; //Valor do sensor de pressao em mBar
float vd0; //valor em voltagem do LVDT1
float vd1; //valor em voltagem do LVDT2
float vd2; //valor do sensor de pressão em mBar (Aplicador)
float vd3; //valor do sensor de pressão em mBar (Camara)
long intervalo00 = 50; // 50 miliseg
long intervalo01 = 100; //100 milise
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
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino due)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino due)
  analogReference(AR_DEFAULT); //Define a tensao de 3.3Volts como sendo a padrao
  analogWrite(DAC0, 1); //pino responsavel em alterar a pressao de (Camara)
  pinMode(A4, INPUT); //pino LVDT1
  pinMode(A6, INPUT); //pino LVDT2
  pinMode(A0, INPUT); //pino Sensor de pressão (Aplicador)
  pinMode(A2, INPUT); //pino Sensor de pressão (Camara)
  pinMode(pinAplicador, OUTPUT);  //configura o pinAplicador
  pinMode(pinAplicadorr, OUTPUT);  //configura o pinAplicadorr
  digitalWrite(pinAplicadorr, HIGH);  //inicia com desativa o pinAplicador
  mp.setSpeed(30); //velocidade de rotacao do motor de passos em rpm
  mp.step(0);  //inicia o motor de passos com zero passos
  bit12_Voltage = (InputRange_code)/(AR_12BIT_MAX - 1); //fator de convercao bit~voltagem
  bit16_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1); //fator de convercao bit~voltagem
  setpointM = 340/InputRange_code;   //setpointM inicia sendo o menor valor admissível (referente ao motor)
  setpointC = int(10*4095/3300);   //setpoint inicia sendo o menor valor admissível (referente a camara)
}

/* Principal */

void loop(void) {
  conexao:
  conexao = Serial.read();

  switch(conexao){
    //**********************************************************************************//
    case 'C':
      //caso receba C (verifica se há conexao com a porta serial)
      Serial.println("conectado");
      Serial.flush();
      condConect = 1;
      break;

    //**********************************************************************************//
    case 'D':
      //caso receba D (implica na desconexao com a porta serial)
      Serial.println("desconectado");
      Serial.flush();
      Serial.end();
      condConect = 0;
      break;

    case 'I':
      //caso receba I (acessa o ensaio da norma DNIT134)

      //**********************************************************************************//
      //**********************************************************************************//
      //********************************* norma DNIT135 **********************************//
      //**********************************************************************************//
      //**********************************************************************************//

      if(condConect == 1){
        sensorLVDTDNIT134:
        Serial.println("DNIT134");
        conditionEnsaio = 0;
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
              goto camaraDNIT134;
            }
            if(leitura == 'M'){
              Serial.println("MOTOR");
              serialFlush();
              goto motorDNIT134;
            }
            if(leitura == 'G'){
              Serial.println("GOLPES");
              serialFlush();
              goto golpesDNIT134;
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

        //**********************************************************************************//
        //****************************** CAMARA DE PRESSAO *********************************//
        camaraDNIT134:
        while(true){
          ad3 = analogRead(A2);
          vd3 = ad3*bit12_Voltage*1000;
          if (Serial.available()>1){
            setpoint2 = Serial.parseInt();    //valor em mbar
            if(setpoint2 > 10){
              Serial.print("CHEGOU=");
              Serial.print(setpoint2);
              Serial.print("/SENSOR=");
              Serial.println(vd3*3.3f);
              serialFlush();
              setpointC = setpoint2*4095/3300;   //valor em contagem
              analogWrite(DAC0, setpointC);
            }
            if(setpoint2 == 3){
              goto sensorLVDTDNIT134;
            }
          }
        }
        break;

        //**********************************************************************************//
        //******************************** MOTOR DE PASSOS *********************************//
        motorDNIT134:
        while(true){
          ad2 = analogRead(A0);
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
          if((vd2 > 1.05*setpointM || vd2 < 0.95*setpointM) && condicao == 1){ //INTERVALO DE PRESSAO NAO OK//
            condicao = 0;
          }
          if(vd2 < 1.02*setpointM && vd2 > 0.98*setpointM){ //INTERVALO DE PRESSAO OK//
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

        //**********************************************************************************//
        //************************************ GOLPES **************************************//
        golpesDNIT134:
        while(true){ //RESPONSAVEL EM COLETAR A QUANTIDADE TOTAL DE GOLPES/
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
        while(true){ //RESPONSAVEL EM COLETAR A FREQUENCIA DOS GOLPES//
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
                  delayMicroseconds(1);
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

          if (Serial.available()> 0){ //aguarda o valor na serial e se for 3 "para" o ensaio//
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
            if(botoes == 4){ //aguarda o valor na serial. e se for 4 pausa o ensaio//
              float guardavalor;
              guardavalor = float(currentMillis - initialMillis);
              while(true){
                imprimir();
                if (Serial.available()> 0){
                  botoes = Serial.parseInt();
                  if(botoes == 2){ //aguarda o valor na serial. e se for 2 continua o ensaio de onde parou//
                    currentMillis = millis();
                    initialMillis = currentMillis-guardavalor;
                    break;
                  }
                  if(botoes == 3){ //aguarda o valor na serial. e se for 3 "para" o ensaio//
                    goto pararEnsaio;
                  }
                }
              }
            }
          }
          if((currentMillis - initialMillis)% 10 == 0 && (currentMillis - initialMillis)!= 0){
            imprimir();
          }
          else{
            delayMicroseconds(1);
            currentMillis = millis(); //Tempo atual em ms
          }
        }/*while*/
        break;
      }/*if(condConect == 1)*/

    case 'J':
    //caso receba J (acessa o ensaio da norma DNIT135)

    //**********************************************************************************//
    //**********************************************************************************//
    //********************************* norma DNIT135 **********************************//
    //**********************************************************************************//
    //**********************************************************************************//

      if(condConect == 1){
        sensorLVDTDNIT135:
        Serial.println("DNIT135");
        conditionEnsaio = 1;
        serialFlush();
        while(true){
          if(Serial.available()>0){
            leitura = Serial.read();
            if(leitura == 'B'){
              Serial.println("BREAK");
              serialFlush();
              goto conexao;
            }
            if(leitura == 'G'){
              Serial.println("GOLPES");
              serialFlush();
              goto golpesDNIT135;
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
                    goto sensorLVDTDNIT135;
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

        //**********************************************************************************//
        //************************************ GOLPES **************************************//
        golpesDNIT135:
        while(true){ //RESPONSAVEL EM COLETAR A QUANTIDADE TOTAL DE GOLPES//
          if(Serial.available()> 0){
            ntotalGolpes = Serial.parseInt();
            if(ntotalGolpes > 0){
              Serial.print("NGOLPES=");
              Serial.println(ntotalGolpes);
              serialFlush();
              break;
            }
            if(ntotalGolpes == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }
        while(true){ //RESPONSAVEL EM COLETAR A FREQUENCIA DOS GOLPES//
          if(Serial.available()> 0){
            frequencia = Serial.parseInt();
            if(frequencia > 0){
              Serial.print("FREQ=");
              Serial.println(frequencia);
              serialFlush();
              break;
            }
            if(frequencia == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }
        while(true){ //RESPONSAVEL EM COLETAR A CARGA CÍCLICA// valor em mbar
          if(Serial.available()> 0){
            setpoint1 = Serial.parseInt();
            if(setpoint1 > 10){
              Serial.print("CHEGOU=");
              Serial.println(setpoint1);
              setpointB = setpoint1*4095/3300;   //valor em contagem
              serialFlush();
              break;
            }
            if(setpoint1 == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }
        while(true){ //RESPONSAVEL EM COLETAR A PRESSAO DE CONTATO// variacao (29 ~ 100) mbar
          if(Serial.available()>0){
            setpoint2 = Serial.parseInt();
            if(setpoint2 > 10){
              Serial.print("CHEGOU=");
              Serial.println(setpoint2);
              setpointC = setpoint2*4095/3300;   //valor em contagem
              digitalWrite(pinAplicadorr, LOW);  //ativa o pinAplicador
              serialFlush();
              break;
            }
            if(setpoint2 == -3){
              goto sensorLVDTDNIT135;
            }
          }
        }

        currentMillis = millis(); //Tempo atual em ms
        initialMillis = currentMillis;  //Tempo inicial

        while(true){
          S resultTempo = tempo(nTime, frequencia, initialMillis);
          initialMillis = resultTempo.t;
          nTime = resultTempo.n;

          if(nGolpe == ntotalGolpes){ //CONDIÇAO DE PARAR O ENSAIO E IMPRIMIR 1S DE DADOS FINAIS
            while(currentMillis - initialMillis <= 990){
              currentMillis = millis(); //Tempo atual em ms
              while(true){
                if((currentMillis - initialMillis)% 5 == 0 && (currentMillis - initialMillis)!= 0){
                  imprimir();
                  break;
                }
                else{
                  delayMicroseconds(1);
                  currentMillis = millis(); //Tempo atual em ms
                }
              }
            }
            initialMillis = currentMillis;
            nGolpe = 0;
            nTime = 0;
            contadorG = 1;
            digitalWrite(pinAplicadorr, HIGH);  //desativa o pinAplicador
            analogWrite(DAC0, 0);  //SETA UM VALOR ZERO NO DAC0
            goto sensorLVDTDNIT135;
          }
          if (Serial.available()> 0){ //CONDICAO DE FUNCIONALIDADES AO DECORRER DO ENSAIO
            botoes = Serial.parseInt();
            if(botoes == 3){ //aguarda o valor na serial e se for 3 "para" o ensaio//
              pararEnsaioDNIT135:
              nGolpe = 0;
              nTime = 0;
              statuS = 0;
              currentMillis = millis();
              initialMillis = currentMillis;
              digitalWrite(pinAplicadorr, HIGH);  //desativa o pinAplicador
              analogWrite(DAC0, 0);  //SETA UM VALOR ZERO NO DAC0
              goto sensorLVDTDNIT135;
            }
            if(botoes == 4){ //aguarda o valor na serial. e se for 4 pausa o ensaio//
              float guardavalor;
              guardavalor = float(currentMillis - initialMillis);
              while(true){
                imprimir();
                if (Serial.available()> 0){
                  botoes = Serial.parseInt();
                  if(botoes == 2){ //aguarda o valor na serial. e se for 2 continua o ensaio de onde parou//
                    currentMillis = millis();
                    initialMillis = currentMillis-guardavalor;
                    break;
                  }
                  if(botoes == 3){ //aguarda o valor na serial. e se for 3 "para" o ensaio//
                    goto pararEnsaioDNIT135;
                  }
                }
              }
            }
          }
          if((currentMillis - initialMillis)% 5 == 0 && (currentMillis - initialMillis)!= 0){
            imprimir();
          }
          else{
            delayMicroseconds(1);
            currentMillis = millis(); //Tempo atual em ms
          }
        }/*while*/
        break;
      }/*if(condConect == 1)*/

    case 'K':
    //caso receba K (acessa o ensaio da norma DNIT...)

    //**********************************************************************************//
    //**********************************************************************************//
    //********************************* norma DNIT... **********************************//
    //**********************************************************************************//
    //**********************************************************************************//
      if(condConect == 1){
        Serial.println("Ainda falta complementar");
      }/*if(condConect == 1)*/
      
   }/*switch*/

}/*void*/

//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//

/* Imprimir dados na tela */
void imprimir(){
  ad0 = adc.read(A4);
  ad1 = adc.read(A6);
  vd0 = ad0*bit16_Voltage;
  vd1 = ad1*bit16_Voltage;
  ad2 = analogRead(A0);
  ad3 = analogRead(A2);
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
  Serial.print(vd0,4);
  Serial.print(",");
  Serial.print(vd1,4);
  Serial.print(",");
  Serial.print(vd2*3.3f);
  Serial.print(",");
  Serial.print(vd3*3.3f);
  Serial.print(",");
  Serial.print(statuS);
  Serial.print(",");
  Serial.println(nGolpe);
  //Serial.println(setpointD);
}/* Imprimir dados na tela */

//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//

/* Limpa o buffer serial */
void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}/* Limpa o buffer serial */

//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//

/* Intervalo de tempo do aplicador */
S tempo(int nTime, int frequencia, long initialMillis){
  currentMillis = millis(); //Tempo atual em ms
  switch(frequencia){
    case 1:
      if(currentMillis - initialMillis < intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
        //Serial.println(currentMillis - initialMillis);
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo09){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }      
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
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo05){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo05 && (currentMillis - initialMillis) <= intervalo05 + intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo05);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo05 + intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
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
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) < intervalo04){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo04 && (currentMillis - initialMillis) <= intervalo04 + intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo04);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo04 + intervalo01 && (currentMillis - initialMillis) <= 2*intervalo04){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo04 && (currentMillis - initialMillis) <= 2*intervalo04+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 2*intervalo04);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo04+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
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
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) <= intervalo03){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo03 && (currentMillis - initialMillis) <= intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo03);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo03+intervalo01 && (currentMillis - initialMillis) <= 2*intervalo03){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo03 && (currentMillis - initialMillis) <= 2*intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 2*intervalo03);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo03+intervalo01 && (currentMillis - initialMillis) <= 3*intervalo03){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo03 && (currentMillis - initialMillis) <= 3*intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 3*intervalo03);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo03+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
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
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo01  && (currentMillis - initialMillis) <= intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 1){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > intervalo02 && (currentMillis - initialMillis) <= intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - intervalo02);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > intervalo02+intervalo01 && (currentMillis - initialMillis) <= 2*intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 2){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo02 && (currentMillis - initialMillis) <= 2*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 2*intervalo02);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > 2*intervalo02+intervalo01 && (currentMillis - initialMillis) <= 3*intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 3){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo02 && (currentMillis - initialMillis) <= 3*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 3*intervalo02);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > 3*intervalo02+intervalo01 && (currentMillis - initialMillis) <= 4*intervalo02){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
        if(contadorG == 4){
          nGolpe++;
          contadorG++;
        }
      }
      if((currentMillis - initialMillis) > 4*intervalo02 && (currentMillis - initialMillis) <= 4*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          if(currentMillis - initialMillis < intervalo00){
            digitalWrite(pinAplicador, HIGH);  //ativa o pinAplicador
          }
          else{
            digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
          }  
        }
        if(conditionEnsaio == 1){
          i = int(currentMillis - initialMillis - 4*intervalo02);
          setpointD = waveformsTable[0][i]*setpointB+setpointC;
          analogWrite(DAC0, setpointD);
        }
      }
      if((currentMillis - initialMillis) > 4*intervalo02+intervalo01){
        if(conditionEnsaio == 0){
          digitalWrite(pinAplicador, LOW);  //desativa o pinAplicador
        }
        if(conditionEnsaio == 1){
          setpointD = setpointC;
          analogWrite(DAC0, setpointD);            
        }
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

//**********************************************************************************//
//**********************************************************************************//
//**********************************************************************************//
