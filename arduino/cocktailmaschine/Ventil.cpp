#include "Ventil.hpp"
#include "Arduino.h"

Ventil::Ventil()
{
}

Ventil::Ventil(int ventil)
{
  this->ventil = ventil;
}

void Ventil::setup()
{
  pinMode(this->ventil, OUTPUT);
}

void Ventil::open()
{
  digitalWrite(this->ventil, LOW);
}


void Ventil::close()
{
  digitalWrite(this->ventil, HIGH);
}
