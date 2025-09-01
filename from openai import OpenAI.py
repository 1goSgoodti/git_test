import feedparser
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI

#fetch news articles
rss_url = "https://news.google.com/rss/search?q=Intel+Corporation"
feed = feedparser.parse(rss_url)

articles = []
for entry in feed.entries[:10]:
    print(entry)
    articles.append({
        "title": entry.title,
        "link": entry.link,
        "summary": entry.summary if "summary" in entry else ""
    })



#pick 3 and summarize
client = OpenAI(api_key="my_key")

article_text = "\n\n".join([f"{i+1}.{a['title']} - {a['summary']}" for i, a in enumerate(articles)])

prompt = f"""
Here are some recent articles about Intel Corporation:

{article_text}

Please:
1. Rank the top 3 most relevant articles to Intel (ignore general tech/finance unless Intel is central to the article).
2. Summarize each selected article in 2-3 sentences.
3. Provide the output as a clean formatted newsltter.

"""



response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt}]
)

newsletter_content = response.choices[0].message.content

#send email
sender = "1goSgoodti@gmail.com"
receiver = "1goSgoodti@gmail.com"
password = "tgbw vhle uzaz uonc"

msg = MIMEText(newsletter_content, "plain")
msg["Subject"] = "Daily Intel Corporation News"
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
