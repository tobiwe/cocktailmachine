#ifndef WAAGE
#define WAAGE

#include <HX711_ADC.h>
#include <EEPROM.h>

class Waage
{
  private:
    float currentValue;
  
  public:
    void setup();
    bool update();
    float getValue();
    void calibrate();
    void tare();
};

#endif


