# import numbers
import pyautogui
from flask import Flask, render_template, request, redirect
import json
from socket import gethostname
from os import path

app = Flask(__name__)
clickable_btns = ['x', 'b', 'j', 't', 'z', 'c', 'esc',
                  "scroll-UP", "scroll-DOWN", "CTRL+", "CTRL-", "del"]
holdable_btns = ['alt', 'space', 'shift', 'ctrl']

buttons = {}
numbers = [str(num) for num in range(1,5)]


@app.route("/")
def main_page():
    return render_template("main-page.html", host_name=gethostname(), buttons=get_buttons())


@app.route("/config")
def config():
    return render_template("config.html",host_name=gethostname(), buttons=get_buttons())


@app.route('/remove_btn', methods=['POST'])
def remove_btn():
    btn_to_remove = json.loads(request.data)
    print_sep(btn_to_remove)
    with open(path.join(path.split(path.realpath(__file__))[0], "buttons.json"),"r+") as f:
        buttons_json = json.load(f)
        del buttons_json[btn_to_remove.get('remove')]
        f.seek(0)
        json.dump(buttons_json,f)
        f.truncate()
    return ("ok", 204)
    

@app.route('/<user_action>', methods=['POST'])
def process_key(user_action, keypress=None):
    keypress = json.loads(request.data).get("macro", "")
    # print(keypress)
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
                    pyautogui.hotkey('ctrl', '+')
                case "CTRL-":
                    pyautogui.hotkey('ctrl', '-')
                case "releaseAll":
                    for btn in [d for d in buttons.values() if d['hold'] == True and d["pressed"] == True]:
                        toggle_buttons(btn.get('name'))
                        pyautogui.keyUp(btn.get("name", "esc"))

    else:
        pass
    return ("ok", 204)


@app.route('/list_btns')
def list_btns():
    return get_buttons()


@app.route('/add_btn', methods=['POST'])
def add_btn():
    data = json.loads(request.data.decode())
    # print(data)
    with open(path.join(path.split(path.realpath(__file__))[0], "buttons.json"),"r+") as f:
        try:
            buttons_json = json.load(f)
        except json.decoder.JSONDecodeError:
            print_sep("faild")
            buttons_json = {}
        print_sep(buttons_json)
        buttons_json[list(data.keys())[0]] = list(data.values())[0]
        print_sep(buttons_json)
        f.seek(0)
        json.dump(buttons_json,f)
        f.truncate()
    return f"got {data}"


def get_buttons():
    global buttons
    if buttons == {}:
        for i in numbers+clickable_btns:
            print_sep(i)
            buttons[str(i)] = {"name": str(i), "hold": False, "pressed": False}
        for i in holdable_btns:
            buttons[str(i)] = {"name": str(i), "hold": True, "pressed": False}
    else: load_buttons_from_json()
    return buttons


def toggle_buttons(keypress):
    if buttons.get(keypress).get("pressed", False):
        pyautogui.keyUp(keypress)
    else:
        pyautogui.keyDown(keypress)
    buttons[keypress]["pressed"] = not buttons[keypress]["pressed"]


def load_buttons_from_json():
    global buttons
    if not path.exists(path.join(path.split(path.realpath(__file__))[0], "buttons.json")):
        print_sep('creating json file')
        with open("buttons.json", "w") as f:
            f.write(json.dumps(get_buttons()))
    else:
        with open("buttons.json","r+") as f:
            try:
                btns = json.load(f)
            except json.decoder.JSONDecodeError:
                buttons = {}
                btns = get_buttons()
                print_sep("only default buttons")
        buttons = btns


def print_sep(things):
    print('-'*100)
    print(things)
    print('-'*100)


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    load_buttons_from_json()
    app.run(debug=True, port=80, host="0.0.0.0")
