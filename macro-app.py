import numbers
import pyautogui
from flask import Flask, render_template, request, redirect
import json
from socket import gethostname
# import keyboard

app = Flask(__name__)

buttons = {}
# numbers = range(10)
numbers = []
clickable_btns = ['x', 'b', 'j', 'esc']
holdable_btns = ['shift', 'ctrl', 'alt', 'space']


@app.route("/")
def main_page():
    return render_template("main-page.html", host_name=gethostname(), buttons=get_buttons())


@app.route('/<user_action>', methods=['POST'])
def process_key(user_action, keypress=None):
    keypress = json.loads(request.data).get("macro", "")
    if (keypress):
        # print(keypress,"pressed: ", keyboard.is_pressed(keypress))
        match user_action:
            case "click":
                pyautogui.press(keypress)
            case "hold" | "release" | "lock":
                toggle_buttons(keypress)
            case "releaseAll":
                for btn in [d for d in buttons.values() if d['hold'] == True]:
                    pyautogui.keyUp(btn.get("name", "esc"))
    else:
        pass
    return ("ok", 204)


def get_buttons():
    global buttons
    for i in numbers+clickable_btns:
        buttons[str(i)] = {"name": str(i), "hold": False, "pressed": False}
    for i in holdable_btns:
        buttons[str(i)] = {"name": str(i), "hold": True, "pressed": False}
    return buttons


def toggle_buttons(keypress):
    if buttons.get(keypress).get("pressed", False):
        pyautogui.keyUp(keypress)
    else:
        pyautogui.keyDown(keypress)
    buttons[keypress]["pressed"] = not buttons[keypress]["pressed"]


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=80, host="0.0.0.0")
