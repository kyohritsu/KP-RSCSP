# アシスタントアプリの開発 (5) フルフィルメントの作成

アシスタントアプリに連携して動作するフルフィルメントを、Firebase Cloud Functionsを利用して開発するための準備手順を説明します。

## フルフィルメントとは

前節と説明が重複しますが、Dialogflowエージェントにおけるフルフィルメント (Fulfillment) のおさらいをします。

アシスタントアプリの会話で、指定のインテントが発生された際、外部のサービス上にホスティングされたクラウド関数を呼び出すように設定できます。この関数をフルフィルメントと呼び、アプリから送られたリクエストに応じ、アプリへレスポンスを返す処理をDialogflowに代わって受け持ちます。

Google アシスタントアプリでは、外部サービスへの接続や連携に関する動作を行う場合には、同社が提供するFirebaseサービスの一部である**Firebase Cloud Functions**が簡単に利用できるようになっています。

## Firebaseのセットアップ

開発用のGoogleアカウントにログインした状態で、下記のURLにアクセスします。ここまでに作成したアシスタントアプリのプロジェクトが一覧に表示されていることを確認してください。

  - https://console.firebase.google.com/

![Firebase ConsoleのOverview画面](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig014.png)

《センサーラボ》用のプロジェクトをクリックして開きます。

Firebaseでプロジェクトを初めて開く際は、利用規約の同意が必要となります。ポップアップが表示された場合は、リンク先の規約を確認した上で☑マークを入れ、［次へ］をクリックしてください。

![規約への同意画面](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig015.png)

## 開発環境の構築

フルフィルメントはNode.js上で動作する関数であり、JavaScriptまたはTypescriptのプログラミング言語を使用して開発します。
開発には、Node.jsが動作するWindows、macOS、Linux環境のいずれかを使用します。今回の《センサーラボ》は最終的にRaspberry Piで計測用のローカルスクリプトを動作させるため、これらの環境構築も便宜上Raspberry Pi上で行います。

お持ちのRaspberry Piをインターネットに接続可能な状態までセットアップし、SSHで接続するか、デスクトップ環境からターミナルを起動してください。

### 1. Node.js のインストール

FirebaseのセットアップにはNode.jsが必要です。Node.jsをインストールして、`node` および `npm` コマンドが使えるようにしておきます。

インストールするバージョンは、Firebaseが実際にクラウド関数を実行している環境と同一である「v6.14.0」に合わせることを推奨します。
※2018年4月25日現在の実行環境です。Firebaseのソフトウェア実行環境は定期的に更新されますので、最新情報は[公式ドキュメント](https://firebase.google.com/docs/functions/get-started?hl=ja)を確認してください。

お使いのRaspberry Piのシリーズにあわせて、下記コマンドを1行ずつ実行してください。(各行頭の `~$` 等はカレントディレクトリおよびプロンプトを表します。実際に入力するコマンドには**含まれません**)

  - Raspberry Pi **2**/**3** の場合
```sh
  ~$ wget http://nodejs.org/dist/v6.14.0/node-v6.14.0-linux-armv7l.tar.xz
  ~$ tar Jxvf node-v6.14.0-linux-armv7l.tar.xz
  ~$ cd node-v6.14.0-linux-armv7l/
  ~/node-v6.14.0-linux-armv7l$ sudo cp -r bin/ include/ lib/ share/ /usr/local/
```
  - Raspberry Pi **1** / **Zero**シリーズの場合
```sh
  ~$ wget http://nodejs.org/dist/v6.14.0/node-v6.14.0-linux-armv6l.tar.xz
  ~$ tar Jxvf node-v6.14.0-linux-armv6l.tar.xz
  ~$ cd node-v6.14.0-linux-armv6l/
  ~/node-v6.14.0-linux-armv6l$ sudo cp -r bin/ include/ lib/ share/ /usr/local/
```

### 2. `firebase-tools` をインストール

Firebaseのセットアップに使用する対話型ツールは、NPMの `firebase-tools` パッケージに含まれています。下記コマンドを実行し、グローバルインストールしてください。

```sh
  ~$ npm install -g firebase-tools
```

### 3. 作業ディレクトリを作成
アシスタントアプリ用フルフィルメントの作業を行うためのディレクトリを作成します。ここでは、リポジトリのクローン時に作成されたディレクトリ `~/KP-RSCSP/sensorlab/fulfillment` を使用します。

```sh
  ~$ cd ~/KP-RSCSP/sensorlab/fulfillment
```

### 4. Firebaseへログイン

Firebaseへのログインを行います。

```sh
  ~/KP-RSCSP/sensorlab/fulfillment$ firebase login --no-localhost
```

対話形式で手順を進行します。

```text
  ? Allow Firebase to collect anonymous CLI usage...
     →匿名での調査に協力するかどうか、任意で選択して [Enter] を入力します。
  Visit this URL on any device to log in:
  https://accounts.google.com/o/oauth2/auth?client_id=...
     →表示されたURLをお使いのブラウザーでアクセスします。Raspberry Piに
       SSHで接続しているPCでも、それ以外の端末でもかまいません。
       作成途中のアシスタントアプリが存在するGoogleアカウントに
       ログインしている事を確認し、Firebase CLIに対してアクセスリクエストの
       許可を行います。
  ? Paste authorization code here:
     →移動したページに表示された認証コードをペーストし、[Enter] を入力します。
  ✔ Success! Logged in as ....@gmail.com
```

![Firebase CLIログイン認証画面へのURL](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig016.png)

![Firebase CLIに対するアクセス リクエストの許可](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig017.png)

お使いのGoogleアカウントでログインが出来た旨が表示されれば、使用アカウントでの連携は完了です。

### 5. Firebaseプロジェクトのセットアップ

作業ディレクトリ上で、Firebase Cloud Functionsプロジェクトのセットアップを行います。引き続き `fulfillment` 内で、下記のコマンドを実行します。

```sh
  ~/KP-RSCSP/sensorlab/fulfillment$ firebase init
```

再度対話形式で進めます。

```text
  ? Which Firebase CLI features do you want to setup for this folder? ...
    →[↓][↑] キーでカーソルを操作し、Functions にカーソル合わせて
      [Space] キーで選択し、[Enter] で決定
  ? Select a default Firebase project ...
    →[↓][↑] キーで作成したアシスタントアプリのプロジェクトを選択し [Enter]
      を入力します。プロジェクトが選択肢に表示されない場合、アプリを作成中の
      Googleアカウントでログインされていない可能性があります。[Ctrl]+[C] で
      一度コマンドを終了し、手順 4. からやり直してください。
  ? What language would you like to use to write Cloud Functions?
     →ここではJavaScriptで説明します。JavaScriptを選択して [Enter]
  ? Do you want to use ESLint to catch probable bugs and enforce style?
     →ESLintによるコーディング規約を適用するかどうか、選択します。
       ここではNoを選びます。n [Enter] と入力してください。
  ? Do you want to install dependencies with npm now?
     →npm を使って、Cloud Functionsに必要な依存パッケージをインストールします。
       y [Enter] と入力し、処理が完了するのを待ちます。
  ✔ Firebase initialization complete!
```

### 6. 追加の依存パッケージをインストール

フルフィルメントでは、手順 5. でインストールされたNPMパッケージの他に `actions-on-google` を使用するため、インストールした上で依存関係リストに追加します。

`functions` ディレクトリの中で下記のコマンドを実行してください。

```sh
  ~/KP-RSCSP/sensorlab/fulfillment$ cd functions/
  ~/KP-RSCSP/sensorlab/fulfillment/functions$ npm install actions-on-google --save
```

以上でセットアップは終了です。

## フルフィルメントのコーディング

フルフィルメントの実装を記述するソースファイルは、作業ディレクトリの `functions/index.js` に雛形が生成されています。これを編集します。

### 《センサーラボ》のフルフィルメント

最終的なフルフィルメントの完成形は、こちらを参照してください。→ [`sensorlab/fulfillment/`](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/fulfillment)

## フルフィルメントのデプロイ

フルフィルメントの記述が完了したら、プロジェクト上にデプロイします。下記のコマンドを実行してください。

```sh
  ~/KP-RSCSP/sensorlab/fulfillment/functions$ cd ../
  ~/KP-RSCSP/sensorlab/fulfillment$ firebase deploy --only functions
```

作成したコードにエラーが無く、デプロイ作業が完了すれば下記のように関数のURLが表示されます。このURLを控えておいてください。
※関数URLは初回のデプロイ完了時のみ表示されます。

```text
  Function URL (....): https://us-central1-.....cloudfunctions.net/....

  ✔  Deploy complete!
```

![デプロイ成功メッセージ](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig018.png)

関数が正しくデプロイされているか確認するには、Firebase Consoleにブラウザーでアクセスし、Functions ＞ ダッシュボード を開きます。一覧内に作成した関数名が存在していれば、問題なくデプロイ処理が完了しています。

![Firebase Consoleより関数登録状況を確認](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig019.png)

以後、フルフィルメントのソースコードを変更した場合は、再度デプロイ作業をやり直してください。

## Dialogflowへのリンク

ここまでの作業で、フルフィルメント関数が使用可能な状態となり、呼び出すためのURLも確認できました。再びDialogflowコンソールに戻り、作成途中の《センサーラボ》のエージェントへ、控えておいた関数のURLを登録します。

メニューからFulfillmentを選択し、下記の通りに内容を変更して［SAVE］をクリックします。

  - **Webhook**  ☑ (ENABLED)
      - **URL**: (デプロイしたフルフィルメント関数の URL)
      - **Basic Auth**: (空欄)
      - **Headers**: (空欄)
      - **Domains**: Enable webhook for all domains
  - **Inline Editor (Powered by Cloud Functions for Firebase)**  □ (DISABLED)

![Dialogflowエージェントへのフルフィルメントのリンク設定](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig020.png)

以上で、フルフィルメント関数を使用するDialogflowエージェントが完成し、アシスタントアプリ側の実装が終了しました。

次は、Raspberry Pi側で動作させるローカルスクリプトの作成を行います。
