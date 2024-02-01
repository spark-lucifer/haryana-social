from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from .models import LinkPost
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LinkPost
    template_name = 'zoom/link-delete.html'
    success_url = reverse_lazy('index')
    def test_func(self) :
        post = self.get_object()
        return self.request.user == post.author
def scrape_website(url):
    # Set up a Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get(url)
    
    # Wait for the presence of 'chakra-heading'
    wait_for_element(driver, '.chakra-heading')

    # Get the HTML content after the page has loaded
    html = driver.page_source

    # Close the browser window
    driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    # Extract the text content from the webpage
    paragraph_list = extract_paragraphs(soup)
    content_list = extract_content_list(soup)

    return content_list


def wait_for_element(driver, selector):
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    WebDriverWait(driver, timeout=10).until(element_present)


def extract_paragraphs(soup):
    chakra_text_elements = soup.find_all('p', class_='chakra-text')
    paragraph_list = [text_content.get_text(strip=True) for text_content in chakra_text_elements]
    return paragraph_list


def extract_content_list(soup):
    elements = soup.find_all(class_='css-46p1lt')
    links = [a['href'] for h2 in soup.find_all('h2', class_='chakra-heading') for a in h2.find_all('a')]
    title = [link[10:] for link in links]
    linkarray = ['https://aa-intergroup.org' + link for link in links]
    content_list = []
    for i in range(5):
        cleaned_paragraph = elements[i].get_text(separator=' ').replace(',', '').replace('[', '').replace(']', '')
        content_list.append({
            'link': linkarray[i],
            'title': title[i],
            'paragraph': cleaned_paragraph,
        })
    return content_list
# Call the function with the URL and store the result in the 'content' variable

content = scrape_website('https://aa-intergroup.org/meetings/')
def home(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Process the form data
        title = request.POST['title']
        body = request.POST['body']
        link = request.POST['link']
        link1 = request.POST['link1']
        link2 = request.POST['link2']
        # Create a new LinkPost object
        post = LinkPost.objects.create(title=title, body=body, link=link, link1=link1, link2=link2, author=request.user)
        # Redirect to the home view
        return redirect('index')
    host = LinkPost.objects.all().order_by('-created_on')
    # Call the function with the URL and store the result in the 'content' variable

    # Pass the 'content' variable to the template
    return render(request, 'zoom/index.html', {'content':content,'host':host})