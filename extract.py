import pandas as pd
from bs4 import BeautifulSoup


def get_review_data(review):
    ''' Retrun a dictionary object of review data.
        Contains 'id', 'name', 'rating', 'time', 'text'. '''
    
    data = dict()
    data["id"] = review.attrs["data-review-id"]

    # getting name
    data["name"] = review.parent.attrs["aria-label"]

    # getting rating
    data["rating"] = review.select_one(
        "span[aria-label$='stars'], span[aria-label$='star']"
    ).attrs["aria-label"]

    # getting review text
    text_tag = review.select_one(f"#{data['id']} > span")
    if text_tag:
        data["text"] = text_tag.text

    return data


def main():
    # opens the file with page source 
    with open("test.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "lxml")

    # find all the reviews 
    reviews = soup.select("div[data-review-id] > div[data-review-id]")

    # get review data
    review_data = []
    for review in reviews:
        review_data.append(get_review_data(review))
    
    df = pd.DataFrame(review_data)
    df.to_csv("output.csv", sep=";", index=False)


if __name__ == "__main__":
    main()    
    