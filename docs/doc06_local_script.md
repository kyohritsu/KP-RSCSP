# アシスタントアプリの開発 (6) ローカルスクリプトの作成

本製品「センサーコミュニケーション基板」を通してセンサーや出力装置が接続された、手元のRaspberry Pi上で動作させる制御用ローカルスクリプトの設計方針と、開発作業の準備に必要な手順を説明します。

## ローカルスクリプトの機能

ローカルスクリプトは、下記の機能を備えた常時稼働型のプログラムとして設計します。

  1. データベースへセンサー状態をアップロード  
     各種センサー入力を読み取り、Firebase Realtime Database サービス (以下、データベースと呼びます) に保存します。そうすることで、先に作成したアシスタントアプリのフルフィルメントから結果を取り出せるようになります。
       - 水分センサーと温湿度センサーの2種については、一定間隔ごとの定期的に指示値とタイムスタンプのペアをデータベースへ書き込みます。
       - PIRモーションセンサーと加速度センサーの2種については、それぞれが変化を検知した時に限り、検知時刻のタイムスタンプをデータベースへ書き込みます。
  2. データベースを監視し、リレー状態を反映  
     フルフィルメントが出力変更をデータベースに書き込む事象を監視し、変化が発生した際にリレーの出力を操作します。

## 事前準備

以下の作業を開始する前に、**Raspberry Piにセンサーコミュニケーション基板を接続**してください。

![基板写真](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/board.jpg)

## GrovePi ソフトウェアのセットアップ

「センサーコミュニケーション基板」のセンサー接続インターフェースは、Seeed Studio 製 [GrovePi+](http://wiki.seeedstudio.com/GrovePi_Plus/) 互換となっています。インターフェースAVRマイコンのファームウェアや、各プログラミング言語向けのGroveモジュール制御用ライブラリソフトウェアは、GrovePiが提供するものを利用します。

GrovePi ソフトウェア
  - https://github.com/DexterInd/GrovePi

上記ページの説明に従い、GrovePi ソフトウェアのインストールを行います。下記のコマンドを実行してください。

```sh
  ~$ cd ~
  ~$ sudo curl -kL dexterindustries.com/update_grovepi | bash
```

基板上のAVRマイコンのファームウェアを書き込みます。

```sh
  ~$ cd Dexter/GrovePi/Firmware
  ~/Dexter/GrovePi/Firmware$ sudo ./firmware_update.sh
```

下記の表示が出てファームウェアの書き込みを行う際の確認がされますので、`y` と入力し、その後いずれかのキーを押して続行します。

```text
  Do you want to update the firmware? [y,n]
    → y と入力します。
  Make sure that GrovePi is connected to Raspberry Pi
  Firmware found
  Press any key to start firmware update
  . . .
    →ここでいずれかのキーを押します。
```

始めてファームウェアを書き込む際は、途中でヒューズバイトの変更を行ってもよいか確認がされますので、`y` を入力して続けてください。

```text
  avrdude: safemode: hfuse changed! Was d9, and is now ff
  Would you like this fuse to be changed back? [y/n]
    → y と入力します。
```

下記のようにエラーなく処理が完了すれば成功です。

```text
  avrdude: verifying ...
  avrdude: 13816 bytes of flash verified

  avrdude: safemode: Fuses OK

  avrdude done.  Thank you.
```

終了後はホームディレクトリに戻ります。

```sh
  ~/Dexter/GrovePi/Firmware$ cd ~
```

## Pyrebase のインストール

Pyrebaseは、James Childs-Maidment氏によって開発されたPython 3.x用のFirebase APIアクセスライブラリです。

  - https://github.com/thisbejim/Pyrebase

Python 3.x 用の pip (パッケージマネージャ) をインストールした後、pip 経由で
`pyrebase` をインストールします。

更に、`google-auth-oauthlib` を最新版にアップグレードします。

```sh
  ~$ sudo apt install python3-pip
  ~$ sudo pip3 install pyrebase
  ~$ sudo pip3 install --upgrade google-auth-oauthlib
```

## 作業ディレクトリの作成

ローカルスクリプト用の作業ディレクトリを作成します。今回はリポジトリをクローンした際につくられたディレクトリを使用します。

```sh
  ~$ cd ~/KP-RSCSP/sensorlab/local_script/
```

## 必要事項の取得

### 認証情報の確認

ローカルスクリプトからFirebase APIにアクセスするために必要な認証情報を確認します。用意するのは下記の3項目です。

| 名称 | 種別 |
| :- | :- |
| **プロジェクト ID** | 文字列 |
| **ウェブ API キー** | 文字列 |
| **サービス アカウントの秘密鍵** | JSONファイル |

開発用のGoogleアカウントにログインした状態で、下記のURLにアクセスします。ここまでに作成したアシスタントアプリのプロジェクトが一覧に表示されていることを確認してください。

  - https://console.firebase.google.com/

![Firebase ConsoleのOverview画面](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig014.png)

《センサーラボ》用のプロジェクトをクリックして開きます。

Firebaseでプロジェクトを初めて開く際は、利用規約の同意が必要となります。ポップアップが表示された場合は、リンク先の規約を確認した上で☑マークを入れ、［次へ］をクリックしてください。

![規約への同意画面](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig015.png)

画面左のメニュー (表示されない場合は、≡ マークをクリック) から、Project Overview 横の歯車マークを選択し、プロジェクトの設定 ＞ 全般 と進みます。

この画面内にある「**プロジェクト ID**」「**ウェブ API キー**」を控えておきます。

![プロジェクト IDとウェブ API キーの確認](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig021.png)

次に、サービス アカウントをクリックします。この画面では、Firebase Admin SDKを使用した秘密鍵データの生成とダウンロードを行うことができます。

![サービス アカウント ](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig022.png)

［新しい秘密鍵の生成］、次に［キーを生成］をクリックします。**秘密鍵JSONファイル**がダウンロードされますので、お使いのPCに保存します。

![新しい秘密鍵の生成](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig023.png)

保存したJSONファイルを、SCP等を利用してRaspberry Piに転送します。保存先は問いません。後にスクリプトから参照しますので、管理しやすい場所を指定してください。

![秘密鍵JSONのSCP転送](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig024.png)

![秘密鍵JSONのSCP転送先の指定](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig025.png)

※**警告**  
この秘密鍵はFirebaseサービスの全権限に関連するものであるため、**決して公開しない**ようにしてください。万一流出した可能性のある場合は、必ず**同操作をもう一度実行**して秘密鍵を更新してください。

## 認証情報の指定

ローカルスクリプト本体 `~/KP-RSCSP/sensorlab/local_script/local_script.py` を編集します。

### 《センサーラボ》のローカルスクリプト

最終的なローカルスクリプトの完成形は、こちらを参照してください。→ [`sensorlab/local_script/`](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/local_script)

スクリプト内の下記の認証情報を格納する変数を、個人のプロジェクトにあわせた値に変更してください。

```python
# ウェブ API キー
WEB_API_KEY = 'AIza***********************************'
# プロジェクト ID
PROJECT_ID = 'yourproject-1e84f'
# 秘密鍵 JSON ファイルへのパス
PATH_TO_CREDENTIAL_JSON = '/home/pi/path/to/credential.json'
```

秘密鍵JSONへのパス `PATH_TO_CREDENTIAL_JSON` には、先程転送した秘密鍵JSONファイルへのパスを入力します。

## Groveモジュールの接続

本製品基板の**モジュール接続コネクタ** (CN3 - CN8) に下記のGroveモジュールを接続します。モジュールは5つ全て揃える必要はありません。一部のみでもかまいません。

| 部品番号 | コネクタ名 | モジュール |
| :--: | :--: | :-- |
| CN3 | I2C0 | *接続なし* |
| CN4 | I2C1 | 3軸加速度センサー ([Grove - 3-Axis Digital Accelerometer(±1.5g)](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-1.5g/)) |
| CN5 | A0 | 水分センサー ([Grove - Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)) |
| CN6 | A2 | PIRモーションセンサー ([Grove - PIR Motion Sensor](http://wiki.seeedstudio.com/Grove-PIR_Motion_Sensor/)) |
| CN7 | D0 | デジタル温湿度センサー ([Grove - Temperature & Humidity Sensor](http://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)) |
| CN8 | D2 | リレー ([Grove - Relay](http://wiki.seeedstudio.com/Grove-Relay/)) |

![モジュール接続図](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/modules.jpg)

## ローカルスクリプトの実行

Groveモジュールを上記通りのコネクタに接続し、認証情報を個人の内容に置き換えた後は、ローカルスクリプトを実行します。

```sh
  ~/KP-RSCSP/sensorlab/local_script$ python3 local_script.py
```

スクリプトは、データベースへの接続に成功すると、下記に示す一連の動作を並行して行います。
  - 定期的な温湿度と水分データの送信
  - PIRモーションセンサーと加速度センサーは、検知したタイミングで随時送信
  - リレー状態を監視し、変化があれば出力の変更

このスクリプトが動作している間は、以上の動作によってアプリとの連動が保たれます。終了するには、`^C` ([Ctrl]+[C]) を2度続けて入力してください。
