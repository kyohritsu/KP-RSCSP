#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from rscsp.onboard import onboard

# カラー指定：前の要素から順に赤、緑、青の出力に対応
COLOR_TABLE = [
    [0, 0, 0],  # 消灯
    [1, 0, 0],  # 赤
    [1, 1, 0],  # 黄
    [0, 1, 0],  # 緑
    [0, 1, 1],  # 水色
    [0, 0, 1],  # 青
    [1, 0, 1],  # 紫色
    [1, 1, 1]   # 白
]

if __name__ == '__main__':
    # RGB LEDを使用開始
    onboard.rgb.use()

    # カラー指定リスト順に点灯
    try:
        while True:
            for i in COLOR_TABLE:
                onboard.rgb.out(i)  # 点灯関数：引数は色指定の3要素リスト
                sleep(0.5)
    # Ctrl+C の入力でループから脱出
    except KeyboardInterrupt:
        print('Quit...')

    # 後始末をして終了
    onboard.clean()
    sys.exit(0)
