from src.Observer.AbstractObserver import AbstractObserver


class UserLoginObserver(AbstractObserver):
    EVENT_NAME = "user_login"

    def update(self, observable, *args, **kwargs):
        if observable.get_user() is not None:
            observable.show_card_group()
            observable.show_sidebar()
            return
        observable.show_login()
        observable.hide_sidebar()
