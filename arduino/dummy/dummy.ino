/***

   Test Dummy
   This file is just for testing purpouse
   It recieves comannds for filling a glas and responses within a random time with "refill" or "finish"
   In refill mode the program waits for ar "done" command to continue
*/

void setup() {

  delay(1000);
  randomSeed(analogRead(0));

  Serial.begin(9600);
  delay(1000);
}

void fillTest()
{
  // print a random number from 1 to 10
  long randNumber = random(1, 5);
  bool refill = false;

  long startMilli = millis();

  while(millis()-startMilli<(5000))
  {
    if (Serial.available())
    {
      String test = Serial.readString();
      if (test == "interrupt\n")
      {
        break;
      }
    }
  }
  
  if (randNumber % 2 == 0)
  {
    refill = true;
    Serial.write(0x02);
    Serial.print("refill");
    Serial.write(0x03);
  }

  while (refill)
  {
    String test = Serial.readString();
    if (test == "done\n")
    {
      refill = false;
    }
  }
  Serial.write(0x02);
  Serial.print("finish");
  Serial.write(0x03);
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

void loop() {

  int zaehler = 0;
  char command[20];
  bool newSerialEvent = false;

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
    float amount;
    int motor, motorSpeed, ventil, state, pumpe, ledShow, wait, r, g, b, sub;

    switch (program)
    {
      case 4:
        pumpe = getValue(command, ' ', 1);
        amount = getValue(command, ' ', 2);

        fillTest();
        break;
      case 5:
        int randNumber = random(0, 10);
        int value[] = {10,50,100,150,200,250,300,350,400,450};
        delay(5);

        Serial.write(0x02);
        Serial.print(value[randNumber]);
        Serial.write(0x03);

        break;
      default:
        //do nothing
        break;
    }
  }

  delay(100);

}
