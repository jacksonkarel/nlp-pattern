import wikipedia

def wiki(page_title, output):
    page = wikipedia.page(page_title)
    content = page.content
    with open(output, 'w') as f:
        f.write(content)