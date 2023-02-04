# Allergen Scraper

While reading the allergen page at Domino's, I felt like making a scraper to get the table and being able to view it in a better manner on, say, Google Sheets, you know, with filters and stuff.

And that it had been a while since I used BS4 so thought this would be a good refresher.

## Requirements

- Python 3.x
- pandas
- requests
- bs4

## Usage

```shell
python scrape.py
```

This will generate two files `pizza.csv` and `sides.csv` in the directory.

## Reference

- [Allergen Information(Pizzas) | Domino's Pizza Japan](https://www.dominos.jp/en/allergen-pizzas-information)
- [Allergen Information(Sides) | Domino's Pizza Japan](https://www.dominos.jp/en/allergen-sides-information)
