from tkinter import messagebox


class ValidatorErrorsHelper:

    @staticmethod
    def show_errors(errors: dict[str, str]) -> None:
        messagebox.showerror(
            "Error", "\n\n".join(f"{field}: {error}" for field, error in errors.items())
        )
