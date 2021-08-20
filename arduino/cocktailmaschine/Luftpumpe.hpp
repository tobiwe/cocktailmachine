#ifndef LUFTPUMPE
#define LUFTPUMPE
#include "config.hpp"
#include "Pumpe.hpp"
#include "Ventil.hpp"
#include "Drucksensor.hpp"
#include "Arduino.h"


class Luftpumpe : public Pumpe
{
  public:
    Drucksensor sensor;
    Ventil ventil;
    Luftpumpe (Type, int, int, int, int, int, Ventil, Drucksensor, bool);
    void stop(bool ventil=true);
    void forward();
    void backward();
};

#endif
