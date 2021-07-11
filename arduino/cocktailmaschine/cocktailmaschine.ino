#include "Waage.hpp"
#include "pumpe.hpp"
#include "Luftpumpe.hpp"
#include "Led.hpp"
#include "Ventil.hpp"
#include "config.hpp"

int peristalicLed[6] = { 5, 4, 3, 2, 1, 0};
int airLed[4] = { 11, 11, 11, 11};
int bottleLed[6] = {6, 7, 8, 9, 10, 11};
int glasLed = 12;

Waage waage;
Led ledstripe;

Ventil ventile[4] = {
  Ventil(VENTIL1),
  Ventil(VENTIL2),
  Ventil(VENTIL3),
  Ventil(VENTIL4)
};


Pumpe p1(PERISTALIC, MOTOR1_In1, MOTOR1_In2, MOTOR1_En, peristalicLed[0], bottleLed[0], false);
Pumpe p2(PERISTALIC, MOTOR2_In1, MOTOR2_In2, MOTOR2_En, peristalicLed[1], bottleLed[1], false);
Pumpe p3(PERISTALIC, MOTOR3_In1, MOTOR3_In2, MOTOR3_En, peristalicLed[2], bottleLed[2], true);
Pumpe p4(PERISTALIC, MOTOR4_In1, MOTOR4_In2, MOTOR4_En, peristalicLed[3], bottleLed[3], true);
Pumpe p5(PERISTALIC, MOTOR5_In1, MOTOR5_In2, MOTOR5_En, peristalicLed[4], bottleLed[4], false);
Pumpe p6(PERISTALIC, MOTOR6_In1, MOTOR6_In2, MOTOR6_En, peristalicLed[5], bottleLed[5], true);
Luftpumpe a1(AIR, MOTOR7_In1, MOTOR7_In2, MOTOR7_En, airLed[0], airLed[0], ventile[0], false);
Luftpumpe a2(AIR, MOTOR8_In1, MOTOR8_In2, MOTOR8_En, airLed[1], airLed[1], ventile[1], false);
Luftpumpe a3(AIR, MOTOR9_In1, MOTOR9_In2, MOTOR9_En, airLed[2], airLed[2], ventile[2], false);
Luftpumpe a4(AIR, MOTOR10_In1, MOTOR10_In2, MOTOR10_En, airLed[3], airLed[3], ventile[3], false);

Pumpe *pumpen[10] = {&p1, &p2, &p3, &p4, &p5, &p6, &a1, &a2, &a3, &a4};

void setup() {

  Serial.begin(BAUDRATE);
  waage.setup();

  for (Pumpe *p : pumpen)
  {
    p->setup();
    if (p->getType() == PERISTALIC)
    {
      p->setSpeed(255);
    }
    else
    {
      p->setSpeed(255);
    }
  }

  for (Ventil v : ventile)
  {
    v.setup();
    v.open();
    delay(10);
    v.close();
    delay(10);
  }

  ledstripe.setup();
}

void loop() {
  int zaehler = 0;
  char command[20];
  bool newSerialEvent = false;

  waage.update();

  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == 0x02) {
      zaehler = 0;
    }
    else if (inChar == 0x03) {
      newSerialEvent = true;
      command[zaehler] = '\0';
    }
    else {
      command[zaehler] = inChar;
      zaehler++;
    }
  }

  if (newSerialEvent)
  {
    int program = getValue(command, ' ', 0);
    float amount, mass;
    int motor, motorSpeed, ventil, state, pumpe, ledShow, wait, r, g, b, sub;
    switch (program)
    {
      case 1:
        ledstripe.setLed(getValue(command, ' ', 1), strip.Color(getValue(command, ' ', 2), getValue(command, ' ', 3), getValue(command, ' ', 4)));
        break;
      case 2:
        motor = getValue(command, ' ', 1);
        motorSpeed = getValue(command, ' ', 2);
        if (motorSpeed == 0) {
          pumpen[motor]->stop();
        }
        else if (motorSpeed > 0) {
          pumpen[motor]->setSpeed(motorSpeed);
          pumpen[motor]->forward();
        }
        else if (motorSpeed < 0) {
          pumpen[motor]->setSpeed(-1 * motorSpeed);
          pumpen[motor]->backward();
        }
        break;
      case 3:
        ventil = getValue(command, ' ', 1);
        state = getValue(command, ' ', 2);
        if (state == 1)ventile[ventil].open();
        else if (state == 0) ventile[ventil].close();
        break;
      case 4:
        pumpe = getValue(command, ' ', 1);
        amount = getValue(command, ' ', 2);
        fillGlas(pumpen[pumpe - 1], amount);
        break;
      case 5:
        sub =  getValue(command, ' ', 1);
        if (sub == 1)
        {
          Serial.write(0x02);
          Serial.print(waage.getValue());
          Serial.write(0x03);
        }

        else if (sub == 2)
        {
          waage.tare();
        }

        else if (sub == 3)
        {
          mass = getValue(command, ' ', 2);
          waage.calibrate(mass);
        }

        else if (sub == 4)
        {
          waage.calibrate();
        }

        break;
      case 6:
        ledShow = getValue(command, ' ', 1);

        if (ledShow == 1)
        {
          wait = getValue(command, ' ', 2);
          ledstripe.rainbow(wait);
        }

        else if (ledShow == 2)
        {
          wait = getValue(command, ' ', 2);
          ledstripe.theaterChaseRainbow(wait);

        }

        else if (ledShow == 3)
        {
          wait = getValue(command, ' ', 2);
          r = getValue(command, ' ', 3);
          g = getValue(command, ' ', 4);
          b = getValue(command, ' ', 5);
          ledstripe.theaterChase(strip.Color(r, g, b), wait);
        }

        else if (ledShow == 4)
        {
          wait = getValue(command, ' ', 2);
          r = getValue(command, ' ', 3);
          g = getValue(command, ' ', 4);
          b = getValue(command, ' ', 5);
          ledstripe.colorWipe(strip.Color(r, g, b), wait);
        }
        break;
      default:
        //do nothing
        break;
    }
  }

  delay(100);

  // demo();
}

float getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }

    String sub = data.substring(strIndex[0], strIndex[1]);
    return found > index ? sub.toFloat() : 0;
}

/**
   Filling the glas with a test gin Tonic
*/
void demo()
{
  /*
      Pumpe 1: Perstialic - Gin  5cl //40% alkohol = 50 * (60*1+40*0,8)/100 = 46g
      Pumpe 2: Air - Tonic Vater 16cl = 160g
      Led Pumpe: persitalicLed [0]
      Led Bottle: bottleLed [0]
      glasLed
  */

  Serial.println("Let's start, give me your glass!");

  while (waage.getValue() < 100) {
    //Blink glas white
    ledstripe.setLed(glasLed, strip.Color(255, 255, 255));
    delay(500);
    ledstripe.setLed(glasLed, strip.Color(0, 0, 0));
    delay(500);

  }

  //Start with Gin
  Serial.println("Starting with Gin!");
  fillGlas(pumpen[0], 46);
  Serial.println("Finished with Gin!");

  //Continue with tonic water
  Serial.println("Starting with Tonic Water!");
  fillGlas(pumpen[6], 160);
  Serial.println("Finished with Tonic Water!");

  Serial.println("Finished! Enjoy your drink!");

  while (waage.getValue() > 100)
  {
    //Blink glas green
    ledstripe.setLed(glasLed, strip.Color(0, 255, 0));
    delay(500);
    ledstripe.setLed(glasLed, strip.Color(0, 0, 0));
    delay(500);
  }
}

void fillGlas(Pumpe *pumpe, float amount)
{
  delay(1000);
  long startTime = millis();
  long lastTime = startTime;
  float loadCell = waage.getValue();
  float oldValue = loadCell;
  bool finished = false;
  bool refill = false;
  float startValue = loadCell;
  float goalValue = startValue + amount;

  int interval = 3000;

  while (loadCell < goalValue)
  {
    waage.update();
    loadCell = waage.getValue();
    pumpe->forward();
    ledstripe.setLed(pumpe->bottleLed, strip.Color(0, 0, 255));
    ledstripe.setLed(glasLed, strip.Color(0, 0, 255));

    long actualTime = millis();


    if (actualTime - lastTime >= interval)
    {
      if (oldValue + 1 > loadCell)
      {
        refill = true;
      }
      lastTime = actualTime;
      interval = 1000;
      oldValue = loadCell;
    }

    if (refill)
    {
      pumpe->stop();
      ledstripe.setLed(pumpe->bottleLed, strip.Color(0, 0, 0));
      ledstripe.setLed(glasLed, strip.Color(0, 0, 0));

      Serial.write(0x02);
      Serial.print("refill");
      Serial.write(0x03);

      interval = 5000;


      while (refill)
      {

        //Blink here
        ledstripe.setLed(pumpe->bottleLed, strip.Color(255, 0, 0));
        delay(250);
        ledstripe.setLed(pumpe->bottleLed, strip.Color(0, 0, 0));
        delay(250);

        if (Serial.available())
        {
          String test = Serial.readString();
          if (test == "done\n")
          {
            refill = false;
          }
        }
      }

      startTime = millis();
      lastTime = startTime;
    }
    if (loadCell >= goalValue) finished = true;

  }


  if (finished)
  {
    pumpe->stop();
    ledstripe.setLed(pumpe->bottleLed, strip.Color(0, 0, 0));
    ledstripe.setLed(glasLed, strip.Color(0, 0, 0));

    Serial.write(0x02);
    Serial.print("finish");
    Serial.write(0x03);
    finished = false;



    delay(1000);
  }
}


