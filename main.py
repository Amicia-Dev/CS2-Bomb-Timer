import cv2
import ctypes
from PIL import Image, ImageTk, ImageGrab
import tkinter as tk


myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Capture plant popup
def screenCapture():
    img = ImageGrab.grab(bbox=(770, 660, 1150, 900))
    img.save('images/capture.jpg')
    img.close()

# Compare captured image with template
def captureMatching():
    img1 = cv2.imread('images/target.jpg')  # Template image
    img2 = cv2.imread('images/capture.jpg')  # Captured screen

    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_img2, gray_img1, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    max_val = cv2.minMaxLoc(result)[1]

    is_similar = max_val >= threshold

    if is_similar:
        countdown(38)
    else:
        status_label.config(text="Waiting for 💣")
        root.after(500, main)

# Capture game end condition
def scanGameEndCondition():
    condImg = ImageGrab.grab(bbox=(700, 180, 1220, 300))
    condImg.save('images/gameConditionCapture.jpg')
    condImg.close()

    img_capture = cv2.imread('images/gameConditionCapture.jpg')
    img_round_lost = cv2.imread('images/roundLost.jpg')
    img_round_won = cv2.imread('images/roundWon.jpg')

    gray_capture = cv2.cvtColor(img_capture, cv2.COLOR_BGR2GRAY)
    gray_round_lost = cv2.cvtColor(img_round_lost, cv2.COLOR_BGR2GRAY)
    gray_round_won = cv2.cvtColor(img_round_won, cv2.COLOR_BGR2GRAY)

    threshold = 0.4
    result_lost = cv2.matchTemplate(gray_capture, gray_round_lost, cv2.TM_CCOEFF_NORMED)
    is_lost = cv2.minMaxLoc(result_lost)[1] >= threshold

    result_won = cv2.matchTemplate(gray_capture, gray_round_won, cv2.TM_CCOEFF_NORMED)
    is_won = cv2.minMaxLoc(result_won)[1] >= threshold

    return is_lost or is_won

# Countdown function with UI update
def countdown(seconds):
    countdown_label.pack()
    if seconds == 0:
        showExplosion()
        return
    if scanGameEndCondition():
        status_label.config(text="Round ended!")
        countdown_label.pack_forget()
        explosion_label.pack_forget()
        root.after(3000, main)
        return

    status_label.config(text=f"The bomb has been planted!")
    countdown_label.config(text=f"{seconds}", fg="red", font=("Helvetica", 80, "bold"))
    root.after(1000, countdown, seconds - 1)

# Show explosion image
def showExplosion():
    status_label.config(text="BOOOM! ***Big explosion***")
    explosion_img = Image.open("images/explosion.jpg")
    explosion_img = explosion_img.resize((200, 200), Image.Resampling.LANCZOS)
    explosion_photo = ImageTk.PhotoImage(explosion_img)

    explosion_label.config(image=explosion_photo)
    explosion_label.image = explosion_photo

    countdown_label.pack_forget()
    explosion_label.pack()
    root.after(3000, resetUI)

# Reset UI and start scanning after explosion
def resetUI():
    explosion_label.pack_forget()
    status_label.config(text="Waiting for 💣")
    countdown_label.config(text="")
    main()


def main():
    screenCapture()
    captureMatching()

# Setup the GUI
root = tk.Tk()
root.title("CS2 Bomb Timer")
root.geometry("400x350")
root.resizable(False, False)
root.configure(bg="#1f1f1f")
root.iconbitmap("images/Icon.ico")
status_label = tk.Label(root, text="Waiting for 💣", font=("Helvetica", 20), bg="#1f1f1f", fg="white")
status_label.pack(pady=10)

countdown_label = tk.Label(root, text="", font=("Helvetica", 80, "bold"), bg="#1f1f1f", fg="red")
countdown_label.pack(pady=10)

explosion_label = tk.Label(root, bg="#1f1f1f")
explosion_label.pack(pady=20)


main()


root.mainloop()
