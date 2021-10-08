import os
from fpdf import FPDF
import urllib.request
import requests
from bs4 import BeautifulSoup
import string
import time



class PDFGenerator:

  def __init__(self):
    if(os.path.exists('pdf')):
      os.system('rm -rf pdf')
    os.mkdir('pdf')


  def generatePDF(self, base_url, title):
    if(os.path.exists('book')):
      os.system('rm -rf book')
    os.mkdir('book')

    pdf = FPDF("P", "mm", "A4")
    url = base_url + '/book/images/' 

    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    count = 0
    total = (len(soup.find_all('a')) - 5 )/ 2
    processing_count = 0
    for link in soup.find_all('a'):
      count+=1
      if(count > 5 ):
        processing_count += 1
        image_url = url + link.get('href')
        if not ('mini' in image_url):
          print('Processing: ' + image_url + ' - ' + self.compute_progression(processing_count / 2, total))
          urllib.request.urlretrieve(image_url, "book/tmp_"+(f"{processing_count:04}")+".jpg")
          pdf.add_page()
          pdf.image("book/tmp_"+(f"{processing_count:04}")+".jpg", 0, 0, 210,297)
    pdf.output('pdf/' + title + ".pdf")

  def compute_progression(self, progression, total):
    return (str)(round(progression * 100 / total)) + ' %'

def main():
  
  pdfgen = PDFGenerator()

  url = 'http://www.childrenslibrary.org/library/lang58.html'

  r = requests.get(url)
  content = r.content

  soup = BeautifulSoup(content.decode('utf-8','ignore'), 'html.parser')
  
  urls = []
  count = 0
  total_books =  (len(soup.find_all('a'))) - 8
  for link in soup.find_all('a'):
    if('books/' in link.get('href')):
      count+=1      
      images_href = url.replace('/lang58.html', '') + '/' + link.get('href').replace('/index.html', '')
      print("Book " + str(count) + "/" + str(total_books) + " : " + link.text)
      pdfgen.generatePDF(images_href, link.text)


if __name__ == "__main__":
  start_time = time.time()
  main()
  print("--- %s seconds ---" % (time.time() - start_time))