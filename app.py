import sys
from pathlib import Path
import threading
import tkinter as tk
from tkinter import PhotoImage, ttk, filedialog
from playsound import playsound

from main import gen_audio, get_price


class PDFtoMP3Converter:
    def __init__(self):
        self.root = tk.Tk()
        self._configure_root()
        self._create_widgets()
        self.root.mainloop()

    def _configure_root(self):
        self.root.title("PDF to MP3 Converter")
        self.root.geometry("585x400")
        # self.root.resizable(False, False)
        self.root.tk.call("source", "Azure-ttk-theme/azure.tcl")
        self.root.tk.call("set_theme", "dark")

    def _create_widgets(self):
        title_label = ttk.Label(
            self.root, text="PDF to Audio Book", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.file_label_text = tk.StringVar(value="Select your PDF")
        file_label = ttk.Label(self.root, textvariable=self.file_label_text)
        file_button = ttk.Button(
            self.root, text="Browse", command=self._select_pdf)

        self.folder_label_text = tk.StringVar(
            value="Choose folder to save file")
        folder_label = ttk.Label(
            self.root, textvariable=self.folder_label_text)
        folder_button = ttk.Button(
            self.root, text="Browse", command=self._select_folder)

        options = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        self.options_var = tk.StringVar(value=options)
        dropdown_label = ttk.Label(self.root, text="Select a voice:")
        dropdown = ttk.Combobox(self.root, values=options,
                                textvariable=self.options_var)
        dropdown.set("alloy")

        # photo = PhotoImage(file="assets/play30.png")
        play_sound_button_label = ttk.Label(self.root, text="Play sample:")
        play_sound_button = ttk.Button(
            self.root,  command=self._play, text="Sample")

        start_page_label = ttk.Label(
            self.root, text="Starting page (inclusive):")
        self.start_page_entry = ttk.Entry(self.root, validate="key", validatecommand=(
            self.root.register(self._validate_positive_integer), "%P"))

        end_page_label = ttk.Label(self.root, text="Ending page (inclusive):")
        self.end_page_entry = ttk.Entry(self.root, validate="key", validatecommand=(
            self.root.register(self._validate_positive_integer), "%P"))

        output_file_label = ttk.Label(
            self.root, text="Output MP3 file name (no file ext):")
        self.output_file_entry = ttk.Entry(self.root)

        estimate_price_button = ttk.Button(
            self.root, text="Estimate Price", command=self._estimate_price)
        generate_button = ttk.Button(
            self.root, text="Generate", command=self._generate)

        # Layout configuration
        file_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        file_button.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        folder_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        folder_button.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        dropdown_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        dropdown.grid(row=3, column=1, padx=10, pady=5)

        play_sound_button_label.grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        play_sound_button.grid(row=4, column=1, padx=10, sticky="e")

        start_page_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.start_page_entry.grid(row=5, column=1, padx=10, pady=5)

        end_page_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.end_page_entry.grid(row=6, column=1, padx=10, pady=5)

        output_file_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.output_file_entry.grid(row=7, column=1, padx=10, pady=5)

        estimate_price_button.grid(row=8, column=0, padx=10, pady=10)
        generate_button.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

    def display_message(self, message):
        # Create a new window
        new_window = tk.Tk()
        new_window.title("Message Display")

        new_window.tk.call("source", "Azure-ttk-theme/azure.tcl")
        new_window.tk.call("set_theme", "dark")
        # Configure window size and position
        new_window.geometry("300x100")

        # Create a label to display the message
        message_label = ttk.Label(new_window, text=message, wraplength=280)
        message_label.pack(expand=True)

        # Create a button to close the window
        close_button = ttk.Button(
            new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=10)

        # Start the Tkinter event loop
        new_window.mainloop()

    def _select_pdf(self):
        self.root.tk.call("set_theme", "light")

        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            file_name = Path(file_path).name
            self.file_label_text.set(file_name)
            self.full_file_path = file_path
        self.root.tk.call("set_theme", "dark")

    def _select_folder(self):
        self.root.tk.call("set_theme", "light")
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_name = Path(folder_path).name
            self.folder_label_text.set(folder_name)
            self.full_folder_path = folder_path
        self.root.tk.call("set_theme", "dark")

    def _play(self):
        voice = self.options_var.get()
        def play_anon(mp3File): playsound(mp3File)
        t1 = threading.Thread(target=play_anon, args=(
            f"assets/samples/{voice}.mp3", ))
        t1.start()

    def _validate_positive_integer(self, P):
        return str.isdigit(P) or P == ""

    def _generate(self):
        form_values = {
            "pdf_file_path": self.file_label_text.get(),
            "folder_path": self.folder_label_text.get(),
            "voice_selection": self.options_var.get(),
            "start_page": self.start_page_entry.get(),
            "end_page": self.end_page_entry.get(),
            "output_file_name": self.output_file_entry.get(),
        }
        try:
            file = gen_audio(self.full_file_path, self.full_folder_path, form_values["output_file_name"], int(
                form_values["start_page"]), int(form_values["end_page"]))
            self.display_message(f"Generated audio saved to {file}")
        except Exception as e:
            self.display_message(f"Failed to generate audio: {e}")

    def _estimate_price(self):
        form_values = {
            "pdf_file_path": self.file_label_text.get(),
            "folder_path": self.folder_label_text.get(),
            "voice_selection": self.options_var.get(),
            "start_page": self.start_page_entry.get(),
            "end_page": self.end_page_entry.get(),
            "output_file_name": self.output_file_entry.get(),
        }
        total_price_cents = get_price(self.full_file_path, int(
            form_values["start_page"]), int(form_values["end_page"]))
        total_price_dollars = total_price_cents / 100

        self.display_message(
            f"Price estimate: ${f'{total_price_dollars:.5f}' if total_price_dollars < 1 else f'{total_price_dollars:.2f}'}")


app = PDFtoMP3Converter()
