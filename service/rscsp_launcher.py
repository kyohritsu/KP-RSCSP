#!/usr/bin/python3
# -*- coding: utf-8 -*-

## Copyright 2018 KYOHRITSU ELECTRONIC INDUSTRY CO., LTD.
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to
## deal in the Software without restriction, including without limitation the
## rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
## sell copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
## IN THE SOFTWARE.

import sys
import signal
from subprocess import Popen, call
from time import sleep
from rscsp.onboard import onboard

# オンエッジ検出で起動するコマンド
COMMAND_ON_RELEASE = ('. env/bin/activate && '
    'googlesamples-assistant-hotword --device_model_id my_rpi1')
PRECOMMAND_ON_RELEASE = 'pkill -f "googlesamples-assistant-hotword"'

# 長押し検出で起動するコマンド
COMMAND_ON_HOLD = 'sudo shutdown -h now'

# 長押し認識時間 (秒)
SW_HOLD_THRESHOLD_SECONDS = 5.0

def signal_handler(signum, frame):
    """各シグナル受信によるプログラムの終了処理"""
    print('Quit on SIGNAL %d...' % signum, file=sys.stderr)
    onboard.clean()
    sys.exit(0)

if __name__ == '__main__':
    # SIGTERM受信時の実行関数を登録
    signal.signal(signal.SIGTERM, signal_handler)

    # ステータスLEDを使用開始し、点灯
    onboard.status.use(1)
    # 押しボタンスイッチを使用開始
    onboard.pushsw.use()

    # オフエッジ、長押し検出でそれぞれコマンドを実行
    try:
        while True:
            # スイッチ入力の取得
            onboard.pushsw.capture()

            # オフエッジ検出を確認
            if onboard.pushsw.off_edge():
                call(PRECOMMAND_ON_RELEASE, shell=True)
                Popen(COMMAND_ON_RELEASE, shell=True)

            # 長押し検出を確認
            if onboard.pushsw.hold_time() >= SW_HOLD_THRESHOLD_SECONDS:
                Popen(COMMAND_ON_HOLD, shell=True)
                break

            # 一定時間待機
            sleep(0.02)
    # Ctrl+C の入力でループから脱出
    except KeyboardInterrupt:
        print('Quit...')

    # 後始末をして終了
    onboard.clean()
    sys.exit(0)
