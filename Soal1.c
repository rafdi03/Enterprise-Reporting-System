/* * SOAL 1: LED OOP Controller
 * File: led_controller.cpp
 */

#include "freertos/FreeRTOS.h"
#include "freertos/timers.h"
#include "driver/gpio.h"
#include "esp_log.h"

// Log tag untuk debugging
static const char *TAG = "LED_CTRL";

// Enum untuk Level Aktif (Active High/Low) [cite: 12]
enum ActiveLevel {
    ACTIVE_LOW = 0,
    ACTIVE_HIGH = 1
};

// Kelas LED Controller
class LedController {
private:
    gpio_num_t pin;
    ActiveLevel activeLevel;
    TimerHandle_t blinkTimer;
    int frequencyHz;
    bool isOn;

    // Callback statis untuk Timer FreeRTOS (bridge ke instance method)
    static void timerCallbackStatic(TimerHandle_t xTimer) {
        // Mendapatkan pointer ke object LedController dari ID Timer
        LedController* led = static_cast<LedController*>(pvTimerGetTimerID(xTimer));
        led->toggle();
    }

    // Method toggle fisik
    void toggle() {
        isOn = !isOn;
        // Logic XOR untuk menangani Active High/Low dengan benar
        gpio_set_level(pin, (isOn ? activeLevel : !activeLevel));
        ESP_LOGD(TAG, "LED Pin %d toggled to %d", pin, isOn);
    }

public:
    // Constructor: Inisialisasi GPIO dan Timer
    LedController(gpio_num_t gpioPin, ActiveLevel level, int freq) 
        : pin(gpioPin), activeLevel(level), frequencyHz(freq), isOn(false) {
        
        // Konfigurasi GPIO
        gpio_reset_pin(pin);
        gpio_set_direction(pin, GPIO_MODE_OUTPUT);
        gpio_set_level(pin, !activeLevel); // Default Off

        // Setup Timer: Perioda (ms) = 1000 / (freq * 2) agar on+off = 1 siklus penuh
        // Contoh: 1 Hz = 500ms on, 500ms off.
        TickType_t timerPeriod = pdMS_TO_TICKS(1000 / (frequencyHz * 2));
        
        // Membuat software timer
        blinkTimer = xTimerCreate("LedTimer", timerPeriod, pdTRUE, (void*)this, timerCallbackStatic);
    }

    void on() {
        xTimerStop(blinkTimer, 0); // Stop timer jika sedang blinking
        isOn = true;
        gpio_set_level(pin, activeLevel);
        ESP_LOGI(TAG, "LED Pin %d set to ON", pin);
    }

    void off() {
        xTimerStop(blinkTimer, 0);
        isOn = false;
        gpio_set_level(pin, !activeLevel);
        ESP_LOGI(TAG, "LED Pin %d set to OFF", pin);
    }

    void blink() {
        if (!xTimerIsTimerActive(blinkTimer)) {
            xTimerStart(blinkTimer, 0);
            ESP_LOGI(TAG, "LED Pin %d blinking at %d Hz", pin, frequencyHz);
        }
    }
};

// Main Program (Simulasi)
extern "C" void app_main() {
    // Instansiasi Object sesuai Tabel Soal [cite: 12]
    LedController ledRed(GPIO_NUM_18, ACTIVE_LOW, 10);   // 10 Hz
    LedController ledGreen(GPIO_NUM_19, ACTIVE_HIGH, 5); // 5 Hz
    LedController ledBlue(GPIO_NUM_21, ACTIVE_HIGH, 2);  // 2 Hz

    // Requirement C: Menjalankan ketiganya bersamaan [cite: 19]
    ESP_LOGI(TAG, "Starting all LEDs in Blink Mode...");
    ledRed.blink();
    ledGreen.blink();
    ledBlue.blink();

    // Biarkan berjalan selamanya (Task Main tidak boleh return)
    while(1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}