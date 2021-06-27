#include "Luftpumpe.hpp"
#include "Pumpe.hpp"
#include "config.hpp"

Luftpumpe::Luftpumpe(Type type, int in1, int in2, int ena, int led, int bottleLed, Ventil ventil, bool inverse) : Pumpe(type, in1, in2, ena, led, bottleLed, inverse)
{
  this->ventil = ventil;
}

void Luftpumpe::stop() {
  digitalWrite(this->in1, HIGH);
  digitalWrite(this->in2, HIGH);
  this->ventil.open();
  delay(1000);
  this->ventil.close();
}
