#ifndef PUMPE
#define PUMPE
#include "config.hpp"
#include "Led.hpp"

extern Led ledstripe;

class Pumpe
{
  protected:
    Type type;
    int in1;
    int in2;
    int ena;
    bool inverse;

  public:
    int led;
    int bottleLed;
    Pumpe(Type, int, int, int, int, int, bool);
    void setup();
    void setSpeed(int);
    void virtual forward();
    void virtual backward();
    void virtual stop();
    bool isInverse();
    Type getType();
};

#endif
