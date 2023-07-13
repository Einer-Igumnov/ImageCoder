from PIL import Image
import tkinter
from tkinter import filedialog
import customtkinter


def get_letter_num(c):
    return ord(c)


def boost_password(s):
    result = ""
    for i in range(len(s)):
        c = chr(ord(s[i])**2)
        result += c
    return result


def hash_string(s):
    result = 0
    pr = 1
    x = 239
    y = 998244353
    for i in range(len(s)):
        result = (result + get_letter_num(s[i])*pr) % y
        pr *= x
    return result


def modify_image(img, command, password):

    p_hash = hash_string(password)

    block_size = 4

    pr = 1
    if command == "decode":
        pr = -1

    w, h = img.size

    pixel_map = img.load()

    print(w, h)

    for i in range(w):
        for j in range(h):
            num = ((i//block_size) * h + (j//block_size)) % len(password)
            r, g, b = img.getpixel((i, j))
            move = ((get_letter_num(password[num]) + 1) ** 10 + round(i ** 2) + round(j ** 2)) * p_hash
            r = (r + pr * move * 13) % 256
            g = (g + pr * move * 23) % 256
            b = (b + pr * move * 33) % 256

            pixel_map[i, j] = (r, g, b)

    return img


def code(img, password):
    password = boost_password(password)
    return modify_image(img, "code", password)


def decode(img, password):
    password = boost_password(password)
    return modify_image(img, "decode", password)


# input_image = Image.open("sample2.jpg")
#
# input_password = "penis"
#
# gen_img = code(input_image, input_password)
#
# gen_img.show()
#
# gen_img.save("coded.png")
#
# input_image = Image.open("coded.png")
#
# gen_img = decode(input_image, "penis")
#
# gen_img.show()

menu_option = "Code image"
generated_image = Image.open("sample.jpg")
input_image = Image.open("sample.jpg")

customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()  # create the Tk window like you normally do
root.geometry("400x240")
root.title("Image Coder beta 0.1")

textbox = customtkinter.CTkTextbox(root, height=1, width=140)
textbox.insert("0.0", "Password...")
textbox.place(relx=0.25, rely=0.4, anchor=tkinter.CENTER)


def menu_callback(choice):
    global menu_option
    menu_option = choice


def select_file():
    global input_image, generated_image
    input_image = Image.open(filedialog.askopenfilename())
    generated_image = input_image


def view_img():
    global input_image, generated_image
    generated_image.show()


def save_img():
    global input_image, generated_image
    generated_image.save(filedialog.askdirectory() + "/coded.png")


def start_gen():
    global generated_image, menu_option, input_image
    password = textbox.get("0.0", "end")
    print(menu_option, password)
    if menu_option == "Code image":
        generated_image = code(generated_image, password)
    else:
        generated_image = decode(generated_image, password)

    view_button = customtkinter.CTkButton(master=root, corner_radius=10, text="View image", command=view_img)
    view_button.place(relx=0.75, rely=0.6, anchor=tkinter.CENTER)

    save_button = customtkinter.CTkButton(master=root, corner_radius=10, text="Save image", command=save_img)
    save_button.place(relx=0.75, rely=0.8, anchor=tkinter.CENTER)


select_button = customtkinter.CTkButton(master=root, corner_radius=10, text="Choose image", command=select_file)
select_button.place(relx=0.25, rely=0.2, anchor=tkinter.CENTER)


menu = customtkinter.CTkOptionMenu(root, values=["Code image", "Decode image"], command=menu_callback)
menu.set("Code image")
menu.place(relx=0.25, rely=0.6, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=root, corner_radius=10, text="Generate", command=start_gen)
button.place(relx=0.25, rely=0.8, anchor=tkinter.CENTER)

root.mainloop()

