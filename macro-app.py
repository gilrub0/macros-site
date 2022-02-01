import numbers
import pyautogui
from flask import Flask, render_template, request, redirect
import json
from socket import gethostname

app = Flask(__name__)
numbers = range(10)
clickable_btns = ['f5', 'f12', 'enter','esc']
holdable_btns = ['shift', 'ctrl', 'alt', 'space']

@app.route("/")
def main_page():
    return render_template("main-page.html", host_name=gethostname(), buttons=get_buttons())


@app.route('/<user_action>', methods=['POST'])
def process_key(user_action, keypress=None):
    keypress = json.loads(request.data).get("macro", "")
    if (keypress):
        match user_action:
            case "click":
                pyautogui.keyDown(keypress)
                pyautogui.keyUp(keypress)
            case "hold":
                pyautogui.keyDown(keypress)
            case "release":
                pyautogui.keyUp(keypress)
            case "releaseAll":
                all_the_buttons = get_buttons()
                for btn in filter(lambda x: x.get('hold')==True, all_the_buttons):
                    pyautogui.keyUp(btn.get("name","esc"))
    else:
        pass
    return ("ok", 204)


def get_buttons():
    buttons = []
    
    buttons = buttons + [{"name": str(i), "hold": False} for i in numbers]
    buttons = buttons + [{"name": str(i), "hold": False} for i in clickable_btns]
    buttons = buttons + [{"name": str(i), "hold": True} for i in holdable_btns]
    return buttons


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=80, host="0.0.0.0")
