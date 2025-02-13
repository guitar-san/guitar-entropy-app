# クラシックギター曲のエントロピー計算アプリ
# guitar-entropy-app

このアプリケーションは、クラシックギター曲のエントロピー（情報量）を計算し、管理するためのツールです。

### 主な機能
・CSVファイルをアップロード して、楽譜データのエントロピーを計算  
・絶対音高（absolute_pitch）、ピッチクラス（pitch_class）、音価（duration）、運指（fingering）、弦（string）、フレット（flet） のエントロピーを自動計算  
・過去のアップロード一覧を表示（エントロピー値を保存）  
・同名ファイルの上書き保存（事前確認あり）  
・個別削除 & 全削除 が可能  
・計算結果をCSVでダウンロード  

### 使い方
・アプリを開く  
https://guitar-entropy-app.streamlit.app/  
・CSVファイルをアップロード  
・エントロピー計算結果を確認  
・アップロード済みデータを一覧表示  
・不要なデータを削除（個別 or 全削除）  
・CSVをダウンロードして保存  

### CSVデータのフォーマット
アップロードするCSVファイルは、以下のカラムを含む必要があります：  
| absolute_pitch | pitch_class | duration | fingering | string | flet |  

### 注意点
Streamlit Cloudの無料プランでは、アップロードしたデータがセッション終了後に消える可能性があります。
そのため、Google Sheets / Google Drive との連携を検討しています。

### License
MIT License

### お問い合わせ: 
niino@slis.tsukuba.ac.jp

