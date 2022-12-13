#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

int led = 13;
int led1 = 2;
int led2 = 4;
int led3 = 7;

int input;

/// lcd의 플리커 현상을 방지하기 위한 변수
int done1 = 0;
int done2 = 0;
int done3 = 0;

void setup()
{
  Serial.begin(9600);
  
  lcd.begin();
	lcd.backlight();

  pinMode(led, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);

  lcd.print("POWER ON");
}

void loop()
{
  while(Serial.available()) input = Serial.read();

  if(input == '0'){

    /// led 1개 점등
    digitalWrite(led1,HIGH);
    digitalWrite(led2,LOW);
    digitalWrite(led3,LOW);

    done2 = 0;
    done3 = 0;
    
    /// first set 표시
    if(done1 == 0){
      lcd.clear();
      lcd.setCursor(4,0);
      lcd.print("First Set");
      done1 = 1;
    }
  }
  if(input == '1'){
    /// led 2개 점등

    digitalWrite(led1,HIGH);
    digitalWrite(led2,HIGH);
    digitalWrite(led3,LOW);

    done1 = 0;
    done3 = 0;
    
    /// second set 표시
    if(done2 == 0){
      lcd.clear();
      lcd.setCursor(4,0);
      lcd.print("Second Set");
      done2 = 1;
    }
  }
  if(input == '2'){
    /// led 3개 점등
    digitalWrite(led1,HIGH);
    digitalWrite(led2,HIGH);
    digitalWrite(led3,HIGH);

    done1 = 0;
    done2 = 0;
    
    /// last set 표시
    if(done3 == 0){
      lcd.clear();
      lcd.setCursor(4,0);
      lcd.print("Last Set");
      done3 = 1;
    }
  }

}