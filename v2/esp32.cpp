#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "WIFI";
const char* password = "SENHA";

WiFiUDP Udp;

const int buttonLock = 2;
const int buttonShutdown = 4;

IPAddress broadcastIP(192, 168, 1, 255);
unsigned int localPort = 8888;
unsigned int targetPort = 9999;

void setup() {
  pinMode(buttonLock, INPUT_PULLUP);
  pinMode(buttonShutdown, INPUT_PULLUP);
  
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi conectado!");
  Serial.println(WiFi.localIP());
  Udp.begin(localPort);
}

void loop() {
  // Botão 1: Bloqueia sessão (Windows + L)
  if (digitalRead(buttonLock) == LOW) {
    Udp.beginPacket(broadcastIP, targetPort);
    Udp.print("LOCK_SESSION");
    Udp.endPacket();
    Serial.println("Enviado: LOCK_SESSION");
    delay(1000);
  }
  
  // Botão 2: Toggle bloqueio teclado/mouse
  if (digitalRead(buttonShutdown) == LOW) {
    Udp.beginPacket(broadcastIP, targetPort);
    Udp.print("TOGGLE_INPUT");
    Udp.endPacket();
    Serial.println("Enviado: TOGGLE_INPUT");
    delay(1000);
  }
}
