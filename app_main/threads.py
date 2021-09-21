import threading
from django.conf import settings
from django.core.mail import send_mail


class send_transaction_email(threading.Thread):
    def __init__(self, reciever, sender, amt):
        self.sender = sender
        self.reciever = reciever
        self.amt = amt
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "You recieved a gift"
            message = f"You recieved {self.amt} points from {self.sender}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message ,email_from, [self.reciever])
        except Exception as e:
            print(e)


class send_request_email(threading.Thread):
    def __init__(self, reciever, asker, amt):
        self.reciever = reciever
        self.asker = asker
        self.amt = amt
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Can u give me a few credits...??"
            message = f"{self.asker} has asked for {self.amt} points.\nWould you like to donate ?"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [self.reciever])
        except Exception as e:
            print(e)


class buy_request_email(threading.Thread):
    def __init__(self, buyer, seller, book):
        self.buyer = buyer
        self.seller = seller
        self.book = book
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Buy request"
            message = f"{self.buyer.name} ({self.buyer.email}) has put up a buy request for {self.book}.\nWould you like to sell ?"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [self.seller])
        except Exception as e:
            print(e)


class transaction_email(threading.Thread):
    def __init__(self, buyer, seller, book):
        self.buyer = buyer
        self.seller = seller
        self.book = book
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Transaction Successfull"
            message = f"Transaction successfull, between {self.buyer.name} and {self.sender.name} for the book {self.book}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [self.buyer.email])
            send_mail(subject, message, email_from, [self.seller.email])
        except Exception as e:
            print(e)