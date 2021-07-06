/***
 * 
 * Test Dummy
 * This file is just for testing purpouse
 * It recieves comannds for filling a glas and responses within a random time with "refill" or "finish"
 * In refill mode the program waits for ar "done" command to continue
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
  delay(500 * randNumber);

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
  delay(500 * randNumber);
  Serial.write(0x02);
  Serial.print("finish");
  Serial.write(0x03);
}

int getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]).toInt() : 0;
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
    int motor, motorSpeed, ventil, state, pumpe, amaount, ledShow, wait, r, g, b, sub;

    switch (program)
    {
      case 4:
        pumpe = getValue(command, ' ', 1);

        amaount = getValue(command, ' ', 2);

        fillTest();

        break;
      default:
        //do nothing
        break;
    }
  }

  delay(100);

}

