# FilmNet Scraper

This Scrapy project is designed to retrieve movie information from the FilmNet API, including movie details, categories, and artists, and store it in a Django database. It also downloads poster images for each movie and saves them in the images directory within the project root.

## requirements

Python 3.x

- Scrapy

- Django

- DjangoItem

- Requests library

- PIL or Pillow (for image processing)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/filmnet-scraper.git
```

Install required Python libraries:

```bash
pip install -r requirements.txt
```

## Usage/Examples

1. Run the Django server(for getting access to admin panel):

   ```bash
   python manage.py runserver
   ```

2. Run the spider:

   ```bash
   python manage.py crawl_filmnet
   ```
