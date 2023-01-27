
class newUserEmail:
    def __init__(self, username):
        self.subject = "Welcome to Litbrary!"
        self.message = f'''
        Hi {username}!\n
        Thank you for registering for Litbrary accounts. We welcome you to access thousands of books in our library. Feel free to come to our place at:\n
        
        Address: Nanyang Cres, Blk 25 38, Singapore 636866\n
        Opening Hours: 10.00 AM - 10.00 PM\n
        Contant Number: 1234 5678\n
        
        Warmest regards,
        Bernard L.E. & Kevin L.G.
    '''

class newBorrowingEmail:
    def __init__(self, username, id, bookName, startDate, endDate):
        self.subject = f"Borrowing Receipt: {bookName}"
        self.message = f'''
        Dear {username}!\n
        We are happy to lend our books to you! Your borrowing details are listed below:\n
        
        Book Title: {bookName}\n
        Borrowing ID: {id}\n
        Starting Date: {startDate}\n
        Returning Date: {endDate}\n
        
        Please return the book according to the returning date. We will charge late return or book damage as written in our borrowing policy. \n
        
        Thank you for using our service on Litbrary!\n
        
        Litbrary\n
        Nanyang Cres, Blk 25 38, Singapore 636866
    '''