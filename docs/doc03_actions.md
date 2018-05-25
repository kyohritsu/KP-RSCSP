# アシスタントアプリの開発 (3) アシスタントアプリの作成

Actions on Googleコンソールより、アシスタントアプリの作成を始めます。まずは第1段階として、作成するアプリ情報の登録を行います。

## 新規プロジェクトの作成

開発用の Google アカウントでログインし、Actions on Google にアクセスします。
  - https://developers.google.com/actions/

新規プロジェクトの作成を行います。  
［＋ Add/import project］をクリックします。

![新規プロジェクト作成](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig001.png)

プロジェクトの名前とメイン地域の設定を入力します。
  - Project name に“SensorLab”を入力
  - Country/region に“Japan”を選択
  - ［CREATE PROJECT］をクリック

![プロジェクト設定の記入](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig002.png)

新規プロジェクトの作成ができない場合は、お使いのGoogleアカウントで作成できるプロジェクト数の割り当てが制限に達している可能性があります。既存のプロジェクトのいずれかに対してシャットダウン (削除操作) を行い、その後定められた保全期間が経過することで割り当て数に空きができます。

## アシスタントアプリの構築手順

画面左上のメニュー欄から“Overview”を選択します。  
(ブラウザウィンドウが狭い場合、メニューは画面左上の［≡］をクリックすることで表示されます)

![アプリ概要メニューを開く](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig003.png)

これから、各項目の必要事項を編集し、アクションアプリの作成を行います。項目の 1. に見えている“Add actions to your app”が、アシスタントアプリが対応する会話内容やそれに関連する連携動作を定義する箇所であり、アプリの本体に相当する部分です。
先に他の設定を終えてから、アクションの作成を行うことにします。

![アプリ作成までのステップ](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig004.png)

### アプリ情報の設定 (2. App information)

［2 App information］をクリックし、現れた［EDIT］ボタンをクリックします。

下記の通り、アプリの日本語版に関する基本情報を入力します。今回は評価用として、必要最低限の項目について説明をします。省略した項目については、アプリのリリースを検討する際は適当な内容を記載する必要があります。
  1. **Name**  
    - Type your Assistant app's name. ...  
      アシスタントアプリに付ける名前を作成します。  
      (この名前は全てのアシスタントアプリの中で先取り式になっているため、先行するアプリに同じ名前があれば登録できません。この先は“センサーラボ”が利用可能だと仮定して進行します。以後の説明では、アプリ名はここで登録したものに読み換えてください。)
    - Pronunciation  
      アシスタントが名前を発音する際の読み方を入力します。
  2. **Details**  
    - Assistant app introduction  
      アシスタントアプリの機能について簡潔に説明する文を入力します。ここでは“センサーの状態確認や、リレー出力の操作”とします。
    - Assistant app voice  
      応答メッセージの声質種類を選択します。お好きな声質を選んでください。［Match user's language setting］をチェックすると、ユーザーのGoogleアカウントの持っているアシスタント設定にリンクされます。
    - Short description  
      アシスタントアプリの概要を入力します。今回の例であれば下記のような文章を入力しますが、実験中は省略してもかまいません。  
      > センサーラボは、手元に設置したセンサーの状態を確認したり、リレー出力を操作するためのアプリです。

    - Full description  
      アシスタントアプリの詳細説明を入力します。
    - Sample invocations  
      アシスタントのトップ階層からこのアプリを呼び出す際の文を invocation と呼びます。これは1アプリにつき最大で5種類登録ができます。初期設定では“Ok Google, *センサーラボ*につないで”が登録されています。
  3. **Images**
  4. **Contant details**
  5. **Privacy and consent**  
     **Additional Information**  
    省略します。

設定が完了したらページ最下部の［SAVE］をクリックします。省略した箇所以外で問題が発生していないか確認し、再度メニューから［Overview］に戻ります。

### ターゲット地域の設定 (3. Location targeting)

［3 Location targeting］では、アプリを使用可能とする地域 (国) を個別に変更できます。初期状態では全地域が対応となっていますので、このままにします。

### サーフェスの対応形式 (4. Surface capabilities)

Surface (サーフェス) とは、スマートフォン/タブレットやスピーカーなど、アシスタントが動作するデバイスの種別を表す単語です。アプリに含まれる応答の一部をサポートしないデバイスがある場合は、この項目でデバイスの対応状況を指定します。例えば、アクションで指定した応答の一部に「画像」や「外部 URL」などを含めたものがある場合、スピーカーは画面を搭載していないため非対応となります。
本文書ではスピーカー向けアプリの作成を目標とするため、この設定はすべて初期状態のままにします。その際は、アクションを作成する際はすべての応答がスピーカーで再生可能な形式でなければなりません。

![アプリ情報の記入](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig005.png)

### アクションの作成 (1. Actions)

［1 Actions］をクリックし、現れた［ADD ACTIONS］ボタンをクリックします。

![アクションの作成](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig004a.png)

今回は、アクションの作成は“Dialogflow”というアクション作成用のビルダーを利用します。
その他、「テンプレートから作成する」「Actions SDK を使用する (アクションを JSON 記述で定義)」等の方法もありますが、この文書では省略します。

移動した画面で、Dialogflow 項目内の［BUILD］をクリックします。

![Dialogflowを選択](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig006.png)

初めての場合、お使いのアカウントでの Dialogflow へのアクセスが求められますので、許可してください。

![Dialogflowへのアクセス許可](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig007.png)
