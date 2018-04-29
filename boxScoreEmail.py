from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def getData():
    
    r  = requests.get(url)
    data = r.text
    return BeautifulSoup(data, "lxml")

def send_email(html):
    
    FROM = my_email
    TO = my_email
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = my_team + " Box Score " + yesterday.strftime("%m.%d.%Y") + " -" + headline
    msg['From'] = FROM
    msg['To'] = TO
    
    contents = MIMEText(html, 'html')
    msg.attach(contents)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(my_email, my_password)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()

yesterday = datetime.now() - timedelta(1)
url = "https://www.rotowire.com/baseball/scoreboard.htm?d=" + yesterday.strftime("%m%d%Y")
my_team = "Mets"
my_team_city = "New York"

f = open("email.txt","r")
my_email = f.read()
f.close()

f = open("pw.txt","r")
my_password = f.read()
f.close()

soup = getData()

for game in soup.findAll("div", class_="offset1 span15 scorebox"):
    for team in game.findAll("div", class_="span7 scorebox-teamname"):
        if my_team in team.text:
            url = "https://www.rotowire.com" + game.a['href']
            
soup = getData()            

try:
    boxscore = soup.find("div", class_="boxalign")

    # clean up html
    boxscore.find("ul", id="playerstattab").decompose()
    for image in boxscore.findAll("img"):
        image.decompose()

    for i in range(5, 20):
        boxscore.findAll("table")[5].decompose()

    # find headline for subject
    for div in boxscore.findAll("div"):
        if my_team_city in div.text and "At" in div.text:
            headline = div.text
    
    # send email
    send_email("<html>\n" + str(boxscore) + "\n</html>")
    
except:
    pass

