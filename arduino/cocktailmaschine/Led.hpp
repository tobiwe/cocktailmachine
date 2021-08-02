#ifndef LED
#define LED

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

extern Adafruit_NeoPixel strip;

class Led
{
  public:
    void setup();
    void setLed(int, uint32_t);
    void fillLed(uint32_t);
    void theaterChaseRainbow(int wait);
    void fasterTheaterChaseRainbow(int wait);
    void rainbow(int wait);
    void theaterChase(uint32_t color, int wait);
    void colorWipe(uint32_t color, int wait);
    void blinkOnOff(uint32_t color, int wait);
    void fasterBlinkOnOff(uint32_t color, int wait);
};

#endif
