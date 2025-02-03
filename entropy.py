import streamlit as st
import pandas as pd
import numpy as np
import os

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
        st.write(saved_entropy_df)
        
        # 削除したいファイルの選択
        file_list = saved_entropy_df["file_name"].unique().tolist()
        if len(file_list) > 0:
            file_to_delete = st.selectbox("削除するファイルを選択", file_list)
            
            if st.button("選択したファイルのエントロピーデータを削除"):
                saved_entropy_df = saved_entropy_df[saved_entropy_df["file_name"] != file_to_delete]
                saved_entropy_df.to_csv(entropy_file_path, index=False)
                st.warning(f"ファイル `{file_to_delete}` のエントロピーデータを削除しました！")
                st.experimental_rerun()
    
    # ファイルアップロード
    st.write("### 新しいCSVファイルをアップロード")
    uploaded_file = st.file_uploader("CSVファイルをドロップまたは選択", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### アップロードされたデータ")
        st.write(df.head())
        
        # 計算対象のカラム
        columns_to_analyze = ["absolute_pitch", "pitch_class", "duration", "fingering", "string"]
        entropy_values = {}
        debug_info = {}
        
        for col in columns_to_analyze:
            entropy_values[col], debug_info[col] = calculate_entropy(df[col].dropna())
        
        entropy_values["file_name"] = uploaded_file.name  # ファイル名を記録
        entropy_df = pd.DataFrame([entropy_values])
        
        # 結果の表示
        st.write("### 計算されたエントロピー値")
        st.write(entropy_df)
        
        # ファイルの保存
        if os.path.exists(entropy_file_path):
            existing_entropy_df = pd.read_csv(entropy_file_path)
            updated_entropy_df = pd.concat([existing_entropy_df, entropy_df], ignore_index=True)
        else:
            updated_entropy_df = entropy_df
        
        updated_entropy_df.to_csv(entropy_file_path, index=False)
        st.success("エントロピー値を `total-entropy.csv` に保存しました！")
        
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
