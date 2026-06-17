from tkinter import *
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES

# Translator object
translator = Translator()

# Translate function
def translate_text():
    try:
        text = input_text.get("1.0", END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text.")
            return

        src_lang = source_lang.get()
        dest_lang = target_lang.get()

        translated = translator.translate(
            text,
            src=src_lang,
            dest=dest_lang
        )

        output_text.delete("1.0", END)
        output_text.insert(END, translated.text)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Copy translated text
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", END))
    messagebox.showinfo("Copied", "Translated text copied!")

# Main Window
root = Tk()
root.title("Language Translator")
root.geometry("700x500")

# Language codes
languages = list(LANGUAGES.keys())

Label(root, text="Enter Text", font=("Arial", 12)).pack()

input_text = Text(root, height=8, width=70)
input_text.pack(pady=5)

frame = Frame(root)
frame.pack(pady=10)

source_lang = ttk.Combobox(frame, values=languages, width=20)
source_lang.set("en")
source_lang.grid(row=0, column=0, padx=10)

target_lang = ttk.Combobox(frame, values=languages, width=20)
target_lang.set("hi")
target_lang.grid(row=0, column=1, padx=10)

Button(frame, text="Translate", command=translate_text).grid(row=0, column=2, padx=10)

Label(root, text="Translated Text", font=("Arial", 12)).pack()

output_text = Text(root, height=8, width=70)
output_text.pack(pady=5)

Button(root, text="Copy Text", command=copy_text).pack(pady=10)

root.mainloop()