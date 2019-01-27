import requests
from bs4 import BeautifulSoup




def requestpage(url):
    try:
        code = requests.get(url)
        plain = code.text
        
    except HTTPError as e:
        return None
    try:
        soup = BeautifulSoup(plain, "html.parser")
    except AttributeError as e:
        
        return None
    return soup


def getLinksFromPage(s):
    linksNews = []

    big_items = s.findAll('div', attrs={'class': 'news_big_item'})
    for it in big_items:
        linksNews.append(it.a.get("href"))
    
    newslists = s.find('ul', attrs={'class': 'news_list'})
    news = newslists.findAll('li')
    
    for link in news:
        linksNews.append(link.a.get("href"))
        
    print("\n----------------page's news links are scrapped!\n-----------------")
    return linksNews




def getHTML(url):
    try:
        code = requests.get(url)
        plain_text = code.text
        
    except HTTPError as e:
        return None
    try:
        detail_page = BeautifulSoup(plain_text, "html.parser")
    except AttributeError as e:
        return None
    return plain_text, detail_page



def getScrappedData(plain,detail_page):
    article= detail_page.find('div', attrs={'class': 'main_bar fl news_article'})
    title = article.h1.text
    short_detail = article.h2.text
    date_time_tags= detail_page.findAll('span', attrs={'class': 'article-date'})
    ad=0
    date_n_time =""
    for dt in date_time_tags:
        if ad == 2:
            date_n_time = dt.text
        ad = ad +1
    
    date_n_time = date_n_time.replace("\n ",'')
    date,time = date_n_time.split("| ")    
    
    article_story = detail_page.find('div', attrs={'class': 'detail_txt'}  )
    starting_index = plain.find('<div class="detail_txt">')
    ending_index = plain.find('<div class="social_sharer">')
    
    text = plain[starting_index:ending_index]
    
    
    detail_txt = BeautifulSoup(text, "html.parser")
    
    [x.extract() for x in detail_txt.findAll(['h2','script','style'])]
    
    det_text = detail_txt.find("div").get_text()
    det_text = det_text.strip("\n")
    
    childt = detail_txt.findChildren("p")
    pTagtxt =""
    for p in childt:
        pTagtxt = pTagtxt + p.get_text().strip('\n')
        pTagtxt = pTagtxt + '\n'    
        
    article_story_text = det_text+ "\n" + pTagtxt
    
    return title, short_detail, date, time, article_story_text






# Main Starts Here

import xlsxwriter
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('CrimeNews.xlsx')
worksheet = workbook.add_worksheet()
row = 1
col = 0

#Main loop for getting news stories from multiple pages    
for page in range(1,21):  
    main_page_url = "https://www.urdupoint.com/en/news/pakistan/crime-updates"+ str(page) + ".html"
    print(main_page_url)
    soup = requestpage(main_page_url)
    newsLinksList = getLinksFromPage(soup)
    
    #loop for requesting multiple news stories
    for item in newsLinksList:
        article_url = item
        plain_text, soup_page = getHTML(article_url)
        title, short_detail, date, time, article_story_text = getScrappedData(plain_text,soup_page)
        #write to file
        worksheet.write(row, col,  main_page_url)
        worksheet.write(row, col + 1, article_url)
        worksheet.write(row, col + 2, date)
        worksheet.write(row, col + 3, time)
        worksheet.write(row, col + 4, title)
        worksheet.write(row, col + 5, short_detail)
        worksheet.write(row, col + 6, article_story_text)
        print("\n {0} story is written... ".format(row))
        row += 1
   


workbook.close()

