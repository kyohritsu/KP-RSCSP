#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from rscsp.onboard import onboard

if __name__ == '__main__':
    # ステータスLEDを使用開始
    onboard.status.use()

    # 2種類のパターンで点滅
    try:
        while True:
            for i in range(20):
                onboard.status.on()    # 点灯関数
                sleep(0.25)
                onboard.status.off()   # 消灯関数
                sleep(0.25)
            for i in range(20):
                onboard.status.on()
                sleep(0.05)
                onboard.status.off()
                sleep(0.45)
    # Ctrl+C の入力でループから脱出
    except KeyboardInterrupt:
        print('Quit...')

    # 後始末をして終了
    onboard.clean()
    sys.exit(0)
