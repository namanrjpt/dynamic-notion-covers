
from datetime import date, datetime
from io import BytesIO
from xml.dom.pulldom import CHARACTERS
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import requests
from urlpath import URL
from pprint import pprint
import textwrap



def useless_facts(theme=None):
    QUOTE = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()['text']


def inspiring_quotes(theme=None):
    res = requests.get("https://api.fisenko.net/v1/quotes/en/random").json()
    TEXT = res['text']
    AUTHOR = res['author']['name']


def james_clear(theme=None):
    res = requests.get("https://www.jcquotes.com/api/quotes/random").json()
    TEXT = res['text']


    
    

def day_night_covers():
    pass




