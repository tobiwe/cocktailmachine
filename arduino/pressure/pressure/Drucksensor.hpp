#ifndef DRUCKSENSOR
#define DRUCKSENSOR

class Drucksensor
{
  private:
    int sensorPin;
    float pressure; 
  public:
    Drucksensor(int);
    void update();
    float getValue();
};

#endif
