from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
has_begun = False

try:
    file = open("data/score.txt")
    score = int(file.readline())
except FileNotFoundError:
    score = 0


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/French.csv")

to_learn = data.to_dict(orient = "records")
def next_card():
    global current_card
    global has_begun, flip_timer, score
    window.after_cancel(flip_timer)
    has_begun = True
    current_card = random.choice(to_learn)
    canvas.itemconfig(french_card, image=card_front)
    canvas.itemconfig(card_title, text = "French", fill = "black", font = ("Ariel", 40, "italic"))
    canvas.itemconfig(card_word, text = current_card["French"], font = ("Ariel", 60, "bold"), fill = "black")
    canvas.itemconfig(card_score, text=f"Number of words learnt: {score}")
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    global has_begun
    if has_begun:
        canvas.itemconfig(french_card, image = card_back)
        canvas.itemconfig(card_title, text="English", fill = "white", font = ("Ariel", 40, "italic"))
        canvas.itemconfig(card_word, text=current_card["English"], fill = "white", font = ("Ariel", 60, "bold"))

def remove_card():
    global has_begun
    global score

    if has_begun:
        score += 1
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv")
        with open("data/score.txt", "w") as file:
            file.write(str(score))
        next_card()

window = Tk()
window.title("Language Learner")
window.config(padx= 50, pady= 50, bg=BACKGROUND_COLOR)
window.resizable(0,0)

flip_timer = window.after(3000, flip_card)

card_front = PhotoImage(file = "images/card_front.png")
card_back = PhotoImage(file = "images/card_back.png")
right_image = PhotoImage(file = "images/right.png")
wrong_image = PhotoImage(file = "images/wrong.png")


canvas = Canvas(width = 800, height = 526)
canvas.config(bg = BACKGROUND_COLOR, highlightthickness = 0)



french_card = canvas.create_image(400, 263, image = card_front)
canvas.grid(row=0, column=0, columnspan = 2)

card_title = canvas.create_text(400, 150, text = "French Language Learner", font = ("Ariel", 40, "bold"))
card_word = canvas.create_text(400, 263, text = "Press the Cross to Begin", font = ("Ariel", 20, "italic"))
card_score = canvas.create_text(400, 350, text = "", font = ("Ariel", 20, "italic"))


wrong_button = Button(image = wrong_image, highlightthickness = 0, borderwidth =0, command = next_card)
wrong_button.grid(row =1, column =1)

right_button = Button(image = right_image, highlightthickness = 0, borderwidth=0, command = remove_card)
right_button.grid(row=1, column =0)


window.mainloop()