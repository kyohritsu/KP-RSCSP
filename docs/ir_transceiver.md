# 赤外線リモコンインターフェースの使用方法

## 概要

本文書では、「IoTスマートスピーカーモジュール」上の赤外線リモコンインターフェースをRaspberry Pi上で使用するための方法を説明します。

## 構成

本製品には、赤外線リモコン信号送信用の赤外LEDと、受信用のモジュールICが各1個搭載されています。Raspberry Pi 上でのGPIOポート接続位置は下表の通りです。

|    | GPIO番号 | ピン番号 |
|----|:--------:|:--------:|
| 送信用LED (LED6) | GPIO17 | 11 |
| 受信用IC (IC3) | GPIO4 | 7 |

## システムのセットアップ

Raspberry Pi上のシステムセットアップ方法を説明します。

対象LinuxディストリビューションはRaspbianです。(Raspbian Stretch with Desktop および Raspbian Stretch Lite 2018-03-14 で動作確認済み)

Raspberry Piにディスプレイとキーボードを接続してターミナルを起動するか、SSHでのリモートログインを行います。

## LIRCのインストール

赤外線リモコン信号送受信制御用ソフトウェア LIRC をインストールします。
下記はターミナルに入力するコマンドを示します。`~$` は現在のディレクトリを示すプロンプトの表記です。コマンドの入力には含めないでください。以下同様に表記します。

```sh
~$ sudo apt install lirc
```

LIRC モジュールの有効化を行います。

```sh
~$ sudo nano /boot/config.txt
```

テキストエディタ nano が開きます。`#dtoverlay=lirc-rpi` となっている行を探し、行頭の `#` を取り除いてコメントアウトを解除します。

更に、LIRC が参照する赤外線リモコン信号入力ピンと出力ピンの番号を記述します。先程変更した行のすぐ下に新しく `dtparam=gpio_in_pin=4` `dtparam=gpio_out_pin=17` の2行を追加します。ここまでの変更内容は下記のようになります。

```text
# Uncomment this to enable the lirc-rpi module
dtoverlay=lirc-rpi
dtparam=gpio_in_pin=4
dtparam=gpio_out_pin=17
```

編集完了後、(Ctrl+O) → Enter と入力して上書き保存し、(Ctrl+X) で nano を終了します。その後再起動を行います。

```sh
~$ sudo reboot
```

再起動後、デバイスファイルが存在するか下記のコマンドで確認します。結果にファイル名が表示されれば、ここまでの設定は完了です。  
`ls: cannot access '/dev/lirc*': No such file or directory` という表示の場合は、再度手順を見直してください。

```sh
~$ ls /dev/lirc*
```

## リモコンコードの学習

リモコンの学習前に、一時的に LIRC サービスを停止しておきます。

```sh
~$ sudo systemctl stop lircd.service lircd.socket
```

先程確認したデバイス名を指定し、リモコン信号記録プログラム `irrecord` を実行します。

```sh
~$ sudo irrecord -n -d /dev/lirc0
```

説明が表示されますので、Enter を入力してください。

```text
irrecord -  application for recording IR-codes for usage with lirc
Copyright (C) 1998,1999 Christoph Bartelmus(lirc@bartelmus.de)

This program will record the signals from your remote control
and create a config file for lircd.
(中略)
Please take the time to finish the file as described in
https://sourceforge.net/p/lirc-remotes/wiki/Checklist/ an send it
to  <lirc@bartelmus.de> so it can be made available to others.

Press RETURN to continue.
```

更に説明が表示されますので、再び Enter で続行します。

```text
Usually you should not create a new config file for devinput
devices. LIRC is installed with a devinput.lircd.conf file which
is built for the current system which works with all remotes
supported by the kernel. There might be a need to update
this file so it matches the current kernel. For this, use the
lirc-make-devinput(1) script.

Press RETURN to continue.
```

下記のメッセージが表示されますので、直射日光や蛍光灯、赤外線リモコン等からの外乱光が受信ICに入らないようにして、数秒お待ちください。

```text
Checking for ambient light  creating too much disturbances.
Please don't press any buttons, just wait a few seconds...
```

問題がなければ下記のメッセージが表示されます。

```
No significant noise (received 0 bytes)
```

続いて、設定するリモコンの識別名がたずねられますので、空白を含めない半角英数字で名前を付けて Enter を入力してください。
下記の例では `remote` としました。

```text
Enter name of remote (only ascii, no spaces) :remote
```

下記のメッセージが表示されますので、ここでリモコンを受信ICに向けて、任意のボタンを何度か押し続ける操作を行います。

学習させる予定の複数のボタンを満遍なく、押下時間約1秒程度をめやすにボタンを押してください。信号を受信する度にメッセージ上にドット `.` が順次表示されていきますので、これが 2 行ぶん (画面幅80文字) に達するまで継続してください。

```text
Using remote.lircd.conf as output filename

Now start pressing buttons on your remote control.

It is very important that you press many different buttons randomly
and hold them down for approximately one second. Each button should
generate at least one dot but never more than ten dots of output.
Don't stop pressing buttons until two lines of dots (2x80) have
been generated.

Press RETURN now to start recording.
```

途中で更にメッセージが表示されますが、そのまま続けます。

```text
................................................................................
Got gap (46100 us)}

Please keep on pressing buttons like described above.
...............................................................................
```

下記のような表示が現れれば、正しく認識されています。ここからボタンのコード登録を始めます。
最初に登録するボタンの名前をたずねられますので、名前を入力後 Enter を入力します。下記の例では `1` というボタン名を入力しています。

```text
Please enter the name for the next button (press <ENTER> to finish recording)
1
```

下記メッセージに従い、名前をつけたボタンを押し下げたままにします。

```text
Now hold down button "1".
```

認識が終了すると、次のボタンの名前がたずねられますので、リモコンのボタンを離して次のボタンの名前を入力します。

```text
Please enter the name for the next button (press <ENTER> to finish recording)
```

以上、名前入力 → ボタン押下を登録したいボタンの数だけ繰り返します。登録を終了するには、名前入力の際に何も文字を入れずに Enter を入力します。

次のメッセージが現れた場合、登録したボタンの信号にトグル・ビットが含まれないか検出を行う処理が始まります。これはエアコンの電源ボタン等にみられるような、押す度に信号の一部が交互に変化するタイプの信号を検出するための処理です。Enter を入力して次に進み、登録したボタンのうちいずれか1つを連続で短く押します (押したままにはしないでください)。認識する度に画面にドット `.` が現れます。もし現れない場合はボタンを押す間隔が短すぎるので、ボタンを離す時間を少し長めに取りながら押してください。

```text
Checking for toggle bit mask.
Please press an arbitrary button repeatedly as fast as possible.
Make sure you keep pressing the SAME button and that you DON'T HOLD
the button down!.
If you can't see any dots appear, wait a bit between button presses.

Press RETURN to continue.
```

検出が終了すると下記のメッセージが表示され、結果がファイル `remote.lircd.conf` に書き出されました。
  - ファイル名は最初に入力したリモコンの名前に応じて異なります。以降、各自設定した名前に読み替えてください。

```text
..............................Cannot find any toggle mask.

Successfully written config file remote.lircd.conf
```

ファイルの内容を確認します。下記は一例です。

```sh
~$ cat remote.lircd.conf
```

```text
# Please take the time to finish this file as described in
# https://sourceforge.net/p/lirc-remotes/wiki/Checklist/
# and make it available to others by sending it to
# <lirc@bartelmus.de>
(中略)
begin remote

  name  remote
  bits            8
  flags SPACE_ENC|NO_HEAD_REP|CONST_LENGTH
  eps            30
  aeps          100

  header       8417  4109
  one           574  1509
  zero          574   474
  ptrail        576
  pre_data_bits   8
  pre_data       0xC2
  gap          46100
  toggle_bit_mask 0x0
  frequency    38000

      begin codes
          1                        0x84
          2                        0x44
          3                        0xC4
          4                        0x24
          5                        0xA4
          6                        0x64
          7                        0xE4
          8                        0x14
          9                        0x94
          *                        0x6C
          0                        0xCC
          #                        0x09
      end codes

end remote
```

生成されたコードファイルを使用するため、LIRCのディレクトリにコピーします。

```sh
~$ sudo cp remote.lircd.conf /etc/lirc/lircd.conf.d/
```

停止していたLIRCサービスを再開します。

```sh
~$ sudo systemctl restart lircd.service lircd.socket
```

入力テストを行います。下記コマンドを実行し、先程登録したリモコンを受信ICに向け、ボタンを押してください。

下に結果の例を示します。左列から順番に［リモコン生コード］［長押し連続数］［ボタン名］［リモコン名］を表します。
  - テストを終了するには (Ctrl+C) を入力します。

```sh
~$ irw
```

```text
000000000000c284 00 1 remote
000000000000c284 01 1 remote
000000000000c284 02 1 remote
000000000000c284 03 1 remote
000000000000c284 04 1 remote
000000000000c284 00 1 remote
000000000000c284 01 1 remote
000000000000c284 02 1 remote
000000000000c284 03 1 remote
000000000000c244 00 2 remote
000000000000c244 01 2 remote
000000000000c244 02 2 remote
000000000000c244 03 2 remote
000000000000c2c4 00 3 remote
000000000000c2c4 01 3 remote
000000000000c2c4 02 3 remote
^C
```

## リモコンコード受信時のコマンド実行

リモコンコード受信時に特定のコマンドを実行するには、ホームディレクトリにファイル `.lircrc` を作成し、コードと実行コマンドの組み合わせを定義します。

```sh
~$ sudo nano ~/.lircrc
```

`.lircrc` の例を下に示します。`button = ` に登録したボタン名、`config = ` に実行するコマンドを記述します。`begin`〜`end` のブロックを、登録するボタン数だけ列挙します。

```text
begin
    prog = irexec
    button = 1
    config = echo "ボタン1が押されました"
end

begin
    prog = irexec
    button = 2
    config = echo "ボタン2が押されました"
end
```

リモコン入力を待機するには、`irexec` コマンドを起動します。実行中にリモコンコードを受信することで、コードに応じたコマンドが実行されます。

```sh
~$ irexec
```

```text
ボタン1が押されました
ボタン2が押されました
```

## リモコンコード送信

赤外線送信LEDを使用して、リモコンコードを送信することができます。

事前準備として、送信したいリモコンコードを上節「**リモコンコードの学習**」の手順に従い登録しておきます。

リモコンコードの送信には、`irsend` コマンドを実行します。下記の例は、リモコン名 `remote` のコード `1` を単発で送信するコマンドです。

```sh
~$ irsend SEND_ONCE remote 1
```
  - `SEND_ONCE` … 単発送信。コードを1回送信します。リモコンボタンを短く押す操作に相当
  - `SEND_START` … 連続送信開始。リピートコードを用いた連続送信を開始します。リモコンボタンを押し下げる操作に相当
  - `SEND_STOP` … 連続送信停止。リピートコードを用いた連続送信を開始します。リモコンボタンを離す操作に相当

**注意**  
リモコンコードの受信プロセス `irexec` を実行中に送信すると、送信したコードを基板上で近接する受信ICが拾う場合があります。
