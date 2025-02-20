# 楽曲の定量スコア計算アプリ
# guitar-entropy-app

このアプリケーションは、クラシックギター曲のエントロピー（平均情報量）や多彩度スコアを計算し、データ管理するためのツールです。

### 主な機能
・CSVファイルをアップロードして、楽曲情報を計算  
　・エントロピー：絶対音高（absolute_pitch）、ピッチクラス（pitch_class）、音価（duration）、運指（fingering）、弦（string）、フレット（fret）
　・多彩度スコア：MDS、TDS、OverallScore（これらの詳細は現在非公開です）
・計算したファイルの一覧を表示 
・個別削除 & 全削除 が可能  
・計算結果をCSVでダウンロード  

### 使い方
・アプリを開く  
https://guitar-entropy-app.streamlit.app/  
・CSVファイルをアップロード  
・エントロピー及び多彩度スコアの結果を確認  
・アップロード済みデータを一覧表示  
・不要なデータを削除（個別 or 全削除）  
・total_score.CSVをダウンロードして保存  

### CSVデータのフォーマット
アップロードするCSVファイルは、以下の6つのカラムを含む必要があります：  
| absolute_pitch | pitch_class | duration | fingering | string | fret |  

### 注意点
Streamlit Cloudの無料プランでは、アップロードしたデータがセッション終了後に消える可能性があります。
そのため、現在 Google Sheets / Google Drive との連携を検討しています。

### License
MIT License

### お問い合わせ: 
niino@slis.tsukuba.ac.jp

