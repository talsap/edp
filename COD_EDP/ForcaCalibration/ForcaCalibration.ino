const int pinA = 12; //pino 12
const int pinB = 7; //pino 7
int setpoint2; //Valor de entrada para o setpoint2 em milibar (0 - 10.000)mBar
int botoes; //botoes
int ad5; //ad5
int condicao = 0; //condicao para continuar mostrando valores da válvula dinâmica
float AD1 = 2.0119;  //valor da A da calibração da válvula dinâmica AD2 para mBar (output)
float BD1 = 38.21; //valor de B da calibração da válvula dinâmica AD2 para mBar (output)
float AD2 = 1.361;  //valor da A da calibração da válvula dinâmica mBar para DAC (input)
float BD2 = -14.258; //valor de B da calibração da válvula dinâmica mBar para DAC (input)
float setpointD; //Valor do setpointD
float vd5; //valor do sensor de pressão em mBar (válvula dinâmica)
unsigned char conexao;  //conexao

void setup() {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  analogReadResolution(12); //Altera a resolucao para 12bits (apenas no arduino DUE)
  analogWriteResolution(12); //Altera a resolucao de escrita para 12bits (apenas no arduino DUE)
  analogReference(AR_DEFAULT); //Define a tensao de 3.3Volts como sendo a padrao (apenas no arduino DUE)
  analogWrite(DAC1, 0); //pino responsavel em alterar a pressao no (regulador de pressão proporcional)
  pinMode(pinA, OUTPUT);  //configura o pinA
  pinMode(pinB, OUTPUT);  //configura o pinB
  digitalWrite(pinA, LOW); //inicia desativado o pinA
  digitalWrite(pinB, LOW); //inicia ativado o pinB 
}

void loop() {
  conexao:
  conexao = Serial.read();

  switch(conexao){
    case 'E':
      Serial.println("DINAMICA");
      while(true){
        if (Serial.available()>1){
          setpoint2 = Serial.parseInt();    //valor em mbar
          if(setpoint2 > 10){
            setpointD = int(setpoint2*AD2+BD2);   //valor em contagem
            analogWrite(DAC1, setpointD);
            Serial.print("CHEGOU=");
            Serial.print(setpoint2);
            Serial.print("/SENSOR=");
            ad5 = analogRead(A2);
            vd5 = ad5*AD1+BD1; //mbar
            Serial.println(vd5);
            condicao = 1;
          }
          if(setpoint2 == 3){
            condicao = 0;
            goto conexao;
          }
        }
        if (condicao == 1){
           delay(100);
           ad5 = analogRead(A2);
           vd5 = ad5*AD1+BD1; //mbar
           Serial.println(vd5);
        }
      }
      break;
    
    case 'a': //abri as válvulas
      digitalWrite(pinA, HIGH);  //ativa o pinA
      digitalWrite(pinB, LOW);  //ativa o pinB
      break;
    
    case 'f': //fecha as válvulas
      digitalWrite(pinA, LOW);  //desativa o pinA
      digitalWrite(pinB, HIGH);  //desativa o pinB
      break;
  
  }/*end switch*/
}/*end loop*/
