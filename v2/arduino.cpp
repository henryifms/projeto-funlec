#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192,168,1,50);
IPAddress broadcastIP(192,168,1,255);

unsigned int localPort = 8888;
unsigned int targetPort = 9999;

const int buttonPin = 2;

EthernetUDP Udp;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);
}

void loop() {
  if (digitalRead(buttonPin) == LOW) {
    Udp.beginPacket(broadcastIP, targetPort);
    Udp.print("LOCK_NOW");
    Udp.endPacket();
    delay(1000);
  }
}
