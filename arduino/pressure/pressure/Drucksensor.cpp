#include "Drucksensor.hpp"
#include "Arduino.h"

Drucksensor::Drucksensor(int pin)
{
  this->sensorPin = pin;
  this->pressure = 0;
  
}

void Drucksensor::update()
{
  int rawValue; // A/D readings
  int offset = 410; // zero pressure adjust
  int fullScale = 9630; // max pressure (span) adjust

  rawValue = 0;
  for (int x = 0; x < 10; x++) rawValue = rawValue + analogRead(this->sensorPin);
  this->pressure = (rawValue - offset) * 700.0 / (fullScale - offset); // pressure conversion
}

float Drucksensor::getValue()
{
  return this->pressure;
}
