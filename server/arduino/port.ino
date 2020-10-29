///////////////////////////////////////////////////////////
//          Asunto: Mercury Challenge 2019               //
//          Script: Controlador Esclavo (Motores)        //
//          Autor:  Cristian F Rubio A.                  //
//                                                       //
///////////////////////////////////////////////////////////

#include <Servo.h>
#include <Wire.h>

#define MAX_SIGNAL 2000
#define MIN_SIGNAL 1000
#define MOTOR_PIN1 12

Servo Recolector;

String inString = "";    
int inChar = 0;          
int avanzar;       
int girar; 
int vueltear;     
int save_as_second = false; 
int data;
int pwm1, pwm2, x, y;
float tic,toc,delta;

void setup() {
  Serial.begin(115200);     
  for (int j=4;j<=9;j++){
    pinMode(j,1);
    digitalWrite(j,0);
  }
  
  Recolector.attach(MOTOR_PIN1);               // Disparador ...
  Recolector.writeMicroseconds(MAX_SIGNAL);    
  delay(3000);
  calibration();                               //           \\...
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

      
      avanzar = avanzar - 80;           
      girar = girar - 80;
      
      pwm1 = avanzar + girar;
      pwm2 = avanzar - girar;

      
// Limitando ------------------------------------------------------------
  
      if(pwm1 > 80){
        pwm1 = 80;    
      }
      
      if(pwm1 < -80){
        pwm1 = -80;
      }
      
      if(pwm2 > 80){
        pwm2 = 80;    
      }
      
      if(pwm2 < -80){
        pwm2 = -80;
      }

// Boost -----------------------------------------------------------------

    if(vueltear == 1){
      
       pwm1 = pwm1 * 2;
       pwm2 = pwm2 * 2;
       
    }
      
// -----------------------------------------------------------------------
      
      if(pwm1 < 0){
        x = abs(pwm1);
        analogWrite(5,x);
        FMI();
      }
     
      if(pwm1 > 2){
        analogWrite(5,pwm1);
        RMI();
      }
      
      if(pwm2 < 0){
        y = abs(pwm2);
        analogWrite(6,y);
        FMD();
      }

      if(pwm2 > 2){
        analogWrite(6,pwm2);
        RMD();
      }
      
      if(pwm1 == 0){
        if(pwm2 == 0)
          Stop();
        }

      if(avanzar == 1){
      Recolector.attach(MOTOR_PIN1);
      Recolector.writeMicroseconds(2000);
    }

    if(avanzar == 2){
      Recolector.attach(MOTOR_PIN1);
      Recolector.writeMicroseconds(1000);
    }
    
  }
   
 }
  
}

void FMI(){
  digitalWrite(7,0); 
  digitalWrite(8,1);
}

void RMI(){
  digitalWrite(7,1); 
  digitalWrite(8,0);
}

void FMD(){
  digitalWrite(4,0); 
  digitalWrite(9,1);
}

void RMD(){
  digitalWrite(4,1); 
  digitalWrite(9,0);
}

void Stop(){
  digitalWrite(7,0); 
  digitalWrite(8,0);
  digitalWrite(4,0);
  digitalWrite(9,0);
}

void calibration(){
  Recolector.writeMicroseconds(MIN_SIGNAL);
  delay(2000);
  }
