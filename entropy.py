import streamlit as st
import pandas as pd
import numpy as np
import os
import uuid

# エントロピー計算関数（途中過程を表示）
def calculate_entropy(series):
    value_counts = series.value_counts()
    total_count = len(series)
    probabilities = value_counts / total_count
    
    # 情報量を算出
    information_values = -probabilities * np.log2(probabilities)
    entropy = information_values.sum()
    
    # 途中過程をデバッグ表示用に返す
    return entropy, pd.DataFrame({
        "ラベル": value_counts.index,
        "出現数": value_counts.values,
        "確率": probabilities.values,
        "情報量": information_values.values
    })

# メイン関数
def main():
    st.title("クラシックギター曲のエントロピー計算")
    
    entropy_file_path = "total-entropy.csv"
    
    # 既存のエントロピー一覧を表示（アップロード前でも見れるようにする）
    if os.path.exists(entropy_file_path):
        st.write("### すべてのアップロードファイルのエントロピー一覧")
        saved_entropy_df = pd.read_csv(entropy_file_path)
        
        # `unique_id` がない場合は追加
        if "unique_id" not in saved_entropy_df.columns:
            saved_entropy_df["unique_id"] = [str(uuid.uuid4()) for _ in range(len(saved_entropy_df))]
            saved_entropy_df.to_csv(entropy_file_path, index=False)
        
        # file_name を一番左に配置
        cols = ["file_name"] + [col for col in saved_entropy_df.columns if col != "file_name"]
        saved_entropy_df = saved_entropy_df[cols]
        st.write(saved_entropy_df)
        
        # データ全削除ボタン
        if st.button("全データを削除"):
            os.remove(entropy_file_path)
            st.warning("全エントロピーデータを削除しました！")
            st.experimental_rerun()
        
        # 削除したいデータの選択（file_name + unique_id）
        if not saved_entropy_df.empty:
            saved_entropy_df["entry"] = saved_entropy_df["file_name"] + " (ID: " + saved_entropy_df["unique_id"] + ")"
            selected_entry = st.selectbox("削除するデータを選択", saved_entropy_df["entry"].tolist())
            selected_unique_id = selected_entry.split(" (ID: ")[1][:-1]
            
            if st.button("選択したエントロピーデータを削除"):
                saved_entropy_df = saved_entropy_df[saved_entropy_df["unique_id"] != selected_unique_id]
                saved_entropy_df.drop(columns=["entry"], inplace=True)
                saved_entropy_df.to_csv(entropy_file_path, index=False)
                st.warning(f"エントロピーデータ（ID: {selected_unique_id}）を削除しました！")
                st.experimental_rerun()
    
    # ファイルアップロード
    st.write("### 新しいCSVファイルをアップロード")
    uploaded_file = st.file_uploader("CSVファイルをドロップまたは選択", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### アップロードされたデータ")
        st.write(df.head())
        
        # 計算対象のカラム
        columns_to_analyze = ["absolute_pitch", "pitch_class", "duration", "fingering", "string", "flet"]
        entropy_values = {}
        debug_info = {}
        
        for col in columns_to_analyze:
            entropy_values[col], debug_info[col] = calculate_entropy(df[col].dropna())
        
        entropy_values["file_name"] = uploaded_file.name  # ファイル名を記録
        entropy_values["unique_id"] = str(uuid.uuid4())  # 一意の識別IDを追加
        entropy_df = pd.DataFrame([entropy_values])
        
        # file_name を一番左に移動
        entropy_df = entropy_df[["file_name"] + [col for col in entropy_df.columns if col != "file_name"]]
        
        # 結果の表示
        st.write("### 計算されたエントロピー値")
        st.write(entropy_df)
        
        # 上書き確認
        if os.path.exists(entropy_file_path):
            existing_entropy_df = pd.read_csv(entropy_file_path)
            if uploaded_file.name in existing_entropy_df["file_name"].values:
                if not st.checkbox(f"{uploaded_file.name} は既に一覧にあります。上書きしますか？チェックボタンを押すと上書きされます。"):
                    return
                existing_entropy_df = existing_entropy_df[existing_entropy_df["file_name"] != uploaded_file.name]  # 同名ファイル削除
            updated_entropy_df = pd.concat([existing_entropy_df, entropy_df], ignore_index=True)
        else:
            updated_entropy_df = entropy_df
        
        updated_entropy_df.to_csv(entropy_file_path, index=False)
        st.success(f"エントロピー値を `total-entropy.csv` に保存しました！（{uploaded_file.name} は上書き）")
        
    # ダウンロードリンク
    if os.path.exists(entropy_file_path):
        st.download_button(
            label="エントロピーCSVをダウンロード",
            data=pd.read_csv(entropy_file_path).to_csv(index=False).encode("utf-8"),
            file_name="total-entropy.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
