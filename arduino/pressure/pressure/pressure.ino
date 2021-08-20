#include "Drucksensor.hpp"
#define SERIAL Serial

Drucksensor mySensor(A0);
 
void setup() {
  SERIAL.begin(9600);
}
 
void loop() {
  mySensor.update(); 
  SERIAL.print("   Pressure is  ");
  SERIAL.print(mySensor.getValue(),1); // one decimal places
  SERIAL.println("  kPa");
  delay(1000);
}
