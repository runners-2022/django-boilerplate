# Third Party
from bs4 import BeautifulSoup


# Main Section
def extract_content_summary(content):
    soup = BeautifulSoup(content, features='html.parser')

    # Extract <style> Tags
    for style_tag in soup.find_all('style'):
        style_tag.extract()

    # Combine the text
    text_parts = soup.find_all(text=True)
    text_parts_filtered = filter(lambda text_part: len(text_part.strip()) >= 1, text_parts)
    content_summary = ' '.join(text_parts_filtered)

    return content_summary
