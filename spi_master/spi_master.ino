//int x;
//int y;
//char in_mem;//[3];
void setup() {
 
 Serial.begin(9600);
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
// Implementation compatible with SDK spi_slave controller generated files
//void loop() {
// while (!Serial.available());
// //int x = Serial.readBytes(in_mem,1);
// //long int t1=micros(); 
// char x1=Serial.read();
// //char x2=Serial.read();
// //char x3=Serial.read();
// //byte x=()in_mem;
// //Serial.println(bitRead(x1,0));
// //Serial.println(bitRead(x1,1));
// //Serial.println(bitRead(x1,2));
// //Serial.println(int(in_mem));
// //Serial.println(int(in_mem[1]));
// //Serial.println(int(in_mem[2]));
// //Serial.println("\n");
// //Serial.println(*in_mem);
// 
// digitalWrite(SS, bitRead(x1,0));
// digitalWrite(SCK, bitRead(x1,2));
// digitalWrite(MOSI, bitRead(x1,1));
// Serial.print(digitalRead(MISO));
// //long int t2=micros();
// //Sierial.println(t2-t1);
// //char t='123';
// //Serial.println(t);
// //Serial.println("\n");
// //int y=in_mem[0].toInt();
// //Serial.println(y);
// //Serial.println(x + 1);
//	
//}


const int freq=1;
 const  unsigned long step_time=((1/freq)/2)*pow(10,6);
 const float conf_len=27;
 const int bytes_num=ceil(conf_len/8);
 const int leftover=8-(bytes_num*8-conf_len);
 byte conf_array[bytes_num];
 byte mon_array[bytes_num];
int currentState =0;

// Implementation for arbitrary SPI master 
void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'w') {
      currentState = 1;
    } else if (command == 'p') {
      currentState = 2;
    } else {
      currentState = 0; // Return to the "doing nothing" state if an unknown command is received
    }
  }

  // State machine
  switch (currentState) {
    case 0: // Doing nothing
      break;
    case 1: // "w" state
      //Serial.println(char('w'));
      //Serial.println(conf_len);
      //Serial.println(bytes_num);
      writeStringToArduino();
      break;
    case 2: // "p" state
      //Serial.println(char('p'));
      readWriteData();
      break;
    default:
      break;
  }
}

void writeStringToArduino() {
  
    //Serial.println(char('z'));
    while(Serial.available() <1){}
    
    for (int i = 0; i < bytes_num; i++) {
      //Serial.println(i);
      while(Serial.available() <1){}
      if (Serial.available() >0) {
        //Serial.println('y');
        conf_array[i] = byte(Serial.read());
        Serial.read();
        delay(100);
      }
    currentState = 0; // Return to the "doing nothing" state
    Serial.write(conf_array[0]);
    Serial.write(conf_array[1]);
    Serial.write(conf_array[2]);
    Serial.write(conf_array[3]);
  }
}

void readWriteData() {
  
  for (int i = 0; i < bytes_num; i++) {
    //Serial.println(char('x'));
    char currentChar = conf_array[i];
    for (int bitIdx = 0; bitIdx < 8; bitIdx++) {
      // Extract the current bit from the character
      if (!(i == bytes_num-1 && bitIdx == leftover)) {
        int currentBit = (currentChar >> bitIdx) & 0x01;
        delayMicroseconds(step_time);
        //delayMicroseconds(1000000);
        
        //delay(100);
        //Serial.println(currentBit);
        digitalWrite(MOSI, currentBit); 
        //digitalWrite(MOSI, 1);
        digitalWrite(SCK, 1);
        //delay(10);
        mon_array[i] |= (digitalRead(MISO) == HIGH) << bitIdx; 
        delayMicroseconds(step_time);
        //delayMicroseconds(1000000);
        //delay(100);
        digitalWrite(SCK, 0);
        
      }
    }
  }
  digitalWrite(SCK, 0);
  digitalWrite(MOSI, 0);
  //mon_array[bytes_num] |= (digitalRead(MISO) == HIGH) << 7;
  // Send array2 to Python
  delay(1000);
  Serial.write(char('a'));
  for (int i = 0; i < bytes_num; i++) {
    Serial.write(mon_array[i]);
    delay(100);
    while(Serial.available() <1){}
    Serial.read();
    //Serial.println(char('b'));
  }
  for (int i = 0; i < bytes_num; i++) {
    Serial.write(conf_array[i]);
    Serial.write(mon_array[i]);
    delay(100);
  }
  currentState = 0; // Return to the "doing nothing" state
}

