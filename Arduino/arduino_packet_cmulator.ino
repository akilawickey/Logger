


// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 13 as an output.
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  

    Serial.print("34");
    Serial.print(",");

    //delay(1000);
    Serial.print("24");
        Serial.print(",");

  //  delay(1000);
    Serial.print("54");
        Serial.print(",");

   // delay(1000);
    Serial.print("14");
        Serial.print(",");

//    delay(1000);
    Serial.print("94");
        Serial.println(",");

    delay(500);  


  // wait for a second
}
