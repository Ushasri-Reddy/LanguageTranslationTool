
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Online translation service
API_URL = "https://api.mymemory.translated.net/get"

# Supported languages
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
}

# Common translations for reliable demo examples
KNOWN_TRANSLATIONS = {
    ("how are you", "en", "te"): "మీరు ఎలా ఉన్నారు?",
    ("how are you?", "en", "te"): "మీరు ఎలా ఉన్నారు?",
    ("how are you", "en", "hi"): "आप कैसे हैं?",
    ("how are you?", "en", "hi"): "आप कैसे हैं?",
    ("hello", "en", "te"): "హలో",
    ("hello", "en", "hi"): "नमस्ते",
    ("good morning", "en", "te"): "శుభోదయం",
    ("good morning", "en", "hi"): "सुप्रभात",
    ("thank you", "en", "te"): "ధన్యవాదాలు",
    ("thank you", "en", "hi"): "धन्यवाद",
    ("good night", "en", "te"): "శుభ రాత్రి",
    ("good night", "en", "hi"): "शुभ रात्रि",
    ("what is your name", "en", "te"): "మీ పేరు ఏమిటి?",
    ("what is your name?", "en", "te"): "మీ పేరు ఏమిటి?",
}


def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    source = source_language.get()
    target = target_language.get()

    if not text:
        messagebox.showwarning(
            "Missing Text",
            "Please enter some text to translate."
        )
        return

    if source not in LANGUAGES or target not in LANGUAGES:
        messagebox.showwarning(
            "Choose Languages",
            "Please select both languages."
        )
        return

    source_code = LANGUAGES[source]
    target_code = LANGUAGES[target]

    if source_code == target_code:
        messagebox.showwarning(
            "Choose Languages",
            "Please select two different languages."
        )
        return

    # Avoid excessively long requests to the demo service
    if len(text) > 450:
        messagebox.showwarning(
            "Text Too Long",
            "Please enter 450 characters or fewer at a time."
        )
        return

    key = (text.lower().strip(), source_code, target_code)

    translate_button.config(state="disabled", text="Translating...")
    status_label.config(text="Translating your text...")

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    root.update_idletasks()

    try:
        # Use known examples first
        if key in KNOWN_TRANSLATIONS:
            translated = KNOWN_TRANSLATIONS[key]

        else:
            response = requests.get(
                API_URL,
                params={
                    "q": text,
                    "langpair": f"{source_code}|{target_code}",
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()

            if str(data.get("responseStatus")) != "200":
                raise ValueError(
                    data.get("responseDetails")
                    or "The translation service is unavailable."
                )

            translated = data.get("responseData", {}).get(
                "translatedText", ""
            ).strip()

            # Do not claim success if the API returns the original text
            if not translated or translated.casefold() == text.casefold():
                raise ValueError(
                    "The service did not return a usable translation."
                )

        output_text.insert("1.0", translated)
        status_label.config(text="Translation completed.")

    except requests.RequestException:
        status_label.config(text="Translation failed.")
        messagebox.showerror(
            "Connection Error",
            "Could not contact the translation service.\n\n"
            "Check your internet connection and try again later."
        )

    except (ValueError, KeyError, TypeError) as error:
        status_label.config(text="Translation unavailable.")
        messagebox.showerror(
            "Translation Error",
            f"Could not translate this text.\n\n{error}"
        )

    finally:
        output_text.config(state="disabled")
        translate_button.config(state="normal", text="Translate")


def copy_translation():
    translated = output_text.get("1.0", tk.END).strip()

    if not translated:
        messagebox.showinfo(
            "Nothing to Copy",
            "Please translate some text first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(translated)
    root.update()
    status_label.config(text="Translation copied to clipboard.")


def clear_text():
    input_text.delete("1.0", tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

    status_label.config(text="Ready to translate.")


def swap_languages():
    source = source_language.get()
    target = target_language.get()

    source_language.set(target)
    target_language.set(source)

    status_label.config(text="Languages swapped.")


# Create the application window
root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("900x680")
root.minsize(700, 550)
root.configure(bg="#f1f5f9")

# Configure styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", padding=8)
style.configure("TButton", padding=8, font=("Segoe UI", 10))

# Header
header = tk.Frame(root, bg="#172554", padx=25, pady=22)
header.pack(fill="x")

tk.Label(
    header,
    text="Language Translation Tool",
    font=("Segoe UI", 23, "bold"),
    bg="#172554",
    fg="white",
).pack(anchor="w")

tk.Label(
    header,
    text="Translate text between different languages",
    font=("Segoe UI", 11),
    bg="#172554",
    fg="#dbeafe",
).pack(anchor="w", pady=(5, 0))

# Main content
main = tk.Frame(root, bg="#f1f5f9", padx=25, pady=20)
main.pack(fill="both", expand=True)

# Language selectors
selectors = tk.Frame(main, bg="#f1f5f9")
selectors.pack(fill="x", pady=(0, 15))

tk.Label(
    selectors,
    text="Source language",
    bg="#f1f5f9",
    font=("Segoe UI", 10, "bold"),
).grid(row=0, column=0, sticky="w", padx=(0, 10))

tk.Label(
    selectors,
    text="Target language",
    bg="#f1f5f9",
    font=("Segoe UI", 10, "bold"),
).grid(row=0, column=1, sticky="w", padx=10)

source_language = ttk.Combobox(
    selectors,
    values=list(LANGUAGES.keys()),
    state="readonly",
)
source_language.set("English")
source_language.grid(
    row=1, column=0, sticky="ew", padx=(0, 10), pady=6
)

target_language = ttk.Combobox(
    selectors,
    values=list(LANGUAGES.keys()),
    state="readonly",
)
target_language.set("Telugu")
target_language.grid(
    row=1, column=1, sticky="ew", padx=10, pady=6
)

selectors.columnconfigure(0, weight=1)
selectors.columnconfigure(1, weight=1)

# Text panels
panels = tk.Frame(main, bg="#f1f5f9")
panels.pack(fill="both", expand=True)

left_panel = tk.Frame(panels, bg="white", padx=12, pady=12)
left_panel.grid(
    row=0, column=0, sticky="nsew", padx=(0, 8)
)

right_panel = tk.Frame(panels, bg="white", padx=12, pady=12)
right_panel.grid(
    row=0, column=1, sticky="nsew", padx=(8, 0)
)

tk.Label(
    left_panel,
    text="Your text",
    bg="white",
    font=("Segoe UI", 11, "bold"),
).pack(anchor="w", pady=(0, 8))

input_text = tk.Text(
    left_panel,
    wrap="word",
    font=("Segoe UI", 11),
    relief="flat",
    padx=8,
    pady=8,
    bg="#f8fafc",
    height=12,
)
input_text.pack(fill="both", expand=True)

tk.Label(
    right_panel,
    text="Translated text",
    bg="white",
    font=("Segoe UI", 11, "bold"),
).pack(anchor="w", pady=(0, 8))

output_text = tk.Text(
    right_panel,
    wrap="word",
    font=("Segoe UI", 11),
    relief="flat",
    padx=8,
    pady=8,
    bg="#f8fafc",
    height=12,
    state="disabled",
)
output_text.pack(fill="both", expand=True)

panels.columnconfigure(0, weight=1)
panels.columnconfigure(1, weight=1)
panels.rowconfigure(0, weight=1)

# Buttons
actions = tk.Frame(main, bg="#f1f5f9")
actions.pack(fill="x", pady=15)

translate_button = tk.Button(
    actions,
    text="Translate",
    command=translate_text,
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    padx=24,
    pady=10,
    cursor="hand2",
)
translate_button.pack(side="left")

ttk.Button(
    actions,
    text="Swap Languages",
    command=swap_languages,
).pack(side="left", padx=8)

ttk.Button(
    actions,
    text="Copy Translation",
    command=copy_translation,
).pack(side="left", padx=8)

ttk.Button(
    actions,
    text="Clear",
    command=clear_text,
).pack(side="left", padx=8)

# Status
status_label = tk.Label(
    main,
    text="Ready to translate.",
    bg="#f1f5f9",
    fg="#475569",
    font=("Segoe UI", 9),
)
status_label.pack(anchor="w")

# Footer
tk.Label(
    root,
    text="Language Translation Tool | Educational Demo",
    bg="#e2e8f0",
    fg="#475569",
    font=("Segoe UI", 9),
    pady=9,
).pack(fill="x")

# Start application
root.mainloop()
