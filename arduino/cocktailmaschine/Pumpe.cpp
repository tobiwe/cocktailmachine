#include "Pumpe.hpp"
#include "Arduino.h"
#include "config.hpp"
#include "Led.hpp"


Pumpe::Pumpe(Type type, int in1, int in2, int ena, int led, int bottleLed, bool inverse)
{
  this->type = type;
  this->in1 = in1;
  this->in2 = in2;
  this->ena = ena;
  this->led = led;
  this->bottleLed = bottleLed;
  this->inverse = inverse;
}

void Pumpe::setup()
{
  pinMode(this->in1, OUTPUT);
  pinMode(this->in2, OUTPUT);
  pinMode(this->ena, OUTPUT);
}
void Pumpe::setSpeed(int motorSpeed)
{
  analogWrite(this->ena, motorSpeed);
}
void Pumpe:: forward()
{
  ledstripe.setLed(this->led, strip.Color(0, 0, 255));
  if (!this->isInverse())
  {
    digitalWrite(this->in1, LOW);
    digitalWrite(this->in2, HIGH);
  }
  else
  { digitalWrite(this->in1, HIGH);
    digitalWrite(this->in2, LOW);

  }
}
void Pumpe:: backward() {
  ledstripe.setLed(this->led, strip.Color(0, 0, 255));

  if (!this->isInverse())
  {
    digitalWrite(this->in1, HIGH);
    digitalWrite(this->in2, LOW);
  }

  else
  {
    digitalWrite(this->in1, LOW);
    digitalWrite(this->in2, HIGH);
  }
}
void Pumpe::stop() {
  ledstripe.setLed(this->led, strip.Color(0, 0, 0));
  digitalWrite(this->in1, HIGH);
  digitalWrite(this->in2, HIGH);
}

bool Pumpe::isInverse()
{
  if (this->inverse == true)
  {
    return true;
  }
  return false;
}

Type Pumpe::getType()
{
  return this->type;
}


