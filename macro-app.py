import numbers
import pyautogui
from flask import Flask, render_template, request, redirect
import json
from socket import gethostname

app = Flask(__name__)

buttons = {}
# numbers = range(10)
numbers = []
clickable_btns = ['x', 'b', 'j', 't', 'esc',"scroll-UP", "scroll-DOWN", "CTRL+", "CTRL-"]
holdable_btns = ['alt', 'space', 'shift', 'ctrl']


@app.route("/")
def main_page():
    return render_template("main-page.html", host_name=gethostname(), buttons=get_buttons())


@app.route('/<user_action>', methods=['POST'])
def process_key(user_action, keypress=None):
    keypress = json.loads(request.data).get("macro", "")
    print (keypress)
    if (keypress):
        if keypress in pyautogui.KEYBOARD_KEYS:
            match user_action:
                case "click":
                    pyautogui.press(keypress)
                case "hold" | "release" | "lock":
                    toggle_buttons(keypress)
                
        else:
            match keypress:
                case "scroll-UP":
                    pyautogui.scroll(100)
                case "scroll-DOWN":
                    pyautogui.scroll(-100)
                case "CTRL+":
                    pyautogui.hotkey('ctrl','+')
                case "CTRL-":
                    pyautogui.hotkey('ctrl','-')
                case "releaseAll":
                    for btn in [d for d in buttons.values() if d['hold'] == True and d["pressed"] == True]:
                        toggle_buttons(btn.get('name'))
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
