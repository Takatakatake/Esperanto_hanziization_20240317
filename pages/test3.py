import streamlit as st
import re
import io
from PIL import Image

# 置換用の辞書
esperanto_to_x = {
    "ĉ": "cx", "ĝ": "gx", "ĥ": "hx", "ĵ": "jx", "ŝ": "sx", "ŭ": "ux",
    "Ĉ": "Cx", "Ĝ": "Gx", "Ĥ": "Hx", "Ĵ": "Jx", "Ŝ": "Sx", "Ŭ": "Ux",
    "c^": "cx", "g^": "gx", "h^": "hx", "j^": "jx", "s^": "sx", "u^": "ux",
    "C^": "Cx", "G^": "Gx", "H^": "Hx", "J^": "Jx", "S^": "Sx", "U^": "Ux"
}
x_to_jijofu = {'cx': 'ĉ', 'gx': 'ĝ', 'hx': 'ĥ', 'jx': 'ĵ', 'sx': 'ŝ', 'ux': 'ŭ', 'Cx': 'Ĉ',
               'Gx': 'Ĝ', 'Hx': 'Ĥ', 'Jx': 'Ĵ', 'Sx': 'Ŝ', 'Ux': 'Ŭ'}
x_to_hat = {'cx': 'c^', 'gx': 'g^', 'hx': 'h^', 'jx': 'j^', 'sx': 's^', 'ux': 'u^', 'Cx': 'C^',
            'Gx': 'G^', 'Hx': 'H^', 'Jx': 'J^', 'Sx': 'S^', 'Ux': 'U^'}

def replace_esperanto_chars(text, letter_dictionary):
    # 各エスペラント文字をX形式に置換
    for esperanto_char, x_char in letter_dictionary.items():
        text = text.replace(esperanto_char, x_char)
    return text

def safe_replace(text, replacements):
    # 必要な置換を記録するための辞書を初期化
    valid_replacements = {}
    # テキスト内の各置換対象文字列をチェックし、プレースホルダーに置換
    for old, new, placeholder in replacements:
        if old in text:
            text = text.replace(old, placeholder)
            # この置換が後で実際に行う必要があることを辞書に記録
            valid_replacements[placeholder] = new
    # プレースホルダーを実際の新しい文字列に置換
    for placeholder, new in valid_replacements.items():
        text = text.replace(placeholder, new)

    return text

st.title("世界语汉字化")
st.caption('这是一个将世界语文本转换成汉字符号的网络应用程序。')

code = '''
import streamlit as st
'''
st.code(code, language='python')

# 画像
image = Image.open('エスペラントの漢字化の理想図.png')
st.image(image)

# ファイルアップローダーを追加
uploaded_file = st.file_uploader("Upload your replacements file", type=['txt'])
if uploaded_file is not None:
    # ファイルを読み込んで replacements3 リストを作成
    replacements3 = []
    for line in uploaded_file:
        decoded_line = line.decode('utf-8').strip()
        parts = decoded_line.split(',')
        if len(parts) == 3:
            replacements3.append((parts[0], parts[1], parts[2]))
else:
    # ファイルがアップロードされていない場合はデフォルトのファイルを使用
    replacements3 = []
    with open("replacements2_list_html.txt", 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            j = line.split(',')
            if len(j) == 3:
                old, new, place_holder = j[0], j[1], j[2]
                replacements3.append((old, new, place_holder))

text = ""  # フォームの外に変数textを定義

with st.form(key='profile_form'):
    # テキストボックス

    # ラジオボタン
    letter_type = st.radio('文字形式', ('字上符', 'x形式', '^形式'))  # select_boxでもいい

    sentence = st.text_area('世界语句子')

    # ボタン
    submit_btn = st.form_submit_button('发送')
    cancel_btn = st.form_submit_button('取消')
    if submit_btn:
        replaced_text = replace_esperanto_chars(sentence, esperanto_to_x)
        text = safe_replace(replaced_text, replacements3)
        if letter_type == '字上符':
            text = replace_esperanto_chars(text, x_to_jijofu)
        elif letter_type == '^形式':
            text = replace_esperanto_chars(text, x_to_hat)
        st.text_area("", text, height=300)

        # ダウンロードボタンをフォームの外に移動
        to_download = io.BytesIO(text.encode('utf-8'))
        to_download.seek(0)

        st.download_button(
            label="下载文本",
            data=to_download,
            file_name="processed_text.txt",
            mime="text/plain"
        )

# ダウンロードボタンをフォームの外に配置
if text:
    to_download = io.BytesIO(text.encode('utf-8'))
    to_download.seek(0)
    st.download_button(
        label="下载文本",
        data=to_download,
        file_name="processed_text.txt",
        mime="text/plain"
    )
