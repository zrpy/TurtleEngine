import flask,requests,urllib
from bs4 import BeautifulSoup
import logging


log = logging.getLogger('werkzeug')
log.disabled = True

app=flask.Flask(__name__)
host="localhost:8080"
proxy={"http":"socks5h://localhost:9050","https":"socks5h://localhost:9050"}

def searchduck(q):
  r=requests.get("https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/html/?q="+q+"&kl=jp-jp",headers={"user-agent":"Mozilla/5.0","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"},proxies=proxy)
  parse=BeautifulSoup(r.text, "html.parser")
  datas={}
  count=0
  for result in parse.findAll("div", {"class": "result results_links results_links_deep web-result"}):
    links=result.find("a", {"class": "result__a"})
    description=result.find("a", {"class": "result__snippet"}).text
    datas[count]={}
    datas[count]["title"]=links.text
    datas[count]["description"]=description
    datas[count]["url"]=str(urllib.parse.unquote("https://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion/"+links["href"]).split("/l/?uddg=")[1]).split("&rut=")[0]
    datas[count]["icon"] = "https:"+result.find("img", {"class": "result__icon__img"}).attrs["src"]
    count+=1
  return datas
    



@app.route("/")
def index():
  return flask.render_template("index.html")

@app.route("/search",methods=["GET","POST"])
def search():
  if "q" in flask.request.args or flask.request.form:
    q=flask.request.args["q"]
    searchresult=searchduck(q)
    return flask.render_template("search.html",searchs=searchresult,q=q)
  elif not "q" in flask.request.args or flask.request.form:
    return flask.redirect(host)

app.run(port=8080,debug=True)
