#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Cam";  
const char* password = "11111111";

WebServer server(80);
#define LED_BUILTIN 2

bool ledBlinking = false;  // Trạng thái nhấp nháy LED
bool ledState = false;     // Trạng thái hiện tại của LED
unsigned long prevMillis = 0;
const int blinkInterval = 300; // Thời gian nhấp nháy (500ms)

// Xử lý trang chủ
void handleRoot() {
  server.send(200, "text/plain", "ESP32 Server Running");
}

// Bật LED (bình thường)
void handleLEDOn() {
  ledBlinking = false;  // Dừng nhấp nháy
  digitalWrite(LED_BUILTIN, HIGH);
  server.send(200, "text/plain", "LED ON");
}

// Tắt LED
void handleLEDOff() {
  ledBlinking = false;  // Dừng nhấp nháy
  digitalWrite(LED_BUILTIN, LOW);
  server.send(200, "text/plain", "LED OFF");
}

// Khi phát hiện người, LED sẽ nhấp nháy
void handlePersonDetected() {
  ledBlinking = true;
  server.send(200, "text/plain", "Person Detected - LED Blinking");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("\nĐang kết nối WiFi...");
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    attempts++;
    if (attempts > 20) {  
      Serial.println("\nKhông thể kết nối WiFi, kiểm tra lại SSID và mật khẩu!");
      return;
    }
  }

  Serial.println("\nKết nối WiFi thành công!");
  Serial.print("Địa chỉ IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/led_on", handleLEDOn);
  server.on("/led_off", handleLEDOff);
  server.on("/person_detected", handlePersonDetected);  // Thêm API khi phát hiện người

  server.begin();
  Serial.println("Máy chủ web đã bắt đầu!");
}

void loop() {
  server.handleClient();

  // Nếu ledBlinking = true, LED sẽ nhấp nháy liên tục
  if (ledBlinking) {
    unsigned long currentMillis = millis();
    if (currentMillis - prevMillis >= blinkInterval) {
      prevMillis = currentMillis;
      ledState = !ledState; // Đảo trạng thái LED
      digitalWrite(LED_BUILTIN, ledState);
    }
  }
}
