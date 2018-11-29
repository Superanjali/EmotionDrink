// the setup function runs once when you press reset or power the board

#define PIN1 7
#define PIN2 8
#define PIN3 9 

#define KEY1 49
#define KEY2 50
#define KEY3 51

void setup() { 
  Serial.begin(9600);
  pinMode(PIN1, OUTPUT);
  pinMode(PIN2, OUTPUT);
  pinMode(PIN3, OUTPUT);
  digitalWrite(PIN1, HIGH);
  digitalWrite(PIN2, HIGH);
  digitalWrite(PIN3, HIGH);
}
void command_relay(int key,int pin, int digit){
  if (digit == key) {  
    digitalWrite(pin, LOW);   
    delay(4000);                       
    digitalWrite(pin, HIGH); 
  }
}

// the loop function runs over and over again forever
void loop() {
  if (Serial.available()) {
    char digit = Serial.read();   // Read one byte from serial buffer
  command_relay(KEY1,PIN1,digit);
  command_relay(KEY2,PIN2,digit);
  command_relay(KEY3,PIN3,digit);
  }
  delay(2);                     // Let the serial buffer catch its breath.                      
 }