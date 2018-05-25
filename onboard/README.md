# KP-RSCSP 基板上デバイス制御用Pythonモジュール

## 概要

「センサーコミュニケーション基板」(KP-RSCSP) に搭載されたGPIO接続デバイスを制御するためのPython 3.x用モジュールです。

操作対象のデバイスは次の4種です。

  - **衛星LED** (部品番号：LED1, LED2, LED3, LED4)  
    基板外周部にある4個の赤色Φ3mm LEDです。  
    それぞれ個別で点灯／消灯操作に対応しています。
  - **RGB LED** (部品番号：LED5)  
    基板中央にある3色点灯タイプのΦ5mm LEDです。  
    赤・緑・青の各色個別で点灯／消灯操作に対応しています。
  - **ステータスLED** (部品番号：LED7)  
    基板端寄りにある緑色Φ3mm LEDです。  
    点灯／消灯操作に対応しています。
  - **押しボタンスイッチ** (部品番号：SW1)  
    一定間隔で読取り関数を実行することで、オンエッジ／オフエッジ／長押し持続時間を取得できます。

## 動作環境

動作確認済み環境は次の通りです。

### ハードウェア

  - Raspberry Pi 3 Model B
  - Raspberry Pi Model B+
  - Raspberry Pi Zero W / WH

### ソフトウェア

  + OS
    - Raspbian Stretch with Desktop または Raspbian Stretch Lite
  + Python 3.4.2、3.5.3
  + `RPi.GPIO` 0.6.3

## インストール方法

```sh
  ~$ git clone https://github.com/kyohritsu/KP-RSCSP
  ~$ cd KP-RSCSP/onboard/
  ~/KP-RSCSP/onboard$ sudo python3 setup.py install
```

### アンインストール方法

```sh
  ~$ sudo pip3 uninstall rscsp.onboard
```

## 使用方法

### モジュールのインポート

```python
from rscsp.onboard import onboard
```

### 関数リファレンス

#### 全般

| 関数名 | 概要 |
| :- | :- |
| `onboard.clean()` | 使用宣言したすべてのデバイスのリソースを解放します。プログラム終了の際に後始末として実行してください。 |

#### 衛星LED

| 関数名 | 概要 |
| :- | :- |
| `onboard.sat.use(num, value=None)` | `num` 番目の衛星LEDを使用宣言します。`value` はオプションで、出力初期値を設定する際に使用します。下項参照 |
| `onboard.sat.out(num, value)` | `num` 番目の衛星LEDを `value` の値に応じて操作します。1 (True) で点灯、0 (False) で消灯 |
| `onboard.sat.on(num)` | `onboard.sat.out(num, 1)` に同じ |
| `onboard.sat.off(num)` | `onboard.sat.out(num, 0)` に同じ |

#### RGB LED

| 関数名 | 概要 |
| :- | :- |
| `onboard.rgb.use(value=None)` | RGB LED (基板外周部のLED1～LED4) を使用宣言します。`value` はオプションで、出力初期値を設定する際に使用します。下項参照 |
| `onboard.rgb.out(value)` | RGB LEDを `value` の値に応じて操作します。`value` は3要素のリストで、先頭から順に赤、緑、青の順にそれぞれ 1 (True) で点灯、0 (False) で消灯 |

#### ステータスLED

| 関数名 | 概要 |
| :- | :- |
| `onboard.status.use(value=None)` | ステータスLEDを使用宣言します。`value` はオプションで、出力初期値を設定する際に使用します。下項参照 |
| `onboard.status.out(value)` | ステータスLEDを `value` の値に応じて操作します。1 (True) で点灯、0 (False) で消灯 |
| `onboard.status.on()` | `onboard.status.out(1)` に同じ |
| `onboard.status.off()` | `onboard.status.out(0)` に同じ |

#### 押しボタンスイッチ

| 関数名 | 概要 |
| :- | :- |
| `onboard.pushsw.use()` | 押しボタンスイッチを使用宣言します。 |
| `onboard.pushsw.capture()` | 押しボタンスイッチの現在状態を取得します。戻り値はオフの場合 0、オンの場合 1 です。 |
| `onboard.pushsw.on_edge()` | 直前の `onboard.pushsw.capture()` 実行の際、オンエッジ (オフからオンへの変化) を検出したか確認します。戻り値は不検出の場合 0、検出した場合 1 です。 |
| `onboard.pushsw.off_edge()` | 直前の `onboard.pushsw.capture()` 実行の際、オフエッジ (オンからオフへの変化) を検出したか確認します。戻り値は不検出の場合 0、検出した場合 1 です。 |
| `onboard.pushsw.hold_time()` | 直前の `onboard.pushsw.capture()` 実行の際、検出した長押し時間を取得します。戻り値はオン状態を維持したまま経過した時間 (単位：秒) です。ただし、現在状態がオフの場合は 0 となります。 |

各デバイスのサンプルプログラムを `examples/` 内に収録しています。あわせてご参照ください。
