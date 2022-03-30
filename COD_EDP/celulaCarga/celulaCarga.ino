#define num 5 //número de iterações da média móvel
#define porta A0 //porta analógica A0

int values[num]; //vetor que armazena os valores para o cálculo da média móvel
int taraVetor[num]; //vetor tara
int botoes; //botoes
int ad0; //ad0
int nTime = -1; //parte inteira do tempo
float filtro; //valor analógico filtrado
float peso; //peso
float tara = 0; //tara
float calc_peso(float valor);  // função de cálculo do peso
long taraAcc = 0; //tara acumulado
long moving_average(int sig); //função de cálculo do filtro média móvel
unsigned long currentMillis; //variacao do tempo em milisegundos
unsigned long initialMillis; //tempo incial dinamico
unsigned char conexao;  //conexao

void setup() {
  Serial.begin(115200); //velocidade da cominicacao com a porta serial
  pinMode(porta, INPUT); //difinindo o pino porta como entrada
}

void loop() {
  conexao:
  conexao = Serial.read();

  switch(conexao){
    case 'a':
      currentMillis = millis(); //Tempo atual em ms
      initialMillis = currentMillis;  //Tempo inicial
      while(true){
        if (Serial.available()> 0){ //aguarda o valor na serial e se for 3 "para" o ensaio//
          botoes = Serial.parseInt();
          if(botoes == 3){
            nTime = 0;
            goto conexao;
          }
          if(botoes == 4){ //aguarda o valor na serial. e se for 4 pausa o ensaio//
            float guardavalor;
            guardavalor = float(currentMillis - initialMillis);
            while(true){
              if (Serial.available()> 0){
                botoes = Serial.parseInt();
                if(botoes == 2){ //aguarda o valor na serial. e se for 2 continua o ensaio de onde parou//
                  currentMillis = millis();
                  initialMillis = currentMillis-guardavalor;
                  break;
                }
                if(botoes == 3){ //aguarda o valor na serial. e se for 3 "para" o ensaio//
                  goto conexao;
                }
              }
            }
          }
        }
        if((currentMillis - initialMillis)% 10 == 0 && (currentMillis - initialMillis)!= 0){
          ad0 = analogRead(porta);
          filtro = moving_average(ad0);
          peso = calc_peso(filtro);
          Serial.print(float(nTime)+float(currentMillis - initialMillis)/1000, 3); //temp
          Serial.print("-");
          Serial.println(peso-tara, 3); //peso
        }
        if((currentMillis - initialMillis) >= 1000){
          initialMillis = currentMillis; //Salva o tempo atual como sendo o inicial
          nTime++;
        }
        else{
          delayMicroseconds(1);
          currentMillis = millis(); //Tempo atual em ms
        }
      }
      break;
    case 't':
      for(int j = 0; j < num; j++){
        ad0 = analogRead(porta);
        peso = calc_peso(ad0);
        taraVetor[j] = peso;
        delayMicroseconds(1);
      };
      for(int j = 0; j < num; j++) taraAcc += taraVetor[j];
      tara = taraAcc/num;
      Serial.print("Tara = ");
      Serial.println(tara, 3); //tara
      break;
  }/*end switch*/
}/*end loop*/

/*funcao onde calcula o peso*/
float calc_peso(float valor){
  float p;
  if(valor <= 95){
    p = 1.3334*valor - 46.667;
  }
  else{
    p = 1.3334*valor - 46.667;
  }
  return p; //retorna o peso p
}/*end função calcular peso*/

/*filtro Média Móvel*/
long moving_average(int sig){
  int i;        //variável auxiliar para iterações
  long acc = 0; //acumulador
  
  //desloca o vetor completamente eliminando o valor mais antigo
  for(i = num; i > 0; i--) values[i] = values[i-1];
  
  values[0] = sig; //carrega o sinal no primeiro elemento do vetor
  
  for(i = 0; i < num; i++) acc += values[i]; //faz o somatório dos valores
  
  return acc/num;  //retorna a média móvel

}//end Média Móvel
