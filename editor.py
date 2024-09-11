from bs4 import BeautifulSoup


def add_links_to_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Keep track of the article and paragraph numbers
    article_count = 0
    paragraph_count = 0
    sub_paragraph_count = 0

    # Iterate through all elements
    for element in soup.find_all("p"):
        text = element.get_text(strip=True)

        # Check for articles
        if text.startswith("Статья"):
            try:
                article_count = text.strip('.').split()[1]
            except Exception as e:
                print(text)
                raise e
            article_ident = f"article_{article_count}"
            anchor = soup.new_tag("a", id=article_ident)
            element.insert(0, anchor)

            # Check for sub-paragraphs (k)
        elif text and text[0].isdigit() and (text[1] == ')' or text[1].isdigit() and text[2] == ')'):
            sub_paragraph_count = text.split()[0].strip(')')
            sub_paragraph_ident = f"sub_paragraph_{article_count}_{paragraph_count}_{sub_paragraph_count}"
            anchor = soup.new_tag("a", id=sub_paragraph_ident)
            element.insert(0, anchor)

        # Check for regular paragraphs (j)
        elif text and text[0].isdigit() and not text[1].isspace():
            paragraph_count = text.split()[0].strip('.')
            paragraph_ident = f"paragraph_{article_count}_{paragraph_count}"
            anchor = soup.new_tag("a", id=paragraph_ident)
            element.insert(0, anchor)

        # Reset counts for new articles
        if text.startswith("Статья") or (len(text) == 0 and element.find_previous("table")):
            paragraph_count = 0
            sub_paragraph_count = 0

    for element in soup.find_all("p"):
        text = element.get_text(strip=True)

    return str(soup)


with open('laborlaw_ru.html') as f:
    html = f.read()

new_html = add_links_to_html(html)


with open('laborlaw_edited.html', 'w') as f:
    f.write(new_html)
