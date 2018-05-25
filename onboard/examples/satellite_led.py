#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from rscsp.onboard import onboard

if __name__ == '__main__':
    # 衛星LEDを全て使用開始：引数はLED番号 (1..4)
    onboard.sat.use(1)
    onboard.sat.use(2)
    onboard.sat.use(3)
    onboard.sat.use(4)

    # 順番に点灯
    try:
        while True:
            for i in range(1, 5):
                onboard.sat.on(i)   # 点灯関数：引数はLED番号
                sleep(0.05)
                onboard.sat.off(i)  # 消灯関数：引数はLED番号
    # Ctrl+C の入力でループから脱出
    except KeyboardInterrupt:
        print('Quit...')

    # 後始末をして終了
    onboard.clean()
    sys.exit(0)
