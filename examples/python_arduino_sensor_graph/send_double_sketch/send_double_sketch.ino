void setup() {
    Serial.begin(9600);
    while (!Serial) {
       ; // wait for serial port to connect. Needed for native USB port only
    }

    // if analog input pin 0 is unconnected, random analog
    // noise will cause the call to randomSeed() to generate
    // different seed numbers each time the sketch runs.
    randomSeed(analogRead(0));
}

double randomDouble(double minf, double maxf)
// https://forum.arduino.cc/index.php?topic=371564.0
{
    return minf + random(1UL << 31) * (maxf - minf) / (1UL << 31); // use 1ULL<<63 for max double values)
}

void loop() {
    Serial.print(randomDouble(-40.00, 40.00), 3);
    Serial.print('\n');
    delay(50);
}
