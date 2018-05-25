# KP-RSCSP 常駐型ランチャーsystemdサービス

## 概要

「センサーコミュニケーション基板」(KP-RSCSP) のステータスLEDと押しボタンスイッチを使用した、ブート完了表示と指定コマンドのランチャー機能を担当するスクリプトです。

## 機能

サービスをインストールして有効化すると、Pythonスクリプト `rscsp_launcher.py` がバックグラウンドで動作します。このスクリプトの機能は下記の通りです。

  - **使用されるデバイス**  
    KP-RSCSP基板上の「ステータスLED」(LED7) と「押しボタンスイッチ」(SW1) が使用されます。
  - **ブート完了表示**  
    システムのブートが完了し、スクリプトが実行された時点で「ステータスLED」が点灯します。
  - **押しボタンスイッチによるランチャー機能**  
    押しボタンスイッチが押されて短時間で離されると、指定のコマンドを実行します。  
    また、5秒間の長押しでシステムのシャットダウンを実行します。

## インストール方法

### 1. 基板上デバイス制御用Pythonモジュールのインストール

[基板上デバイス制御用Pythonモジュール](https://github.com/kyohritsu/KP-RSCSP/tree/master/onboard)をまだインストールしていない場合は、最初にインストールしてください。

### 2. 実行コマンドの準備

次に、押しボタンスイッチが短時間で離された際に起動するプログラムの指定を変更するため、スクリプト本体を編集します。

```sh
  ~$ cd ~/KP-RSCSP/service/
  ~/KP-RSCSP/service$ nano rscsp_launcher.py
```

プログラム内の文字列変数 `COMMAND_ON_RELEASE` には、標準では Google Assistant SDK の提供するホットワード対応サンプルが設定されています。この時オプション指定するデバイスモデルIDは個人の環境で異なるため、お使いのものに置き換える必要があります。

```python
COMMAND_ON_RELEASE = ('. env/bin/activate && '
    'googlesamples-assistant-hotword --device_model_id my_rpi1')
```

上記実行コマンド変数を置き換えることで、Google Assistantに限らず他のコマンドを実行することもできます。その際は、多重起動防止のために事前実行するコマンド `PRECOMMAND_ON_RELEASE` の `pkill` 対象コマンド名も必要に応じて変更してください。

```python
PRECOMMAND_ON_RELEASE = 'pkill -f "googlesamples-assistant-hotword"'
```

### 3. `systemd` への登録

実行コマンドの編集後、スクリプトをLinuxブート時に自動起動するためにサービス化し、`systemd` へ登録します。

```sh
  ~/KP-RSCSP/service$ sudo cp ~/KP-RSCSP/service/rscsp.service /etc/systemd/system/
  ~/KP-RSCSP/service$ sudo systemctl enable rscsp.service
  ~/KP-RSCSP/service$ sudo systemctl start rscsp.service
```

### アンインストール方法

下記のコマンドで、登録したサービスを停止、無効化および削除します。

```sh
  ~$ sudo systemctl stop rscsp.service
  ~$ sudo systemctl disable rscsp.service
  ~$ sudo rm /etc/systemd/system/rscsp.service
```
