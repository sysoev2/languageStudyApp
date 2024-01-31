import tkinter as tk


class Input(tk.Entry):
    def __init__(
        self,
        master=None,
        placeholder="Enter text here",
        color="grey",
        show=None,
        **options
    ):
        self.show = show  # Store the masking character
        options["show"] = (
            "" if show else None
        )  # Temporarily disable masking to show the placeholder
        super().__init__(master, **options)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)
        self.bind("<KeyPress>", self._key_press)  # New event binding

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color
        self["show"] = ""  # Ensure placeholder is visible

    def _focus_in(self, event):
        if self["fg"] == self.placeholder_color:
            self.delete("0", "end")
            self["fg"] = self.default_fg_color
            self["show"] = "" if self.show and not self.get() else self.show

    def _focus_out(self, event):
        if not self.get():
            self.put_placeholder()
        else:
            self["show"] = self.show  # Reinstate masking when the entry has content

    def _key_press(self, event):
        if self["fg"] == self.placeholder_color and not self.get():
            self.delete("0", "end")
            self["fg"] = self.default_fg_color
        self["show"] = self.show  # Enable masking on key press

    def clear(self):
        self.delete(0, tk.END)
        self.put_placeholder()

    def get(self):
        if self["fg"] == self.placeholder_color:
            return ""
        return super().get()
