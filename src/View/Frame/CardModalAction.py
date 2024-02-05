import tkinter as tk


class CardModalAction(tk.Toplevel):
    def __init__(self, parent, title=None, initial_value=None):
        super().__init__(parent)
        self.transient(parent)  # Set to be a transient window of the parent
        self.title(title or "Card Details")

        self.result = None  # The result is None unless the user enters values
        self.initial_value = (
            initial_value if initial_value else {"front": "", "back": ""}
        )
        self.parent = parent  # Keep a reference to the parent window

        # Create and pack the body frame
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        # Create and pack the button box
        self.buttonbox()

        # Set window to grab focus
        self.grab_set()

        # Set initial focus
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)  # Handle closing the window
        self.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50)
        )  # Position the window

        self.initial_focus.focus_set()
        self.wait_window(self)  # Wait for the window to finish

    def body(self, master):
        # Create and grid labels and entries for front and back text
        tk.Label(master, text="Front Text:").grid(row=0)
        tk.Label(master, text="Back Text:").grid(row=1)

        self.front_entry = tk.Entry(master)
        self.back_entry = tk.Entry(master)

        self.front_entry.grid(row=0, column=1)
        self.back_entry.grid(row=1, column=1)

        # If there are initial values, insert them into the entries
        self.front_entry.insert(0, self.initial_value["front"])
        self.back_entry.insert(0, self.initial_value["back"])

        return self.front_entry  # Set the initial focus to the front text entry

    def buttonbox(self):
        # Create a frame to hold the buttons
        box = tk.Frame(self)

        # Create OK and Cancel buttons
        ok_button = tk.Button(
            box, text="OK", width=10, command=self.ok, default=tk.ACTIVE
        )
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)

        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)  # Bind Return key to OK
        self.bind("<Escape>", self.cancel)  # Bind Escape key to Cancel

        box.pack()

    def ok(self, event=None):
        # Store the front and back text as a result and close the window
        self.result = {"front": self.front_entry.get(), "back": self.back_entry.get()}
        self.parent.focus_set()  # Return focus to the parent window
        self.destroy()  # Close the modal window

    def cancel(self, event=None):
        self.result = None
        self.parent.focus_set()  # Return focus to the parent window
        self.destroy()  # Close the modal window
