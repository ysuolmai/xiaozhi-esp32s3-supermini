# ESP32-S3 SuperMini 小智AI固件

基于 [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) 官方固件适配，专为 ESP32-S3 SuperMini 开发板设计。

## 硬件配置

| 模块 | 型号 | 说明 |
|------|------|------|
| 主控 | ESP32-S3 SuperMini | 4MB Flash / 2MB PSRAM / 512KB SRAM |
| 功放 | MAX98357A | I2S数字功放 |
| 麦克风 | INMP441 | I2S数字麦克风 |
| 屏幕 | 可选 | 默认无屏；可编译 ST7789 240x240 SPI LCD 版本 |

> ESP32-S3FH4R2 的封装内 Flash 是 4MB Quad SPI，封装内 PSRAM 是 2MB Quad SPI。不要按 ESP32-S3R8/R16V 那类 8MB/16MB PSRAM 芯片配置成 Octal/OPI。

## 接线图

这份配置避开了 ESP32-S3 原生 USB 常用的 GPIO19/GPIO20，也避开了大部分启动绑带脚。不同 ESP32-S3 SuperMini 批次引脚丝印可能略有不同，请以你手上的开发板引脚图为准。

### MAX98357A 功放

```text
MAX98357A    ESP32-S3
---------    --------
VIN    -->   3.3V
GND    -->   GND
BCLK   -->   GPIO12
LRC    -->   GPIO13
DIN    -->   GPIO11
GAIN   -->   不接(默认9dB) 或 GND(12dB)
SD     -->   不接(默认启用)
```

### INMP441 麦克风

```text
INMP441      ESP32-S3
-------      --------
VDD    -->   3.3V
GND    -->   GND
SCK    -->   GPIO5
WS     -->   GPIO4
SD     -->   GPIO6
L/R    -->   GND (左声道)
```

默认版本不使用屏幕，GPIO7/GPIO8/GPIO9/GPIO10 未被 LCD 占用，可按需改作其它外设。

### 可选 ST7789 屏幕

选择 `esp32s3-supermini-st7789` 构建时启用：

```text
ST7789       ESP32-S3
------       --------
VCC    -->   3.3V
GND    -->   GND
SCL    -->   GPIO7
SDA    -->   GPIO8
DC     -->   GPIO9
CS     -->   GPIO10
RST    -->   3.3V (或不接)
BLK    -->   3.3V (常亮)
```

## 固件版本

| 构建名称 | 屏幕 | 说明 |
|----------|------|------|
| `esp32s3-supermini` | 无 | 默认版本，使用 `NoDisplay`，节省资源和 GPIO |
| `esp32s3-supermini-st7789` | ST7789 | 启用 240x240 SPI LCD |

## 源码编译

### 环境准备

```bash
# 1. 安装 ESP-IDF v5.5.2+
git clone -b v5.5.2 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh esp32s3
source export.sh

# 2. 克隆官方仓库
git clone --recursive https://github.com/78/xiaozhi-esp32.git
cd xiaozhi-esp32

# 3. 下载或复制本板卡配置
git clone https://github.com/ysuolmai/xiaozhi-esp32s3-supermini.git board-config

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

# 默认构建无屏版本；如需 ST7789，追加：
# CONFIG_ESP32S3_SUPERMINI_ST7789_DISPLAY=y

# 编译
idf.py build

# 烧录
idf.py -p COM3 flash

# 查看日志
idf.py -p COM3 monitor
```

## 使用配置

### 首次配网

1. 上电后设备进入配网模式
2. 按串口日志提示或使用小智APP完成配网
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

#### 3. 板载 LED 不亮

外接音频和屏幕模块只使用可插针 GPIO1-GPIO13。板载 RGB LED 的 DIN 标注为 GPIO48，不属于两侧可插针；若你的板载 LED 不是普通 GPIO LED，请修改 `config.h` 里的 `BUILTIN_LED_GPIO`，或按上游项目已有 RGB LED 驱动板型改写 `GetLed()`。

#### 4. WiFi连接失败

- 确认WiFi为2.4GHz（不支持5GHz）
- 检查密码是否正确
- 长按BOOT 5秒重新配网

## 引脚占用总览

| GPIO | 功能 | 模块 |
|------|------|------|
| 0 | BOOT | 按键 |
| 4 | WS | INMP441 |
| 5 | SCK | INMP441 |
| 6 | SD | INMP441 |
| 11 | DIN | MAX98357A |
| 12 | BCLK | MAX98357A |
| 13 | LRC | MAX98357A |
| 48 | LED | 板载 RGB LED DIN，不属于可插针 |

ST7789 版本额外占用：

| GPIO | 功能 | 模块 |
|------|------|------|
| 7 | SCLK/SCL | ST7789 |
| 8 | MOSI/SDA | ST7789 |
| 9 | DC | ST7789 |
| 10 | CS | ST7789 |

## 相关链接

- [小智官方固件](https://github.com/78/xiaozhi-esp32)
- [小智官方服务](https://xiaozhi.me)

## License

MIT License
