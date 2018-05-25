#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from time import sleep
from rscsp.onboard import onboard

# 長押し認識時間 (秒)
SW_HOLD_THRESHOLD_SECONDS = 5.0

if __name__ == '__main__':
    # 押しボタンスイッチを使用開始
    onboard.pushsw.use()

    # オンエッジ、オフエッジ、長押し認識ごとにメッセージを表示
    try:
        while True:
            # (x) スイッチ入力の取得
            onboard.pushsw.capture()

            # (a) オンエッジ検出を確認
            # 処理 x で取得したスイッチ状態がオンエッジ (前回オフ→今回オン)
            # であった場合、下記関数の戻り値がTrueになります。
            if onboard.pushsw.on_edge():
                print('on')

            # (b) オフエッジ検出を確認
            # 処理 x で取得したスイッチ状態がオンエッジ (前回オフ→今回オン)
            # であった場合、下記関数の戻り値がTrueになります。
            if onboard.pushsw.off_edge():
                print('off')

            # (c) 長押し検出を確認
            # 処理 x で取得したスイッチ状態がオンを維持している場合、
            # 秒単位の持続時間が下記関数の戻り値として取得できます。
            # 呼び出し元側で別途、一定秒数以上であるか判定をすることで、
            # オン状態を維持したまま一定時間経過する事象を検出できます。
            if onboard.pushsw.hold_time() >= SW_HOLD_THRESHOLD_SECONDS:
                print('hold')

            # 一定時間待機
            # 処理 x を反復実行する際、チャタリング (押しボタンスイッチの
            # 機械接点の振動に伴うオン回数の多重認識) の影響を受けないように
            # 待ち時間の調節を行います。
            sleep(0.02)
    # Ctrl+C の入力でループから脱出
    except KeyboardInterrupt:
        print('Quit...')

    # 後始末をして終了
    onboard.clean()
    sys.exit(0)
