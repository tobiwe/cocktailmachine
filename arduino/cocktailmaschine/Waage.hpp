#ifndef WAAGE
#define WAAGE

#include <HX711_ADC.h>
#include <EEPROM.h>

class Waage
{
  public:
    void setup();
    float getValue();
    void calibrate();
};

#endif


