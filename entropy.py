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
    st.write("CSVファイルをアップロードしてください。")
    
    # ファイルアップロード
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
        entropy_file_path = "total-entropy.csv"
        if os.path.exists(entropy_file_path):
            existing_entropy_df = pd.read_csv(entropy_file_path)
            updated_entropy_df = pd.concat([existing_entropy_df, entropy_df], ignore_index=True)
        else:
            updated_entropy_df = entropy_df
        
        updated_entropy_df.to_csv(entropy_file_path, index=False)
        st.success("エントロピー値を `total-entropy.csv` に保存しました！")
        
        # 保存されたエントロピー一覧を表示
        st.write("### すべてのアップロードファイルのエントロピー一覧")
        st.write(updated_entropy_df)
        
        # 各カラムの途中計算過程を表示
        st.write("### 計算過程の詳細")
        for col in debug_info:
            st.write(f"#### {col} の計算過程")
            st.write(debug_info[col])
        
        # ダウンロードリンク
        st.download_button(
            label="エントロピーCSVをダウンロード",
            data=updated_entropy_df.to_csv(index=False).encode("utf-8"),
            file_name="total-entropy.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
