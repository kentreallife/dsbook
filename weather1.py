import sys
from PySide2 import QtCore, QtScxml

prefs = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県",
         "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]

# 定義


def get_place(text):
    for pref in prefs:
        if pref in text:
            return pref
        return ""

# テキストに「今日」もしくは「明日」があればそれを返す．見つからない場合は空文字を返す．


def get_date(text):
    if "今日" in text:
        return "今日"
    elif "明日" in text:
        return "明日"
    else:
        return ""

# テキストに「天気」もしくは「気温」があればそれを返す．見つからない場合は空文字を返す．


def get_type(text):
    if "天気" in text:
        return "天気"
    elif "気温" in text:
        return "気温"
    else:
        return ""


# Qtに関するおまじない
app = QtCore.QCoreApplication()
el = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト
print("SYS> こちらは天気情報案内システムです")

# 状態とシステム発話を紐づけた辞書
uttdic = {"ask_place": "地名を言ってください",
          "ask_date": "日付を言ってください",
          "ask_type": "情報種別を言ってください"}

# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)

# ユーザ入力の処理
while True:
    text = input("> ")

    if current_state == "ask_place":
        place = get_place(text)
        if place != "":
            sm.submitEvent("place")
            el.processEvents()
    elif current_state == "ask_date":
        date = get_date(text)
        if date != "":
            sm.submitEvent("date")
            el.processEvents()
    elif current_state == "ask_type":
        _type = get_type(text)
        if _type != "":
            sm.submitEvent("type")
            el.processEvents()
# ユーザ入力を用いて状態遷移
    sm.submitEvent(text)
    el.processEvents()

    # 遷移先の状態を取得
    current_state = sm.activeStateNames()[0]
    print("current_state=", current_state)

    # 遷移先がtell_infoの場合は情報を伝えて終了
    if current_state == "tell_info":
        print("天気をお伝えします")
        break
    else:
        # その他の遷移先の場合は状態に紐づいたシステム発話を生成
        sysutt = uttdic[current_state]
        print("SYS>", sysutt)

    # 終了発話
    print("ご利用ありがとうございました")

    # end of file
