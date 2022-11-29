char cmd;
int led1 = 13;
int led2 = 12;
int led3 = 11;
char work_set = 0;

void setup() {
  Serial.begin(9600);
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
}

void loop() {
  if(Serial.available()){
    cmd = Serial.read();

    if(cmd == 'a'){
      Serial.println("1set");
      digitalWrite(led1,HIGH);
      delay(100);
    }
    else if(cmd == 'b'){
      Serial.println("2set");
      digitalWrite(led2,HIGH);
      delay(100);
    }
    else if(cmd == 'c'){
      Serial.println("3set");
      digitalWrite(led3,HIGH);
      delay(100);
    }
    else if(cmd == 'd'){
      
      Serial.println("End");
      digitalWrite(led1,LOW);
      digitalWrite(led2,LOW);
      digitalWrite(led3,LOW);
      delay(100);
    }
    else Serial.println("fail");
  }
}
