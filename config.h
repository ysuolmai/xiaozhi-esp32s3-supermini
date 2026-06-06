#ifndef _BOARD_CONFIG_H_
#define _BOARD_CONFIG_H_

#include <driver/gpio.h>

// ============================================================
// ESP32-S3 SuperMini
// MAX98357A + INMP441 + No display
// 4MB Flash / 2MB PSRAM / 512KB SRAM
// ============================================================

#define AUDIO_INPUT_SAMPLE_RATE  16000
#define AUDIO_OUTPUT_SAMPLE_RATE 24000

// Simplex I2S mode (separate TX/RX channels)
#define AUDIO_I2S_METHOD_SIMPLEX

// INMP441 Microphone (I2S RX), aligned with upstream bread-compact-wifi
#define AUDIO_I2S_MIC_GPIO_WS    GPIO_NUM_4
#define AUDIO_I2S_MIC_GPIO_SCK   GPIO_NUM_5
#define AUDIO_I2S_MIC_GPIO_DIN   GPIO_NUM_6

// MAX98357A Speaker (I2S TX), use only ESP32-S3 SuperMini header GPIO 1-13
#define AUDIO_I2S_SPK_GPIO_DOUT  GPIO_NUM_11
#define AUDIO_I2S_SPK_GPIO_BCLK  GPIO_NUM_12
#define AUDIO_I2S_SPK_GPIO_LRCK  GPIO_NUM_13

// Buttons
#define BOOT_BUTTON_GPIO        GPIO_NUM_0
#define TOUCH_BUTTON_GPIO       GPIO_NUM_NC
#define VOLUME_UP_BUTTON_GPIO   GPIO_NUM_NC
#define VOLUME_DOWN_BUTTON_GPIO GPIO_NUM_NC

// Onboard WS2818/RGB LED DIN. External header GPIOs are limited to GPIO 1-13.
#define BUILTIN_LED_GPIO        GPIO_NUM_48

#ifdef CONFIG_ESP32S3_SUPERMINI_ST7789_DISPLAY
// ST7789 LCD Display
#define DISPLAY_MOSI_PIN        GPIO_NUM_8
#define DISPLAY_CLK_PIN         GPIO_NUM_7
#define DISPLAY_CS_PIN          GPIO_NUM_10
#define DISPLAY_DC_PIN          GPIO_NUM_9
#define DISPLAY_RST_PIN         GPIO_NUM_NC
#define DISPLAY_BACKLIGHT_PIN   GPIO_NUM_NC

#define DISPLAY_WIDTH           240
#define DISPLAY_HEIGHT          240
#define DISPLAY_MIRROR_X        false
#define DISPLAY_MIRROR_Y        false
#define DISPLAY_SWAP_XY         false
#define DISPLAY_INVERT_COLOR    true
#define DISPLAY_RGB_ORDER       LCD_RGB_ELEMENT_ORDER_RGB
#define DISPLAY_OFFSET_X        0
#define DISPLAY_OFFSET_Y        0
#define DISPLAY_SPI_MODE        0
#endif

#endif // _BOARD_CONFIG_H_
