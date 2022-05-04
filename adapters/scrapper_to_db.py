from datetime import datetime

def adapt_scrapped_book_to_internal(scrapped_book):
    # Convert [Tuesday May 3, 2022] to a python date object
    scrapped_book['last_accessed'] = datetime.strptime(scrapped_book['last_accessed'], '%A %B %d, %Y')
    scrapped_book['highlights'] = list(map(lambda highlight: {'text': highlight, 'isFavorite': False}, scrapped_book['highlights']))
    return scrapped_book