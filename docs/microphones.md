# MEMS マイクの使用方法

## 概要

本文書では、「IoTスマートスピーカーモジュール」上のMEMSマイク (MC1, MC2) をRaspberry Pi上で使用するための方法を説明します。

## 構成

本製品には、I2S (Inter-IC Sound) 接続のMEMSマイクが2個搭載されています。Raspberry Pi上では、2個のマイクの入力を合成したモノラル音声や、左右独立したチャンネルを持つステレオ音声を録音することができます。

## システムのセットアップ

Raspberry Pi上のシステムセットアップ方法を説明します。

対象LinuxディストリビューションはRaspbianです。(2019-09-26-raspbian-buster で動作確認済み)

  - 以下のセットアップ手順に関する説明は、下記文書の情報を基にして作成されています。  
    [Adafruit Learning System: I2S MEMS Microphone Breakout - Raspberry Pi Wiring & Test](https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-and-test)

### 1. 準備

Raspberry Piにディスプレイとキーボードを接続してターミナルを起動するか、SSHでのリモートログインを行います。

### 2. I2S の有効化

MEMSマイクを接続するI2Sインターフェースは初期状態で無効となっているため、有効化を行います。
下記はターミナルに入力するコマンドを示します。`~$` は現在のディレクトリを示すプロンプトの表記です。コマンドの入力には含めないでください。以下同様に表記します。

```sh
~$ sudo nano /boot/config.txt
```

テキストエディタ nano が開きます。`#dtparam=i2s=on` となっている行を探し、行頭の `#` を取り除いてコメントアウトを解除します。その後、(Ctrl+O) → Enter と入力して上書き保存し、(Ctrl+X) で nano を終了します。

### 3. サウンドモジュールの有効化

次に、Raspberry Piが搭載するチップセット内蔵のサウンド機能を有効化します。再び nano を実行し、設定ファイルを開きます。

```sh
~$ sudo nano /etc/modules
```

ファイルの末尾に `snd-bcm2835` という行を追加し、上書き保存してから終了します。完了後、再起動します。

```sh
~$ sudo reboot
```

再起動後にターミナルを開き、下記のコマンドを入力して `snd-bcm2835` モジュールがロードされていることを確認します。

```sh
~$ lsmod | grep snd
```

結果に `snd_bcm2835` から始まる行があれば成功です。

### 4. Linuxカーネルのダウンロード

新しい I2S オーディオドライバを組み込む際に使用するLinuxカーネルを入手します。まず、現在のRaspbianを最新バージョンのカーネルに更新します。

更新用プログラム `rpi-update` をインストールし、実行します。

```sh
~$ sudo apt update
~$ sudo apt install rpi-update
~$ sudo rpi-update
```

完了後、再起動します。

```sh
~$ sudo reboot
```

### 5. 作業に関わる依存パッケージのインストール

カーネルの取得・コンパイルに必要となる依存パッケージをインストールします。

```sh
~$ sudo apt install git bc libncurses5-dev bison flex libssl-dev
```

Linuxカーネルのダウンローダー `rpi-source` を取得し、実行して最新版のビルド済みカーネルをダウンロードします。

```sh
~$ sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
~$ sudo chmod +x /usr/bin/rpi-source
~$ /usr/bin/rpi-source -q --tag-update
~$ rpi-source --skip-gcc
```

カーネルのダウンロードには長い時間がかかります。Raspberry Pi 3の場合で15分以上、Raspberry Pi Zero等では1時間以上かかる場合もあります。ダウンロード中はターミナルに進捗状況が表示されますので、もし途中でダウンロード失敗した場合は、下記のコマンドを実行して残った途中のファイルを削除後再試行してください。

```sh
~$ rm linux-*.tar.gz
~$ rm -R linux-*
~$ sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
~$ sudo chmod +x /usr/bin/rpi-source
~$ /usr/bin/rpi-source -q --tag-update
~$ rpi-source --skip-gcc
```

### 6. I2S サウンドモジュールのコンパイル

I2S サウンドモジュールのコンパイル前に、Linuxカーネル上のASoCプラットフォーム上でI2Sデバイスをサポートする準備が整っているか確認を行います。下記のコマンドを実行してください。

```sh
~$ sudo mount -t debugfs debugs /sys/kernel/debug
```

環境によっては上記のコマンドの結果、`mount: debugs is already mounted or /sys/kernel/debug busy` と表示されますが、このまま次に進んでください。

次のコマンドを実行し、実行結果の中に下記の行が含まれていれば、問題なく準備ができています。

```sh
~$ sudo cat /sys/kernel/debug/asoc/components
```

```text
3f203000.i2s
snd-soc-dummy
```

  - **Raspberry Pi 3 (Model B+/B) / 2 (Model B)** の場合:  
    `3f203000.i2s`
  - **Raspberry Pi Zero (W)(WH) / 1 (初代) (Model B+/A+)** の場合:  
    `20203000.i2s`

サウンドモジュールのソースコードをダウンロードします。

```sh
~$ git clone https://github.com/PaulCreaser/rpi-i2s-audio
~$ cd rpi-i2s-audio
```

- **お使いのRaspberry PiがZeroシリーズまたは初代 Model B+、A+** (搭載SoCがBCM2835の機種) **の場合**
  コンパイル前にソースファイル `my_loader.c` に変更を加えます。それ以外の場合はこの手順をスキップして、モジュールのコンパイルに進んでください。
```sh
~/rpi-i2s-audio$ nano my_loader.c
```

  nano で下記の記述を書き換え、上書き保存して終了します。

  - `.platform = "3f203000.i2s"` → `.platform = "20203000.i2s"`
  - `.name = "3f203000.i2s"` → `.name = "20203000.i2s"`

モジュールをコンパイルし、インストールを行います。

```sh
~/rpi-i2s-audio$ make -C /lib/modules/$(uname -r)/build M=$(pwd) modules
~/rpi-i2s-audio$ sudo insmod my_loader.ko
```

下記2通りの方法でモジュールが正常にインストールできたことを確認してください。

1. `lsmod` を実行し、`my_loader` で始まる行が出力されること。
```sh
~/rpi-i2s-audio$ lsmod | grep my_loader
```

2. `dmesg` を実行し、カーネルメッセージログの最後に下記の内容を含む行が表示されていること。
```sh
~/rpi-i2s-audio$ dmesg | tail
```
```text
asoc-simple-card asoc-simple-card.0: snd-doc-dummy-dai <-> 3d203000.i2s mapping ok
```

以上で現在実行中のカーネルへモジュールがインストールされました。ただし、現在の状態ではRaspberry Piを再起動することでモジュールがインストールされていない状態に戻ります。

### 7. 起動時に自動でモジュールをロード

Raspberry Piを起動する度にモジュールをロードするには、下記コマンドを実行してください。

```sh
~/rpi-i2s-audio$ sudo cp my_loader.ko /lib/modules/$(uname -r)
~/rpi-i2s-audio$ echo 'my_loader' | sudo tee --append /etc/modules > /dev/null
~/rpi-i2s-audio$ sudo depmod -a
~/rpi-i2s-audio$ sudo modprobe my_loader
```

完了後、再起動します。

```sh
~/rpi-i2s-audio$ sudo reboot
```

## 録音デバイスの確認

下記のコマンドで、ALSAプラットフォーム上でのMEMSマイクの認識状況を確認します。

```sh
~$ arecord -l
```

出力例は下記のようになります。この場合は、カード番号**1**、デバイス番号**0**で認識されています。

```text
**** List of CAPTURE Hardware Devices ****
card 1: sndrpisimplecar [snd_rpi_simple_card], device 0: simple-card_codec_link snd-soc-dummy-dai-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

## 録音の実行

上記結果時のモノラル録音コマンドは下記の通りです。

`-D` オプションで録音デバイスを指定します。カード番号やデバイス番号が例と異なる場合は、適宜変更してください。後続のオプションは下記の通りです。
  - `-c` 録音チャンネル数 … 1
  - `-r` サンプルレート指定 … 48000
  - `-f` サンプル形式指定 … 32ビット/リトルエンディアン (下位バイト先行)
  - `-t` ファイルフォーマット … Microsoft WAV
  - `-V` 録音時に表示されるレベルメーターの方式 … モノラル
  - `-v` 出力先ファイル指定 … `file.wav`

```sh
~$ arecord -D plughw:1,0 -c1 -r 48000 -f S32_LE -t wav -V mono -v file.wav
```

ステレオ録音を行う場合は下記のコマンドを使います。

```sh
~$ arecord -D plughw:1,0 -c2 -r 48000 -f S32_LE -t wav -V stereo -v file_stereo.wav
```
