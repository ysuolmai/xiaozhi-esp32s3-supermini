# ESP32-S3 SuperMini 小智AI固件

基于 [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) 官方固件适配，专为 ESP32-S3 SuperMini 开发板设计。

## 硬件配置

| 模块 | 型号 | 说明 |
|------|------|------|
| 主控 | ESP32-S3 SuperMini | 4MB Flash / 2MB PSRAM / 512KB SRAM |
| 功放 | MAX98357A | I2S数字功放 |
| 麦克风 | INMP441 | I2S数字麦克风 |
| 屏幕 | ST7789 | 240x240 SPI LCD |

## 接线图

这份配置避开了 ESP32-S3 原生 USB 常用的 GPIO19/GPIO20，也避开了大部分启动绑带脚。不同 ESP32-S3 SuperMini 批次引脚丝印可能略有不同，请以你手上的开发板引脚图为准。

### MAX98357A 功放

```text
MAX98357A    ESP32-S3
---------    --------
VIN    -->   3.3V
GND    -->   GND
BCLK   -->   GPIO4
LRC    -->   GPIO5
DIN    -->   GPIO6
GAIN   -->   不接(默认9dB) 或 GND(12dB)
SD     -->   不接(默认启用)
```

### INMP441 麦克风

```text
INMP441      ESP32-S3
-------      --------
VDD    -->   3.3V
GND    -->   GND
SCK    -->   GPIO7
WS     -->   GPIO15
SD     -->   GPIO16
L/R    -->   GND (左声道)
```

### ST7789 屏幕

```text
ST7789       ESP32-S3
------       --------
VCC    -->   3.3V
GND    -->   GND
SCL    -->   GPIO12
SDA    -->   GPIO11
DC     -->   GPIO9
CS     -->   GPIO10
RST    -->   3.3V (或不接)
BLK    -->   3.3V (常亮)
```

## 源码编译

### 环境准备

```bash
# 1. 安装 ESP-IDF v5.4+
git clone -b v5.4 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32s3
source export.sh

# 2. 克隆官方仓库
git clone --recursive https://github.com/78/xiaozhi-esp32.git
cd xiaozhi-esp32

# 3. 下载或复制本板卡配置
git clone https://github.com/dakeqi/xiaozhi-esp32s3-supermini.git board-config

# 4. 复制板卡文件
mkdir -p main/boards/esp32s3-supermini
cp board-config/config.h main/boards/esp32s3-supermini/
cp board-config/esp32s3_supermini_board.cc main/boards/esp32s3-supermini/

# 5. 注册 Board Type 选项
python board-config/scripts/setup_board.py main
```

### 编译烧录

```bash
# 设置目标芯片
idf.py set-target esp32s3

# 配置，选择 ESP32-S3 SuperMini
idf.py menuconfig
# Xiaozhi Assistant -> Board Type -> ESP32-S3 SuperMini

# 编译
idf.py build

# 烧录
idf.py -p COM3 flash

# 查看日志
idf.py -p COM3 monitor
```

## 使用配置

### 首次配网

1. 上电后设备进入配网模式，屏幕显示配网二维码
2. 微信扫码或使用小智APP配网
3. 输入WiFi密码完成配网

### 语音唤醒

默认唤醒词：**"你好小智"**

说出唤醒词后，设备进入对话模式，可以：
- 问答对话
- 播放音乐
- 智能家居控制
- 更多功能

### 按键操作

| 操作 | 功能 |
|------|------|
| 短按 BOOT | 手动唤醒/停止对话 |
| 长按 BOOT 5秒 | 重置WiFi配置 |

## 调试指南

### 串口日志

```bash
# Windows
idf.py -p COM3 monitor

# Linux/Mac
idf.py -p /dev/ttyACM0 monitor
```

### 常见问题

#### 1. 没有声音

- 检查 MAX98357A 接线是否正确
- 确认 BCLK/LRC/DIN 三根线都已连接
- 检查扬声器是否正常（4Ω-8Ω）

#### 2. 麦克风无法录音

- 检查 INMP441 的 L/R 引脚是否接 GND
- 确认 SCK/WS/SD 接线正确
- 检查 VDD 是否为 3.3V

#### 3. 屏幕不亮/显示异常

- 确认 SPI 接线正确
- 检查 DC/CS/SCL/SDA 引脚是否与 `config.h` 一致
- 尝试调整 `DISPLAY_INVERT_COLOR`、`DISPLAY_MIRROR_X`、`DISPLAY_MIRROR_Y`

#### 4. 板载 LED 不亮

不同 ESP32-S3 SuperMini 的板载 LED 可能不是普通 GPIO LED，也可能接在 GPIO48 的 RGB LED 上。若不亮，请修改 `config.h` 里的 `BUILTIN_LED_GPIO`，或按上游项目已有 RGB LED 驱动板型改写 `GetLed()`。

#### 5. WiFi连接失败

- 确认WiFi为2.4GHz（不支持5GHz）
- 检查密码是否正确
- 长按BOOT 5秒重新配网

## 引脚占用总览

| GPIO | 功能 | 模块 |
|------|------|------|
| 0 | BOOT | 按键 |
| 4 | BCLK | MAX98357A |
| 5 | LRC | MAX98357A |
| 6 | DIN | MAX98357A |
| 7 | SCK | INMP441 |
| 9 | DC | ST7789 |
| 10 | CS | ST7789 |
| 11 | MOSI/SDA | ST7789 |
| 12 | SCLK/SCL | ST7789 |
| 15 | WS | INMP441 |
| 16 | SD | INMP441 |
| 48 | LED | 板载 LED，视开发板版本而定 |

## 相关链接

- [小智官方固件](https://github.com/78/xiaozhi-esp32)
- [小智官方服务](https://xiaozhi.me)

## License

MIT License
