import tkinter as tk


class ModalWindow(tk.Toplevel):
    def __init__(self, parent, title=None, initial_value=None):
        super().__init__(parent)
        self.transient(parent)  # Set to be a transient window of the parent
        self.title(title or "Enter Name")

        self.result = None  # The result is None unless the user enters a value
        self.initial_value = initial_value  # The initial value for the entry, if any
        self.parent = parent  # Keep a reference to the parent window

        # Create and pack the body frame
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        # Create and pack the button box®
        self.buttonbox()

        # Set window to grab focus
        self.grab_set()

        # Set initial focus
        if not self.initial_focus:
            self.initial_focus = self

        # Handle closing the window
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # Position the window relative to the parent
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        # Wait for the window to finish
        self.wait_window(self)

    def body(self, master):
        # Create and grid the label and entry in the body frame
        label = tk.Label(master, text="Name:")
        label.grid(row=0)

        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1)
        if self.initial_value:
            # If there's an initial value, insert it into the entry and select it
            self.entry.insert(0, self.initial_value)
            self.entry.select_range(0, tk.END)

        return self.entry

    def buttonbox(self):
        # Create a frame to hold the buttons
        box = tk.Frame(self)

        # Create OK and Cancel buttons and pack them into the box
        ok_button = tk.Button(
            box, text="OK", width=10, command=self.ok, default=tk.ACTIVE
        )
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Bind the Return key to ok and the Escape key to cancel
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        # When OK is clicked, set the result to the entry's value and close
        self.result = self.entry.get()
        self.parent.focus_set()  # Return focus to the parent window
        self.destroy()  # Close the modal window

    def cancel(self, event=None):
        # When Cancel is clicked, just close the modal without setting result
        self.parent.focus_set()  # Return focus to the parent window
        self.destroy()  # Close the modal window
