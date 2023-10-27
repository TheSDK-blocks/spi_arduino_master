//int x;
//int y;
//char in_mem;//[3];
void setup() {
 Serial.begin(115200);
 //Serial.setTimeout(1);
 
  
    uint8_t port = digitalPinToPort(SS);
    uint8_t bit = digitalPinToBitMask(SS);
    volatile uint8_t *reg = portModeRegister(port);
    if(!(*reg & bit)){
      digitalWrite(SS, HIGH);
    }

    pinMode(SS, OUTPUT);// pin 10
    pinMode(SCK, OUTPUT);// pin 13
    pinMode(MOSI, OUTPUT);// pin 11
    pinMode(MISO, INPUT); // pin 12
    
    
    
    
  
  
}
void loop() {
 while (!Serial.available());
 //int x = Serial.readBytes(in_mem,1);
 //long int t1=micros(); 
 char x1=Serial.read();
 //char x2=Serial.read();
 //char x3=Serial.read();
 //byte x=()in_mem;
 //Serial.println(bitRead(x1,0));
 //Serial.println(bitRead(x1,1));
 //Serial.println(bitRead(x1,2));
 //Serial.println(int(in_mem));
 //Serial.println(int(in_mem[1]));
 //Serial.println(int(in_mem[2]));
 //Serial.println("\n");
 //Serial.println(*in_mem);
 
 digitalWrite(SS, bitRead(x1,0));
 digitalWrite(SCK, bitRead(x1,2));
 digitalWrite(MOSI, bitRead(x1,1));
 Serial.print(digitalRead(MISO));
 //long int t2=micros();
 //Sierial.println(t2-t1);
 //char t='123';
 //Serial.println(t);
 //Serial.println("\n");
 //int y=in_mem[0].toInt();
 //Serial.println(y);
 //Serial.println(x + 1);
	
}
