#!/usr/bin/env python3
"""Setup ESP32-S3 SuperMini board in xiaozhi-esp32 project"""

import sys
import os

def update_cmakelists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'CONFIG_BOARD_TYPE_ESP32S3_SUPERMINI' in content:
        print('CMakeLists.txt already contains ESP32S3_SUPERMINI, skipping')
        return
    
    new_board = '''elseif(CONFIG_BOARD_TYPE_ESP32S3_SUPERMINI)
    set(BOARD_TYPE "esp32s3-supermini")
    set(BUILTIN_TEXT_FONT font_puhui_basic_14_1)
    set(BUILTIN_ICON_FONT font_awesome_14_1)
'''
    
    # Find the last board config entry (e.g., CONFIG_BOARD_TYPE_HU_087) and insert after it
    marker = 'elseif(CONFIG_BOARD_TYPE_HU_087)'
    if marker in content:
        # Find the endif() after this marker within the board config block
        idx = content.find(marker)
        # Find the endif() that closes the board selection block
        rest = content[idx:]
        # Look for the pattern: set(...) followed by endif()
        lines = rest.split('\n')
        insert_line = 0
        for i, line in enumerate(lines):
            if line.strip() == 'endif()' and i > 0:
                # Calculate absolute position
                insert_pos = idx + sum(len(l)+1 for l in lines[:i])
                content = content[:insert_pos] + new_board + content[insert_pos:]
                break
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('CMakeLists.txt updated')

def update_kconfig(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'BOARD_TYPE_ESP32S3_SUPERMINI' not in content:
        new_option = '''    config BOARD_TYPE_ESP32S3_SUPERMINI
        bool "ESP32-S3 SuperMini (4MB Flash / 2MB PSRAM, MAX98357A + INMP441)"
        depends on IDF_TARGET_ESP32S3
'''
        marker = 'config BOARD_TYPE_HU_087'
        if marker in content:
            idx = content.find(marker)
            rest = content[idx:]
            lines = rest.split('\n')
            insert_pos = idx
            for i, line in enumerate(lines[1:], 1):
                if line.strip().startswith('config ') or line.strip() == 'endchoice':
                    insert_pos = idx + sum(len(l)+1 for l in lines[:i])
                    break
            content = content[:insert_pos] + new_option + content[insert_pos:]
    else:
        print('Kconfig.projbuild already contains ESP32S3_SUPERMINI, skipping board option')

    if 'ESP32S3_SUPERMINI_ST7789_DISPLAY' not in content:
        display_option = '''
config ESP32S3_SUPERMINI_ST7789_DISPLAY
    bool "Enable ST7789 display for ESP32-S3 SuperMini"
    depends on BOARD_TYPE_ESP32S3_SUPERMINI
    default n
'''
        marker = 'endchoice'
        idx = content.find(marker, content.find('choice BOARD_TYPE'))
        if idx != -1:
            insert_pos = idx + len(marker)
            content = content[:insert_pos] + display_option + content[insert_pos:]
    else:
        print('Kconfig.projbuild already contains ESP32S3_SUPERMINI_ST7789_DISPLAY, skipping display option')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Kconfig.projbuild updated')

if __name__ == '__main__':
    base_path = sys.argv[1] if len(sys.argv) > 1 else 'xiaozhi-esp32/main'
    update_cmakelists(os.path.join(base_path, 'CMakeLists.txt'))
    update_kconfig(os.path.join(base_path, 'Kconfig.projbuild'))
