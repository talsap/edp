#include <Oversampling.h>  //biblioteca de alteração da resolução
#define ADC_16BIT_MAX   65536 //valor da resolucao do arduino com Oversampling

Oversampling adc(10, 16, 2); //aumentar a resolução do adc de 10bit para 16bit

int ad0; //valor analógico do LVDT1
int ad1; //valor analógico do LVDT2
int ad4; //valor analógico do sensor de pressão (Válvula do Motor)
int ad5; //valor analógico do sensor de pressão (Válvula Dinâmica)
int nGolpe = 0; //numpero de golpes
int nTime = 0; //parte inteira do tempo
int currentMillis = 0;
int statuS = 0; //(0 ou 1)(ok ou n_ok) mado de avisar erro de pressao do aplicador
float vd0; //valor em voltagem do LVDT1
float vd1; //valor em voltagem do LVDT2
float vd4; //valor do sensor de pressão em mBar (válvula do motor)
float vd5; //valor do sensor de pressão em mBar (válvula dinâmica)
float bit16_Voltage; //Usado para a conversao de bits ~ volts
float InputRange_code = 5.0f; //valor do ImputRange 5.0V

void setup() {
  Serial.begin(9600); //velocidade da cominicacao com a porta serial
  bit16_Voltage = (InputRange_code)/(ADC_16BIT_MAX - 1); //fator de conversão bit~voltagem
}

void loop() {
  //ad0 = adc.read(A4);
  //ad1 = adc.read(A6);
  ad4 = analogRead(A0);
  ad5 = analogRead(A2);
  vd0 = ad0*bit16_Voltage;
  vd1 = ad1*bit16_Voltage;
  vd4 = ad4; //mbar
  vd5 = ad5; //mbar
  
  Serial.print(float(nTime)+float(currentMillis)/1000, 3); //temp
  Serial.print(",");
  //Serial.print(ad0);         //y1
  //Serial.print(",");
  //Serial.print(ad1);         //y2
  Serial.print(",");
  Serial.print(vd0,4);       //y1v
  Serial.print(",");
  Serial.print(vd1,4);       //y2v
  Serial.print(",");
  Serial.print(vd4,4);       //motor
  Serial.print(",");
  Serial.print(vd5,4);       //dinamica
  Serial.print(",");
  Serial.print(statuS);      //sts
  Serial.print(",");
  Serial.println(nGolpe);    //glp
  //delay(1);
  currentMillis = currentMillis + 10;
  if(currentMillis > 999){
    currentMillis = 0;
    nTime ++;
  }

}
