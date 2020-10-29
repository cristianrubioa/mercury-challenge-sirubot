///////////////////////////////////////////////////////////
//          Asunto: Mercury Challenge 2019               //
//          Script: Controlador Esclavo (Motores)        //
//          Autor:  Cristian F Rubio A.                  //
//                                                       //
///////////////////////////////////////////////////////////

// 8 & 9 Motores y Cooler             |            |
//                                    | Disparador |
//                                    |            |
// 6 & 7 
// 13 Servo inclinacion
// 4 & 5 MPU6050
// Camara 2 & 3

#include <Servo.h>

Servo Disparador;
Servo CamGiroH;
Servo CamGiroV;

String inString = "";    
int inChar = 0;          
int avanzar;       
int girar;    
int vueltear;  
int save_as_second = false; 
int data;
float tic,toc,delta;
int conV = 135;
int conH = 120;
float valV = 135.0;
float valH = 120.0;
float sum = 0.1;
float mpu = 30;
float valor2;
float valor3;
float valor;

void setup() {
  Serial.begin(115200);    
  for (int j=8;j<=12;j++){
    pinMode(j,1);
    digitalWrite(j,0);
  }
  pinMode(2,0);
  pinMode(0,0);
  
 
 
  Disparador.detach();   // Servo Disparador
  CamGiroV.attach(2);
  CamGiroV.write(valV);
  CamGiroH.attach(3);
  CamGiroH.write(valH);
}


void loop() {
   if (Serial.available()) {  
    inChar = Serial.read(); 
    inString += char(inChar);
  
    
    if (inChar == ',') {
      if (save_as_second == false) {
        avanzar = inString.toInt(); 
        inString = "";              
        save_as_second == true;     
      }
    }
    
    if (inChar == ';') {     
      girar = inString.toInt();
      inString = "";       
      save_as_second = false;
    }

    if (inChar == ':') {     
      vueltear = inString.toInt();
      inString = "";       
      save_as_second = false;

      
    if(avanzar == 91){
      
      digitalWrite(8,1);   
      digitalWrite(9,0); 
    }

    if(avanzar == 92){
      
      digitalWrite(8,0);   
      digitalWrite(9,0);
    }

    if(vueltear == 1){

    if(avanzar == 90){
      Disparador.detach(); 
      digitalWrite(LED_BUILTIN,1);
    }

    if(avanzar > 96){
      valor3 = analogRead(0);
      Serial.println(valor3);
      valor = (5/1023)*valor3;
      Serial.println(valor);
      if(valor3 <= 4 ){
        Disparador.attach(13);
        Disparador.write(0); 
        
      }
      if(valor3 > 4 ){
        Disparador.detach();

      }
      

    }


    if(avanzar < 89){
      valor2 = analogRead(2);
      valor2 = (5/1023)*valor2;
      if(valor2 <= 4){
        Disparador.attach(13);
        Disparador.write(180); 
      }
      if(valor2 > 4 ){
        Disparador.detach();
      }
    }
    
   }
///// Vertical

    if(vueltear == 0){

     if(avanzar > 96){
      
      CamGiroV.attach(2);
      valV = valV + sum;
      conV = valV;
      if(conV > 180)
      {
        conV = 180;
        valV = 180;
        }
      CamGiroV.write(conV);
      }


      if(avanzar < 89){
      
      CamGiroV.attach(2);
      valV = valV - sum;
      conV = valV;
      if(conV < 110)
      {
        conV = 110;
        valV = 110;
        }
      CamGiroV.write(conV);
      }
      

///// Horizontal

     if(girar > 96){
      
      CamGiroH.attach(3);
      valH = valH - sum;
      conH = valH;
      if(conH < 90)
      {
        conH = 90;
        valH = 90;
        }
      CamGiroH.write(conH);
      }


      if(girar < 89){
      
      CamGiroH.attach(3);
      valH = valH + sum;
      conH = valH;
      if(conH > 150)
      {
        conH = 150;
        valH = 150;
        }
      CamGiroH.write(conH);
      }

    }
      
//////////////

      if(avanzar == 89){
         valV = 135;
         valH = 120;
         CamGiroV.attach(2);
         CamGiroV.write(valV);
         CamGiroH.attach(3);
         CamGiroH.write(valH);
      }

  }
   
 }
  
}
