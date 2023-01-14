from catalog.models import Book
import csv


def run():
    with open('scripts/books.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Book.objects.all().delete()

        for row in reader:
            print(row)

            book = Book(
                        title=row[3],
                        author=row[4],
                        publisher=row[6],
                        pubYear=row[5],
                        imgUrl = row[7],
                        isbn = row[2],
                        category = row[9],
                        desc = row[8],
                        borrowed = row[10]
                        )
            
            book.save()
            