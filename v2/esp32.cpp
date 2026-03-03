#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "WIFI";
const char* password = "SENHA";

WiFiUDP Udp;

const int buttonPin = 2;

IPAddress broadcastIP(192,168,1,255);
unsigned int localPort = 8888;
unsigned int targetPort = 9999;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectadp!");
  Serial.println(WiFi.localIP());

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
