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
import time
import RPi.GPIO as gpio

class Onboard:
    '''各種基板上デバイス操作用ライブラリ'''

    class SatelliteLed:
        '''衛星LEDサブクラス'''

        # 衛星LED 1..4 のGPIO番号 (BOARD = [32, 33, 36, 15])
        BCM = [12, 13, 16, 22]

        def __init__(self, super):
            '''衛星LEDサブクラスのコンストラクタ'''
            self.super = super

        def use(self, num, value=None):
            '''指定番号の衛星LEDを使用開始する
            位置引数
                num - 衛星LEDの番号：有効値は1..4、それぞれLED1..LED4に対応
            キーワード引数
                value - (オプション) 初期の出力値：Trueで点灯、Falseで消灯
            戻り値 - なし
            '''
            try:
                if 1 <= num <= 4:
                    if self.BCM[num - 1] not in self.super.used_pins:
                        self.super.used_pins.append(self.BCM[num - 1])
                        gpio.setup(self.BCM[num - 1], gpio.OUT)
                        if value is not None:
                            self.out(num, value != 0)
                    else:
                        raise IOError('error: LED%d pin is already declared to'
                            ' be used' % num)
                else:
                    raise ValueError('error: no such device LED%d' % num)
            except ValueError as e:
                print(e)
            except IOError as e:
                print(e)

        def out(self, num, value):
            '''指定番号の衛星LEDに対し、出力を操作する
            位置引数
                num - 衛星LEDの番号：有効値は1..4、それぞれLED1..LED4に対応
                value - 出力値：Trueで点灯、Falseで消灯
            戻り値 - なし
            '''
            try:
                if 1 <= num <= 4:
                    if self.BCM[num - 1] in self.super.used_pins:
                        gpio.output(self.BCM[num - 1], value != 0)
                    else:
                        raise IOError('error: LED%d pin is not declared to '
                            'be used' % num)
                else:
                    raise ValueError('error: no such device LED%d' % num)
            except IOError as e:
                print(e)
            except ValueError as e:
                print(e)

        def on(self, num):
            '''指定番号の衛星LEDを点灯する
            位置引数
                num - 衛星LEDの番号：有効値は1..4、それぞれLED1..LED4に対応
            戻り値 - なし
            '''
            self.out(num, True)

        def off(self, num):
            '''指定番号の衛星LEDを消灯する
            位置引数
                num - 衛星LEDの番号：有効値は1..4、それぞれLED1..LED4に対応
            戻り値 - なし
            '''
            self.out(num, False)

    class RGBLed:
        '''RGB LEDサブクラス'''

        # 赤, 緑, 青各チャンネルのGPIO番号 (BOARD = [16, 18, 22])
        BCM = [23, 24, 25]

        def __init__(self, super):
            '''RGB LEDサブクラスのコンストラクタ'''
            self.super = super

        def use(self, value=None):
            '''RGB LEDを使用開始する
            キーワード引数
                value - (オプション) 初期の出力値：長さ3のリスト
                    0番要素…赤、1番要素…緑、2番要素…青
                    それぞれTrueで点灯、Falseで消灯
            戻り値 - なし
            '''
            try:
                if all([i not in self.super.used_pins for i in self.BCM]):
                    for i in self.BCM:
                        self.super.used_pins.append(i)
                    gpio.setup(self.BCM, gpio.OUT)
                    if value is not None:
                        if isinstance(value, list):
                            gpio.output(self.BCM, [i == 0 for i in value])
                else:
                    raise IOError('error: one or more of RGB LED pins are '
                        'already declared to be used')
            except IOError as e:
                print(e)

        def out(self, value):
            '''RGB LEDに対し、出力を操作する
            位置引数
                value - (オプション) 初期の出力値：長さ3のリスト
                    0番要素…赤、1番要素…緑、2番要素…青
                    それぞれTrueで点灯、Falseで消灯
            戻り値 - なし
            '''
            try:
                if all([i in self.super.used_pins for i in self.BCM]):
                    gpio.output(self.BCM, [i == 0 for i in value])
                else:
                    raise IOError('error: one or more of RGB LED pins are not '
                        'declared to be used')
            except IOError as e:
                print(e)

    class StatusLed:
        '''ステータスLEDサブクラス'''

        # ステータスLEDのGPIO番号 (BOARD = 37)
        BCM = 26

        def __init__(self, super):
            '''ステータスLEDサブクラスのコンストラクタ'''
            self.super = super

        def use(self, value=None):
            '''ステータスLEDを使用開始する
            キーワード引数
                value - (オプション) 初期の出力値：Trueで点灯、Falseで消灯
            戻り値 - なし
            '''
            try:
                if self.BCM not in self.super.used_pins:
                    self.super.used_pins.append(self.BCM)
                    gpio.setup(self.BCM, gpio.OUT)
                    if value is not None:
                        gpio.output(self.BCM, value != 0)
                else:
                    raise IOError('error: status LED pin is already declared '
                        'to be used')
            except IOError as e:
                print(e)

        def out(self, value):
            '''ステータスLEDに対し、出力を操作する
            位置引数
                value - 出力値：Trueで点灯、Falseで消灯
            戻り値 - なし
            '''
            try:
                if self.BCM in self.super.used_pins:
                    gpio.output(self.BCM, value != 0)
                else:
                    raise IOError('error: status LED pin is not declared to '
                        'be used')
            except IOError as e:
                print(e)

        def on(self):
            '''ステータスLEDを点灯する
            戻り値 - なし
            '''
            self.out(True)

        def off(self):
            '''ステータスLEDを消灯する
            戻り値 - なし
            '''
            self.out(False)

    class PushSwitch:
        '''押しボタンスイッチサブクラス'''

        # 押しボタンスイッチのGPIO番号 (BOARD = 31)
        BCM = 6

        def __init__(self, super):
            '''押しボタンスイッチのコンストラクタ'''
            self.super = super
            self.last_hold = None
            self.last_capture = None
            self.on_count = 0
            self.off = 0

        def use(self):
            '''押しボタンスイッチを使用開始する
            戻り値 - なし
            '''
            try:
                if self.BCM not in self.super.used_pins:
                    self.super.used_pins.append(self.BCM)
                    gpio.setup(self.BCM, gpio.IN, pull_up_down=gpio.PUD_UP)
                else:
                    raise IOError('error: push switch pin is already declared '
                        'to be used')
            except IOError as e:
                print(e)

        def capture(self):
            '''押しボタンスイッチの入力を読取り、エッジ検出/長押し判定を実行
            戻り値 - bool：今回入力がオンであればTrue、オフであればFalse
            '''
            result = None
            try:
                if self.BCM in self.super.used_pins:
                    self.last_capture = time.time()
                    result = gpio.input(self.BCM)
                    if result != 0:
                        # オフ時：
                        # オン持続回数をクリアし、長押し開始時刻を消去
                        # オフ検出フラグには直前のオン持続回数をコピー
                        self.off = self.on_count
                        self.on_count = 0
                        self.last_hold = None
                    else:
                        # オン時：
                        # オン持続回数を加算 (初回の場合、長押し開始時刻保存)
                        # オフ検出フラグはクリア
                        self.off = 0
                        self.on_count += 1
                        if self.on_count == 1:
                            self.last_hold = self.last_capture
                else:
                    raise IOError('error: push switch pin is not declared to '
                        'be used')
            except IOError as e:
                print(e)
            return result

        def on_edge(self):
            '''押しボタンスイッチの前回読取り時、オンエッジが検出されたか調べる
            戻り値 - bool：オンエッジ検出時True、不検出時False
            '''
            return self.on_count == 1

        def off_edge(self):
            '''押しボタンスイッチの前回読取り時、オフエッジが検出されたか調べる
            戻り値 - bool：オフエッジ検出時True、不検出時False
            '''
            return self.off > 0

        def hold_time(self):
            '''押しボタンスイッチの長押し継続時間を調べる。
            戻り値 - float：長押し開始から現在までの継続時間。
                長押し継続中でない場合はNone
            '''
            result = 0
            try:
                result = self.last_capture - self.last_hold
            except TypeError:
                pass
            return result

    def __init__(self):
        '''クラス Onboard のコンストラクタ'''
        gpio.setmode(gpio.BCM)
        # 使用中ピンリストの初期化
        Onboard.used_pins = []
        # 各サブクラスのインスタンス生成
        self.sat = self.SatelliteLed(self)
        self.rgb = self.RGBLed(self)
        self.status = self.StatusLed(self)
        self.pushsw = self.PushSwitch(self)

    def clean(self):
        '''使用したピンのGPIOリソースを解放する'''
        gpio.cleanup(self.used_pins)
        self.used_pins = []

if __name__ == '__main__':
    print('This file should be imported from other script')
else:
    onboard = Onboard()
