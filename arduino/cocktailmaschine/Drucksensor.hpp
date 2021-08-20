#ifndef DRUCKSENSOR
#define DRUCKSENSOR

class Drucksensor
{
  private:
    int sensorPin;
    float pressure;
    float defaultPressure;
    
  public:
    Drucksensor();
    Drucksensor(int);
    void update();
    float getValue();
    void setDefaultPressure(float);
    float getDefaultPressure();
};

#endif
