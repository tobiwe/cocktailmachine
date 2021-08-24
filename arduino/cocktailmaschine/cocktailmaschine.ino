#include "Waage.hpp"
#include "pumpe.hpp"
#include "Luftpumpe.hpp"
#include "Led.hpp"
#include "Ventil.hpp"
#include "Drucksensor.hpp"
#include "config.hpp"

int peristalicLed[6] = { 5, 4, 3, 2, 1, 0};
int airLed[4] = { 13, 12, 15, 14};
int bottleLed[6] = {6, 7, 8, 9, 10, 11};
int glasLed = 16;

char newCommand[20];
char command[20];
int program = 0;
int old = 0;
char oldCommand[20];

int zaehler = 0;
bool newSerialEvent = false;

bool switchtoOldProgram = false;


Waage waage;
Led ledstripe;

Ventil ventile[4] = {
  Ventil(VENTIL1),
  Ventil(VENTIL2),
  Ventil(VENTIL3),
  Ventil(VENTIL4)
};

Drucksensor sensoren[4] = {
  Drucksensor(DRUCK1),
  Drucksensor(DRUCK2),
  Drucksensor(DRUCK3),
  Drucksensor(DRUCK4),
};


Pumpe p1(PERISTALIC, MOTOR1_In1, MOTOR1_In2, MOTOR1_En, peristalicLed[0], bottleLed[0], false);
Pumpe p2(PERISTALIC, MOTOR2_In1, MOTOR2_In2, MOTOR2_En, peristalicLed[1], bottleLed[1], false);
Pumpe p3(PERISTALIC, MOTOR3_In1, MOTOR3_In2, MOTOR3_En, peristalicLed[2], bottleLed[2], true);
Pumpe p4(PERISTALIC, MOTOR4_In1, MOTOR4_In2, MOTOR4_En, peristalicLed[3], bottleLed[3], true);
Pumpe p5(PERISTALIC, MOTOR5_In1, MOTOR5_In2, MOTOR5_En, peristalicLed[4], bottleLed[4], false);
Pumpe p6(PERISTALIC, MOTOR6_In1, MOTOR6_In2, MOTOR6_En, peristalicLed[5], bottleLed[5], true);
Luftpumpe a1(AIR, MOTOR7_In1, MOTOR7_In2, MOTOR7_En, airLed[0], airLed[0], ventile[0], &(sensoren[0]), false);
Luftpumpe a2(AIR, MOTOR8_In1, MOTOR8_In2, MOTOR8_En, airLed[1], airLed[1], ventile[1], &(sensoren[1]), false);
Luftpumpe a3(AIR, MOTOR9_In1, MOTOR9_In2, MOTOR9_En, airLed[2], airLed[2], ventile[2], &(sensoren[2]), false);
Luftpumpe a4(AIR, MOTOR10_In1, MOTOR10_In2, MOTOR10_En, airLed[3], airLed[3], ventile[3], &(sensoren[3]), false);

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
  }

  a1.setSpeed(150);
  a2.setSpeed(150);
  a3.setSpeed(150);
  a4.setSpeed(150);

  for (Ventil v : ventile)
  {
    v.setup();
    v.open();
  }
  delay(1000);
  for (Ventil v : ventile)
  {
    v.setup();
    v.close();
  }

  for (int i = 0; i < 4; i++)
  {
    sensoren[i].update();
    sensoren[i].setDefaultPressure(sensoren[i].getValue());
  }

  ledstripe.setup();
}

void loop() {

  for (int i = 0; i < 4; i++)
  {
    sensoren[i].update();
  }
  waage.update();

  checkForSerialEvent();
  if (newSerialEvent)
  {
    old = program;
    memcpy(oldCommand, command, sizeof(command));
    memcpy(command, newCommand, sizeof(newCommand));
    program = getValue(command, ' ', 0);
    newSerialEvent = false;

    /** Debug
        Serial.print("Old: ");
        Serial.print(old);
        Serial.print(", ");
        Serial.print("Buffer");
        Serial.println(oldCommand);

        Serial.print("New: ");
        Serial.print(program);
        Serial.print(", ");
        Serial.print("Buffer");
        Serial.println(command);*/
  }

  float amount, mass;
  int motor, motorSpeed, ventil, state, pumpe, ledShow, wait, r, g, b, sub, cmd, pressure;
  switch (program)
  {
    case 1:
      cmd = getValue(command, ' ', 1);
      if (cmd == 1)
      {
        ledstripe.setLed(getValue(command, ' ', 2), strip.Color(getValue(command, ' ', 3), getValue(command, ' ', 4), getValue(command, ' ', 5)));
      }
      else if (cmd == 2)
      {
        ledstripe.fillLed(strip.Color(getValue(command, ' ', 2), getValue(command, ' ', 3), getValue(command, ' ', 4)));
      }
      program = 0;
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
      program = 0;
      break;
    case 3:
      ventil = getValue(command, ' ', 1);
      state = getValue(command, ' ', 2);
      if (state == 1)ventile[ventil].open();
      else if (state == 0) ventile[ventil].close();
      program = 0;
      break;
    case 4:
      pumpe = getValue(command, ' ', 1);
      amount = getValue(command, ' ', 2);
      fillGlas(pumpen[pumpe - 1], amount);
      program = 0;
      break;
    case 5:
      sub = getValue(command, ' ', 1);
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
      switchtoOldProgram = true;
      break;
    case 6:
      ledShow = getValue(command, ' ', 1);

      if (ledShow == 1)
      {
        wait = getValue(command, ' ', 2);
        ledstripe.fasterRainbow(wait);
      }

      else if (ledShow == 2)
      {
        wait = getValue(command, ' ', 2);
        ledstripe.fasterTheaterChaseRainbow(wait);
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
      else if (ledShow == 5)
      {
        wait = getValue(command, ' ', 2);
        r = getValue(command, ' ', 3);
        g = getValue(command, ' ', 4);
        b = getValue(command, ' ', 5);
        ledstripe.fasterBlinkOnOff(strip.Color(r, g, b), wait);
      }
      break;
    case 7:
      pressure = getValue(command, ' ', 1);
      Serial.write(0x02);
      Serial.print(sensoren[pressure].getValue());
      Serial.write(0x03);
      program = 0;
      break;
    default:
      //do nothing
      break;
  }
  if (program != 6)
  {
    delay(50);
  }
  else
  { delay(1);
  }

  if (switchtoOldProgram)
  {

    //Toggle Program
    int tmp = old;
    old = program;
    program = tmp;

    //Toggle Commands
    char tmpCommand[20];;
    memcpy(tmpCommand, command, sizeof(command));
    memcpy(command, oldCommand, sizeof(oldCommand));
    memcpy(oldCommand, tmpCommand, sizeof(tmpCommand));

    switchtoOldProgram = false;
  }
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
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  String sub = data.substring(strIndex[0], strIndex[1]);
  return found > index ? sub.toFloat() : 0;
}


void fillGlas(Pumpe *pumpe, float amount)
{
  delay(100);
  long startTime = millis();
  long lastTime = startTime;
  long lastSpeedCheck = startTime;
  float loadCell = waage.getValue();
  float oldSpeedWeight = loadCell;
  float oldValue = loadCell;
  float oldPressure = 0;
  bool finished = false;
  bool refill = false;
  float startValue = loadCell;
  float goalValue = startValue + amount;
  bool interrupt = false;
  Drucksensor *sensor = nullptr;
  if (pumpe->getType() == AIR)
  {
    sensor  = ((Luftpumpe*)pumpe)->sensor;
    oldPressure = sensor->getValue();
  }

  int interval = 6000;
  int maxInterval = 10000;

  while (loadCell < goalValue)
  {
    ledstripe.fillLed(strip.Color(0, 0, 0));
    waage.update();
    if (pumpe->getType() == AIR)
    {
      sensor->update();
    };

    loadCell = waage.getValue();
    pumpe->forward();
    ledstripe.setLed(pumpe->bottleLed, strip.Color(0, 0, 255));
    ledstripe.setLed(glasLed, strip.Color(0, 0, 255));

    long actualTime = millis();
    bool updateInterval = false;


    if (actualTime - lastTime >= interval)
    {

      if (pumpe->getType() == AIR)
      {
        if (oldPressure + 0.2 > sensor->getValue() && oldValue + 1 > loadCell)
        {
          refill = true;
        }
      }

      else if (oldValue + 1 > loadCell)
      {
        refill = true;
      }

      lastTime = actualTime;
      interval = 1000;
      oldValue = loadCell;
      oldPressure = sensor->getValue();
    }

    // Flow per time check for speed optimization
    if (pumpe->getType() == AIR)
    {
      if (actualTime - lastSpeedCheck >= 1000 && loadCell > oldValue)
      {
        int actualSpeed = pumpe->getSpeed();
        int change = loadCell - oldSpeedWeight;
        //Check for 10g
        if (change < 15 && actualSpeed < 200)
        {
          pumpe->setSpeed(actualSpeed += 5);
        }
        else if (change > 5 && actualSpeed > 100)
        {
          pumpe->setSpeed(actualSpeed -= 5);
        }

        lastSpeedCheck = actualTime;
        oldSpeedWeight = loadCell;
      }
    }



    if (refill)
    {
      pumpe->stop(false);
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

        for (int i : peristalicLed)
        {
          ledstripe.setLed(i, strip.Color(255, 0, 0));
        }

        delay(250);
        ledstripe.setLed(pumpe->bottleLed, strip.Color(0, 0, 0));
        for (int i : peristalicLed)
        {
          ledstripe.setLed(i, strip.Color(0, 0, 0));
        }
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

    if (loadCell >= goalValue)
    {
      finished = true;
    }

    if (Serial.available())
    {
      String test = Serial.readString();
      if (test == "interrupt\n")
      {
        finished = true;
        break;
      }
    }
  }


  if (finished)
  {
    pumpe->stop(false);
    if (pumpe->getType() == AIR)
    {
      Luftpumpe* air = (Luftpumpe*)pumpe;
      air->ventil.open();
    }

    ledstripe.fillLed(strip.Color(255, 255, 255));
    //Wait till weight stays the same
    bool valueChange = true;
    float first, second;
    while (valueChange)
    {
      first = waage.getValue();
      long startTime = millis();
      while (millis() - startTime < 2000)
      {
        waage.update();
        delay(10);
      }
      second = waage.getValue();

      if ((second - first) < 0.1)
      {
        valueChange = false;
        if (pumpe->getType() == AIR)
        {
          Luftpumpe* air = (Luftpumpe*)pumpe;
          air->ventil.close();
        }
      }
    }

    Serial.write(0x02);
    Serial.print("finish");
    Serial.write(0x03);
    finished = false;
    delay(100);
  }
}

void checkForSerialEvent()
{
  while (Serial.available()) {

    char inChar = (char)Serial.read();
    if (inChar == 0x02) {
      zaehler = 0;
    }
    else if (inChar == 0x03) {
      newSerialEvent = true;
      newCommand[zaehler] = '\0';
      break;
    }
    else {
      newCommand[zaehler] = inChar;
      zaehler++;
    }
  }
}
