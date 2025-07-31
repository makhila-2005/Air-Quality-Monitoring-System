#include <ESP8266WiFi.h>
#include "ThingSpeak.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

// LCD setup
LiquidCrystal_I2C lcd(0x27, 16, 2);  // 16x2 LCD at I2C address 0x27

// DHT11 setup
#define DHTPIN D4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Pins
#define MQ2_PIN A0
#define LDR_PIN D7
#define LED1_PIN D5     // LED control for LDR
#define PIR_PIN D6      // PIR motion sensor

// Thresholds
const int MQ2_THRESHOLD = 300;
const float TEMP_THRESHOLD = 30.0;
const int LDR_THRESHOLD = 500;

// WiFi credentials
char ssid[] = "mnrkumar_5G";  // Your WiFi SSID
char pass[] = "mnrkumar123";            // Your WiFi Password
WiFiClient client;

// ThingSpeak details
unsigned long myChannelNumber = 3017296;
const char *myWriteAPIKey = "BLM2MOUVY2MVUMMB";

void setup() {
  Serial.begin(115200);
  dht.begin();
  lcd.init();
  lcd.backlight();

  pinMode(LED1_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);

  // LCD init message
  lcd.setCursor(0, 0);
  lcd.print("   System Init   ");
  delay(2000);
  lcd.clear();

  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);
}

void loop() {
  // WiFi connection check
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.println(ssid);
    while (WiFi.status() != WL_CONNECTED) {
      WiFi.begin(ssid, pass);
      delay(5000);
      Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");
  }

  // Sensor readings
  int mq2Value = analogRead(MQ2_PIN);
  int ldrValue = analogRead(LDR_PIN);
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int pirStatus = digitalRead(PIR_PIN);  // 1 = Motion detected, 0 = no motion

  // LED control based on LDR
  if(mq2Value>MQ2_THRESHOLD)
  {
    digitalWrite(LED1_PIN,HIGH);
  }
  else
  {
    digitalWrite(LED1_PIN,LOW);
  }

  // LCD Display
  lcd.setCursor(0, 0);
  lcd.print("Temp=");
  lcd.print(temperature, 1);
  lcd.print(" Hum=");
  lcd.print(humidity, 1);

  lcd.setCursor(0, 1);
  lcd.print("Gas=");
  lcd.print(mq2Value);
  lcd.print(" LDR=");
  lcd.print(ldrValue);

  // Debug output
  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print(" C, Hum: ");
  Serial.print(humidity);
  Serial.print(" %, MQ2: ");
  Serial.print(mq2Value);
  Serial.print(", LDR: ");
  Serial.print(ldrValue);
  Serial.print(", PIR: ");
  Serial.println(pirStatus);

  // Upload to ThingSpeak
  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  ThingSpeak.setField(3, mq2Value);
  ThingSpeak.setField(4, ldrValue);
  ThingSpeak.setField(5, pirStatus);

  int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
  if (x == 200) {
    Serial.println("Data sent to ThingSpeak.");
  } else {
    Serial.println("Error sending data. HTTP code: " + String(x));
  }

  delay(20000);  // 20 sec delay for ThingSpeak rate limit
}