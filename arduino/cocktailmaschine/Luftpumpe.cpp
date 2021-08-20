#include "Luftpumpe.hpp"
#include "Pumpe.hpp"
#include "config.hpp"

Luftpumpe::Luftpumpe(Type type, int in1, int in2, int ena, int led, int bottleLed, Ventil ventil, Drucksensor sensor, bool inverse) : Pumpe(type, in1, in2, ena, led, bottleLed, inverse)
{
  this->ventil = ventil;
  this->sensor = sensor;
}

void Luftpumpe::stop(bool ventil) {
  digitalWrite(this->in1, HIGH);
  digitalWrite(this->in2, HIGH);
  if (ventil)
  {
    this->ventil.open();
    delay(3000);
    this->ventil.close();
  }
}

void Luftpumpe::forward()
{
  this->ventil.close();
  ledstripe.fillLed(strip.Color(255, 255, 255), false);
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
void Luftpumpe::backward() {
  this->ventil.close();
  ledstripe.fillLed(strip.Color(255, 255, 255), false);
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
