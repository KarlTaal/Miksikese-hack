import pyautogui
import time
import pytesseract
from PIL import Image
import os
import shutil


# kuidas tesseracti üles seada
# https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
BUTTON_CLICK_DELAY = 0.05
START_DELAY = 0.5
SUBMIT_DELAY = 0.9

def read_button(txt):
    buttonlocation = pyautogui.locateOnScreen(f"images/{txt}.png")
    buttonx, buttony = pyautogui.center(buttonlocation)
    return [buttonx, buttony]


def read_buttons():
    buttons = {}
    for i in range(10):  # numbers
        try:
            buttonlocation = pyautogui.locateOnScreen(f"images/{i}.png")
            buttonx, buttony = pyautogui.center(buttonlocation)
            buttons[str(i)] = [buttonx, buttony + int(buttonlocation[3] * 0.8)]
            print("Loaded:", i)
        except:
            print(f"There was an exception while loading number {i}")
            exit()

    other_centers = ["ok", "alusta"]
    for o in other_centers:  # other buttons
        try:
            buttonlocation = pyautogui.locateOnScreen(f"images/{o}.png")
            buttonx, buttony = pyautogui.center(buttonlocation)
            if o != "alusta":
                buttons[o] = [buttonx, buttony + int(0.8 * buttonlocation[3])]
            else:
                buttons[o] = [buttonx, buttony]
            print("Loaded: ", o)
        except:
            print(f"There was an exception while loading button {o}")
            exit()
    return buttons


def read_expression(path="images/processed_expression_image.png"):
    #https://tesseract-ocr.github.io/tessdoc/Data-Files
    value = Image.open(path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Karl\AppData\Local\Tesseract-OCR\tesseract.exe'
    return pytesseract.image_to_string(value).split("=")[0]


def calc_expr(expr):
    return eval(expr)


def cut_expression(guideline):
    # left top width height
    coords = (guideline[0], guideline[1] - guideline[3], int(guideline[2] * 2), guideline[3])
    im = pyautogui.screenshot(region=coords)
    im.save("images/expression_image.png")


def process_image(path="images/expression_image.png", to="images/processed_expression_image.png"):
    im = Image.open(path)
    im = im.convert("RGB")
    data = im.getdata()

    new_image_data = []
    # print(Image.Image.getcolors(im))
    black = (0, 0, 0)
    white = (255, 255, 255)
    for item in data:
        if item[0] in list(range(50, 100)):  # green
            new_image_data.append(white)
        else:
            new_image_data.append(black)
    im.putdata(new_image_data)
    w, h = im.size
    furthest_black_x = 0
    for x in range(w):
        for y in range(h):
            r, g, b = im.getpixel((x, y))
            if (r, g, b) == black and x > furthest_black_x and y < h / 2 + h / 5:
                furthest_black_x = x

    area = (0, 0, furthest_black_x, h)
    cropped_img = im.crop(area)

    cropped_img.save(to)


if False: #debug
    process_image(path="logs/34+5+39/imgdefault.png", to="logs/34+5+39/debug.png")
    print("default", read_expression("logs/34+5+39/imgdefault.png"))
    print("procesessed", read_expression("logs/34+5+39/imgprocessed.png"))
    print("debug", read_expression("logs/34+5+39/debug.png"))
    exit()


def submit_answer(buttons, answer):
    for c in str(answer):
        pyautogui.click(x=buttons[c][0], y=buttons[c][1])
        time.sleep(BUTTON_CLICK_DELAY)
    pyautogui.click(x=buttons["ok"][0], y=buttons["ok"][1])


def make_log(expr, expr_val):
    os.mkdir(f"logs/{expr}+{expr_val}")
    with open(f"logs/{expr}+{expr_val}/expr.txt", "w", encoding="UTF-8") as f:
        f.write(expr)
    im = Image.open("images/processed_expression_image.png")
    im.save(f"logs/{expr}+{expr_val}/imgprocessed.png")
    im = Image.open("images/expression_image.png")
    im.save(f"logs/{expr}+{expr_val}/imgdefault.png")
    print("Logged\n")


# process_image()

button_coords = read_buttons()

try:
    shutil.rmtree('logs/')
    os.mkdir(f"logs")
except:
    os.mkdir(f"logs")

first_iter = True

while True:
    if first_iter:
        pyautogui.click(x=button_coords["alusta"][0], y=button_coords["alusta"][1])
        time.sleep(START_DELAY)
        button_coords["expr_guideline"] = pyautogui.locateOnScreen(f"images/expr_guideline.png")
        if (not button_coords["expr_guideline"]):
            print(f"Failed to laod quideline")
            exit()
        print("Loaded guideline")
        print()
        first_iter = False

    expr = "dummy"
    expr_val = "dummy"
    try:
        cut_expression(button_coords["expr_guideline"])  # cutting the expression and saving to png
        process_image()  # process png for better text detection
        expr = read_expression()  # read expression from png
        expr_val = calc_expr(expr)  # calculate the answer
        print("Expression: ", expr)
        print("Answer:", expr_val, "\n")
        try:
            make_log(expr, expr_val)
        except:
            pass
        submit_answer(button_coords, expr_val)  # click the buttons
        time.sleep(SUBMIT_DELAY)
    except:
        print("In error")
        try:
            make_log(expr, expr_val)
        except:
            pass
