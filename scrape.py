import requests
import bs4
import pandas as pd


def header(table):
    """Generates list of headers from original bs4 soup of tabular data"""
    head_tag = table.find("thead").find_all("td")
    hdr = []
    for tag in head_tag:
        if tag["class"][0] == "ProductCell":
            hdr.append(tag.text)
            continue
        letters = tag.prettify().replace("<br/>\n <br/>", "<br/>\n  <br/>"
                                         ).replace("<br/>", "").split("\n")[1:-2]
        hdr.append("".join(l[1:] for l in letters))
    return hdr


def minimize(cls: str):
    """Minimizes the class to useful information only"""
    cls_type = cls.split('_')[1]
    if cls_type[0] == 'C':
        return "●"
    elif cls_type[0] == 'D':
        return "－"
    elif "Store" in cls_type:
        return "▽"
    else:
        return "▲"


def body(table):
    """Generates list of rows from original bs4 soup of tabular data"""
    body = table.find("tbody").find_all("tr")
    dat = []
    this_category = ''
    for row in body:
        entry = []
        firstProduct = True
        rEntry = row.find_all("td")
        for tag in rEntry:
            if tag["class"][0] == "ProductCell" and firstProduct:
                category = tag.text
                if category != "\xa0":   # Since the category is brought from top; if new, update
                    this_category = category
                entry.append(this_category)
                firstProduct = False
                continue
            elif tag["class"][0] == "ProductCell":
                # Since sides has only one product cell, this automatically works out
                entry.append(tag.text[1:])
                continue
            entry.append(minimize(tag["class"][1]))
        dat.append(entry)
    return dat


def pull(URL: str, isPizza: bool):
    """
    Pulls the data from the allergen URL and converts into simple DataFrame
    Designed for the URLs https://www.dominos.jp/en/allergen-(type)-information 
    """
    soup = bs4.BeautifulSoup(requests.get(URL).content, "html.parser")
    table = soup.find("table", attrs={"class": "AllergenNutritionInfoTable"})
    hdr = header(table)
    if isPizza:
        # Since the table for Pizza has an empty column
        hdr.insert(0, "Category")
    dat = body(table)
    df = pd.DataFrame(dat, columns=hdr)
    return df


def save(URL: str, key: str):
    isPizza = key == "pizza"
    df = pull(URL, isPizza)
    df.to_csv(key+".csv", index=False)


def main():
    PIZZA_URL = "https://www.dominos.jp/en/allergen-pizzas-information"
    SIDES_URL = "https://www.dominos.jp/en/allergen-sides-information"
    save(PIZZA_URL, "pizza")
    save(SIDES_URL, "sides")


if __name__ == "__main__":
    main()
