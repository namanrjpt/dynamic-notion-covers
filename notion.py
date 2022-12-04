import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import shutil
from datetime import datetime, date
import pyaztro
import textwrap
from millify import millify
import instaloader
import praw, prawcore
from bs4 import BeautifulSoup
from urlpath import URL

DARK_STOIC_COVERS = [
    "https://i.imgur.com/1NqFrFV.jpg",
    "https://i.imgur.com/1ybI0DX.png",
    "https://i.imgur.com/2S29xNg.jpg",
    "https://i.imgur.com/2fTKAqB.jpg",
    "https://i.imgur.com/2kClSHz.jpg",
    "https://i.imgur.com/2sVBBka.jpg",
    "https://i.imgur.com/37lsoja.jpg",
    "https://i.imgur.com/3udF5vv.jpg",
    "https://i.imgur.com/41JzrSO.jpg",
    "https://i.imgur.com/5jORbaF.png",
    "https://i.imgur.com/6mifIgT.jpg",
    "https://i.imgur.com/6yqjDJQ.jpg",
    "https://i.imgur.com/7cGRXP4.jpg",
    "https://i.imgur.com/8Qlb6sx.jpg",
    "https://i.imgur.com/9JNJFJZ.jpg",
    "https://i.imgur.com/9cp8Yl5.jpg",
    "https://i.imgur.com/CN1KgjR.jpg",
    "https://i.imgur.com/Ctu4McN.jpg",
    "https://i.imgur.com/DYPlZDr.jpg",
    "https://i.imgur.com/E1vgEnP.png",
    "https://i.imgur.com/EyXLfvk.jpg",
    "https://i.imgur.com/FhchcrX.jpg",
    "https://i.imgur.com/GEpIKLX.jpg",
    "https://i.imgur.com/HfWBLIR.png",
    "https://i.imgur.com/JdljkJ3.jpg",
    "https://i.imgur.com/KG8Vyme.png",
    "https://i.imgur.com/KJ1Tse7.jpg",
    "https://i.imgur.com/KsP7kZI.jpg",
    "https://i.imgur.com/MRjUZQO.png",
    "https://i.imgur.com/NFb3oMa.png",
    "https://i.imgur.com/NY3GRAt.png",
    "https://i.imgur.com/PMdsRXI.jpg",
    "https://i.imgur.com/Pf8lwj1.jpg",
    "https://i.imgur.com/QGHNYet.png",
    "https://i.imgur.com/QPmH3fD.jpg",
    "https://i.imgur.com/ROwUqXi.jpg",
    "https://i.imgur.com/RoOMlD2.jpg",
    "https://i.imgur.com/TjiepYJ.jpg",
    "https://i.imgur.com/TpNk4tw.jpg",
    "https://i.imgur.com/TvFP4X6.png",
    "https://i.imgur.com/VNsIed8.jpg",
    "https://i.imgur.com/WdPjyPx.png",
    "https://i.imgur.com/XCvWUUM.jpg",
    "https://i.imgur.com/XSuff1Z.jpg",
    "https://i.imgur.com/Xj8ct0v.jpg",
    "https://i.imgur.com/XqbynfI.png",
    "https://i.imgur.com/YMIa1sY.jpg",
    "https://i.imgur.com/YgatBJU.jpg",
    "https://i.imgur.com/YlPZi2z.jpg",
    "https://i.imgur.com/dMkvTf1.png",
    "https://i.imgur.com/dPoK95O.png",
    "https://i.imgur.com/dx2CmOy.jpg",
    "https://i.imgur.com/fspyz7u.png",
    "https://i.imgur.com/gWtjhLU.png",
    "https://i.imgur.com/hrDhQZi.jpg",
    "https://i.imgur.com/idGUXi1.jpg",
    "https://i.imgur.com/ilojA5u.png",
    "https://i.imgur.com/jbBbzQV.jpg",
    "https://i.imgur.com/k5m4z3Y.jpg",
    "https://i.imgur.com/kWzxruO.jpg",
    "https://i.imgur.com/lEmwPEm.jpg",
    "https://i.imgur.com/mFyz11M.png",
    "https://i.imgur.com/mPKUxo5.png",
    "https://i.imgur.com/n0P7O0p.jpg",
    "https://i.imgur.com/oF3ZKAK.jpg",
    "https://i.imgur.com/oOCH13o.jpg",
    "https://i.imgur.com/oesf4fr.jpg",
    "https://i.imgur.com/qutLkAB.jpg",
    "https://i.imgur.com/rXckmrx.jpg",
    "https://i.imgur.com/tXGT5IY.png",
    "https://i.imgur.com/tYde41x.jpg",
    "https://i.imgur.com/tYh9RTM.jpg",
    "https://i.imgur.com/wKmi9pP.jpg"
]

LIGHT_STOIC_COVERS = [
    "https://i.imgur.com/0hVGUJe.png",
    "https://i.imgur.com/19qP2Ow.png",
    "https://i.imgur.com/22SOMGA.png",
    "https://i.imgur.com/24n4d4L.png",
    "https://i.imgur.com/2JhRWl4.jpg",
    "https://i.imgur.com/2L0XiCy.png",
    "https://i.imgur.com/2XiMyy7.png",
    "https://i.imgur.com/3KPTcfB.jpg",
    "https://i.imgur.com/3NbE2mG.png",
    "https://i.imgur.com/3OloKRk.jpg",
    "https://i.imgur.com/3xWcN6S.jpg",
    "https://i.imgur.com/6msGqVP.png",
    "https://i.imgur.com/6z4XzoI.jpg",
    "https://i.imgur.com/7ORu4vc.jpg",
    "https://i.imgur.com/7Y7Da1R.png",
    "https://i.imgur.com/8TyMmAc.png",
    "https://i.imgur.com/A5DINWI.png",
    "https://i.imgur.com/B9j3p1T.png",
    "https://i.imgur.com/DOzWKAh.png",
    "https://i.imgur.com/Dp4GOwV.png",
    "https://i.imgur.com/DzDXPF1.png",
    "https://i.imgur.com/E1ZBflz.png",
    "https://i.imgur.com/HEeH0aV.png",
    "https://i.imgur.com/IOLSttz.png",
    "https://i.imgur.com/Jf5QBlp.png",
    "https://i.imgur.com/KGqOxVX.png",
    "https://i.imgur.com/KGvvDYC.png",
    "https://i.imgur.com/KdESpmM.png",
    "https://i.imgur.com/LLvV5Ly.png",
    "https://i.imgur.com/NijEjPR.png",
    "https://i.imgur.com/NpTpTQK.png",
    "https://i.imgur.com/ORU3p2f.jpg",
    "https://i.imgur.com/Oa54EFm.png",
    "https://i.imgur.com/P12eoRR.png",
    "https://i.imgur.com/P5LRFkG.jpg",
    "https://i.imgur.com/P6P0rtz.jpg",
    "https://i.imgur.com/QKwZJcO.png",
    "https://i.imgur.com/R827mU2.png",
    "https://i.imgur.com/SuNysLl.png",
    "https://i.imgur.com/Xyk0HWM.png",
    "https://i.imgur.com/YouvWzM.png",
    "https://i.imgur.com/Yq3YIqZ.png",
    "https://i.imgur.com/a46uYNK.png",
    "https://i.imgur.com/aCRpcY2.jpg",
    "https://i.imgur.com/dKaiOcl.png",
    "https://i.imgur.com/ePuFrqZ.png",
    "https://i.imgur.com/eqWmvbP.png",
    "https://i.imgur.com/f501eHJ.png",
    "https://i.imgur.com/fPbwLSk.jpg",
    "https://i.imgur.com/g5G1dE8.png",
    "https://i.imgur.com/h6xmopU.png",
    "https://i.imgur.com/hioFOa6.png",
    "https://i.imgur.com/iIB7mCf.png",
    "https://i.imgur.com/iaivm9a.jpg",
    "https://i.imgur.com/jXoZIKj.png",
    "https://i.imgur.com/kBMj4ee.png",
    "https://i.imgur.com/l3Yu2lp.png",
    "https://i.imgur.com/n5tzWeP.png",
    "https://i.imgur.com/nHeSz98.jpg",
    "https://i.imgur.com/ont7BRN.png",
    "https://i.imgur.com/oz68my3.png",
    "https://i.imgur.com/p8tcnkT.png",
    "https://i.imgur.com/rOgHPwZ.png",
    "https://i.imgur.com/sBdgdlX.png",
    "https://i.imgur.com/t2kQvXA.png",
    "https://i.imgur.com/tAWQTAN.png",
    "https://i.imgur.com/uVpIZ8f.png",
    "https://i.imgur.com/uvD7mw8.png",
    "https://i.imgur.com/wISWk4l.png",
    "https://i.imgur.com/x09acJe.png",
    "https://i.imgur.com/xmKTxMo.png",
    "https://i.imgur.com/yD3DJ76.png",
    "https://i.imgur.com/yv1AQCj.jpg"
]

def download_stoic_quote(URL):
    response = requests.get(URL, stream=True)
    with open('./media/stoic_quote.png', 'wb') as outfile:
        shutil.copyfileobj(response.raw, outfile)
    del response

def create_weather_image(ip):
    latlong = requests.get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')
    API_KEY = '94e03d1e9bec379c279844da999765c1'

    weather = requests.get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latlong[0], latlong[1], API_KEY)).json()

    ICON_URL = 'https://openweathermap.org/img/wn/{}@2x.png'.format(str(weather['weather'][0]['icon']))
    MOOD = str(weather['weather'][0]['description']).capitalize()
    PLACE = weather['name']
    COUNTRY = weather['sys']['country']
    LAST_UPDATE = datetime.utcfromtimestamp(weather['dt']+weather['timezone']).strftime('%I:%M%p')
    TEMPERATURE  = str(round(float(weather['main']['temp'] - 273.15),2))+u'\N{DEGREE SIGN}'+"C"
    HUMIDITY  = str(weather['main']['humidity'])+"%"
    VISIBILITY = str(weather['visibility'])+"m"
    WIND_SPEED = str(weather['wind']['speed'])+"m/s"
    SUNRISE = datetime.utcfromtimestamp(weather['sys']['sunrise']+weather['timezone']).strftime('%I:%M%p')
    SUNSET = datetime.utcfromtimestamp(weather['sys']['sunset']+weather['timezone']).strftime('%I:%M%p')

    BASE_IMAGE = "https://i.imgur.com/pwdNhnM.png"
    MAX_W, MAX_H = 1500, 600
    im = Image.open(BytesIO(requests.get(BASE_IMAGE).content))
    draw = ImageDraw.Draw(im, "RGBA")
    font = ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 42)
    draw.text((204, 282), str(MOOD), font=font, align='left', fill=(0,0,0,255))
    draw.text((204, 330), str(PLACE), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 23), align='left', fill='#888')
    draw.text((204, 361), str(COUNTRY), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 20), align='left', fill='#888')
    country_icon = Image.open(BytesIO(requests.get("https://countryflagsapi.com/png/{}".format(str(COUNTRY).lower())).content)).resize((33,20))
    im.paste(country_icon, (245, 363))
    draw.text((270, 386), str(LAST_UPDATE), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 10), align='left', fill='#888')

    weather_icon_image = Image.open(BytesIO(requests.get(ICON_URL).content)).resize((106,106))
    im.paste(weather_icon_image, (200,175), weather_icon_image)

    draw.text((640, 215), str(TEMPERATURE), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')
    draw.text((914, 215), str(HUMIDITY), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')
    draw.text((1187, 215), str(VISIBILITY), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')
    draw.text((640, 325), str(WIND_SPEED), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')
    draw.text((914, 325), str(SUNRISE), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')
    draw.text((1187, 325), str(SUNSET), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')

    im.save('./media/weather_image.png')

def create_todays_horoscope(SIGN):
    zodiac_icons = {
        'aries' : 'https://i.imgur.com/ua1F9pO.png',
        'cancer': 'https://i.imgur.com/icVOFaY.png',
        'pisces': 'https://i.imgur.com/6OK25WL.png',
        'taurus': 'https://i.imgur.com/5TRswxq.png',
        'scorpio': 'https://i.imgur.com/tEiZglW.png',
        'aquarius': 'https://i.imgur.com/AGwqTRM.png',
        'virgo': 'https://i.imgur.com/7TSwYgw.png',
        'leo': 'https://i.imgur.com/AGYdGaa.png',
        'libra': 'https://i.imgur.com/eQdPcda.png',
        'capricorn': 'https://i.imgur.com/iF5NyX9.png',
        'sagittarius': 'https://i.imgur.com/2BGO2gg.png',
        'gemini': 'https://i.imgur.com/VBOW1PD.png'
    }

    horoscope = pyaztro.Aztro(sign=SIGN, day='today')
    # print(horoscope.compatibility)
    im = Image.open(BytesIO(requests.get("https://i.imgur.com/LcT3UYh.png").content))
    draw = ImageDraw.Draw(im, "RGBA")
    draw.text((190, 211), str(horoscope.sign).title(), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 32), align='left', fill='#000')
    draw.text((412, 211), str(horoscope.current_date).title(), font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 14), align='left', fill='#000')
    draw.text((793, 225), str(horoscope.lucky_number).title(), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 25), align='left', fill='#000')
    draw.text((976, 225), str(horoscope.mood).title(), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 25), align='left', fill='#000')
    draw.text((793, 312), str(horoscope.lucky_time).upper(), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 25), align='left', fill='#000')
    draw.text((976, 312), str(horoscope.color).title(), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 25), align='left', fill='#000')
    draw.text((1166, 316), str(horoscope.compatibility).title(), font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 20), align='left', fill='#000')

    font = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 14)
    offset = 276
    for line in textwrap.wrap(horoscope.description,width=40):
        draw.text((409, offset), str(line), font=font, align='left', fill="#808080")
        offset+=font.getbbox(line)[3]

    current_zodiac_sign = Image.open(BytesIO(requests.get(zodiac_icons['{}'.format(horoscope.sign)]).content)).resize((140,140))
    companion_zodiac_sign = Image.open(BytesIO(requests.get(zodiac_icons['{}'.format(str(horoscope.compatibility).lower())]).content)).resize((85,85))

    im.paste(current_zodiac_sign, (179,257), current_zodiac_sign)
    im.paste(companion_zodiac_sign, (1160, 228), companion_zodiac_sign)

    im.save('./media/todays_horoscope.png')

def create_instagram_cover(username):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, str(username))

    PROFILE_PIC = profile.get_profile_pic_url()
    LATEST_THREE_POSTS = []
    i=-1
    for post in profile.get_posts():
        i+=1
        if i==3:
            break
        LATEST_THREE_POSTS.append(Image.open(BytesIO(requests.get(vars(post)['_node']['thumbnail_src']).content)).resize((194,194)))

    FOLLOWER_COUNT = profile.followers
    POSTS_COUNT = profile.get_posts().count

    base_im = Image.open(BytesIO(requests.get("https://i.imgur.com/MLj0xJC.png").content))
    circular_mask = Image.open(BytesIO(requests.get("https://i.imgur.com/h2VXCjL.png").content)).resize((135,135)).convert('L')
    profile_im = Image.open(BytesIO(requests.get(PROFILE_PIC).content)).resize((135,135))
    circular_profile = ImageOps.fit(profile_im, circular_mask.size, centering=(0.5, 0.5))
    circular_profile.putalpha(circular_mask)

    base_im.paste(circular_profile, (186, 262), circular_profile)
    draw = ImageDraw.Draw(base_im, "RGBA")

    draw.text((238, 206), str(profile.username).lower(), font=ImageFont.truetype('./fonts/Poppins-SemiBold.ttf', 26), align='left', fill='#000')
    draw.text((367, 297), str(millify(FOLLOWER_COUNT)).title(), font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26), align='left', fill='#000')
    draw.text((503, 297), str(POSTS_COUNT).title(), font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26), align='left', fill='#000')

    base_im.paste(LATEST_THREE_POSTS[0], (708,203))
    base_im.paste(LATEST_THREE_POSTS[1], (917,203))
    base_im.paste(LATEST_THREE_POSTS[2], (1126,203))

    base_im.save('./media/instagram_profile.png')

def create_crypto_fng_image():
    im_original = Image.open(BytesIO(requests.get("https://alternative.me/crypto/fear-and-greed-index.png").content))
    im_radar = im_original.crop((0, 120, im_original.size[0], im_original.size[1]-70))

    im_radar = im_radar.resize((306, 184))

    im_bg = Image.open(BytesIO(requests.get("https://i.imgur.com/nqBYNAC.png").content))
    im_bg.paste(im_radar, (597, 238))
    im_bg.save('./media/crypto_fng_image.png')

def create_reddit_hot_post(subreddit):
    reddit = praw.Reddit(
        client_id='d1jRR7y_cOSQR0aqWCTmNg',
        client_secret='zHrJxT-21Hu0qjVDZ7aJVvrFdmVNhQ',
        user_agent='web:d1jRR7y_cOSQR0aqWCTmNg:v0.0.1 (by /u/typical__human)',
    )

    try:
        for submission in reddit.subreddit(str(subreddit)).hot(limit=10):
            if vars(submission)['stickied'] == False:

                SBR_NAME = vars(submission)['subreddit_name_prefixed']
                MEM_COUNT = millify(vars(submission)['subreddit_subscribers'])
                COMMENTTS_COUNT = millify(vars(submission)['num_comments'])
                TITLE = vars(submission)['title']
                UPS = vars(submission)['ups']
                THUMBNAIL = vars(submission)['thumbnail']
                break

        im_base = Image.open(BytesIO(requests.get("https://i.imgur.com/6oUO7KE.png").content))
        draw = ImageDraw.Draw(im_base, 'RGBA')
        draw.text((264, 215), SBR_NAME, font=ImageFont.truetype('./fonts/Poppins-SemiBold.ttf', 26), align='left', fill='#000')
        draw.text((206, 281), MEM_COUNT, font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26), align='left', fill='#999')

        if THUMBNAIL =='' or THUMBNAIL=='self':
            offset = 269
            i = 0
            for line in textwrap.wrap(TITLE,width=70):
                if i==1:
                    list1 = list(line)
                    list1[-1] = "."
                    list1[-2] = "."
                    list1[-3] = "."
                    line = ''.join(list1)
                draw.text((411, offset), str(line), font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26), align='left', fill="#000")
                offset+=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26).getbbox(line)[3]
                i+=1
                if i==2:
                    break
        else:
            offset = 269
            i = 0
            for line in textwrap.wrap(TITLE,width=50):
                if i==1:
                    list1 = list(line)
                    list1[-1] = "."
                    list1[-2] = "."
                    list1[-3] = "."
                    line = ''.join(list1)
                draw.text((411, offset), str(line), font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26), align='left', fill="#000")
                offset+=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 26).getbbox(line)[3]
                i+=1
                if i==2:
                    break
            im_base.paste(Image.open(BytesIO(requests.get(THUMBNAIL).content)), (1165, 269))
        
        im_base.paste(Image.open(BytesIO(requests.get("https://i.imgur.com/L39Dj8L.png").content)).resize((25,25)), (413, offset+22), Image.open(BytesIO(requests.get("https://i.imgur.com/L39Dj8L.png").content)).resize((25,25)))
        draw.text((444, offset+20), str(UPS), font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 21), align='left', fill='#FF4400')
        im_base.paste(Image.open(BytesIO(requests.get("https://i.imgur.com/jtDLkT3.png").content)).resize((25,25)), (559, offset+22), Image.open(BytesIO(requests.get("https://i.imgur.com/jtDLkT3.png").content)).resize((25,25)))
        draw.text((589, offset+20), COMMENTTS_COUNT, font=ImageFont.truetype('./fonts/Poppins-Bold.ttf', 21), align='left', fill='#808080')

        im_base.save('./media/reddit_hot_post.png')


    except prawcore.exceptions.Redirect:
        print("Subreddit not found :( Please try again!")

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def create_monthly_life_progress_dark(year_of_birth, life_expectancy):

    BASE_IMAGES_SET = [
        'https://i.imgur.com/aMBSmPe.png',
        'https://i.imgur.com/b2UTLZo.png',
        'https://i.imgur.com/be1FRF4.png',
        'https://i.imgur.com/jAk0PGo.png'
    ]

    base_im = Image.open(BytesIO(requests.get(random.choice(BASE_IMAGES_SET)).content))
    draw = ImageDraw.Draw(base_im, "RGBA")

    TOTAL_SQUARES = (add_years((date(year_of_birth, 1, 1)), life_expectancy).year - date(year_of_birth,1,1).year)*12 + add_years((date(year_of_birth, 1, 1)), life_expectancy).month - date(year_of_birth, 1, 1).month
    COMPlETED_SQUARES = (date.today().year - date(year_of_birth, 1, 1).year) * 12 + date.today().month - date(year_of_birth, 1, 1).month

    title = "Months I've lived"
    subtitle = " I've lived {} months ({}%) of my {} years of life".format(COMPlETED_SQUARES, int((COMPlETED_SQUARES/TOTAL_SQUARES)*100), life_expectancy)
    draw.text(((1500 - int(draw.textlength(title, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 20)))) / 2, 200), title, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 20), align='center')
    draw.text(((1500 - int(draw.textlength(subtitle, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18)))) / 2, 238), subtitle, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18), align='center')
    draw.text((174, 281), "*Each square represents 1 month", font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 10), align='left', fill='white')

    FULL_ROWS, SQUARES_IN_LAST_ROW = TOTAL_SQUARES//164, TOTAL_SQUARES-(TOTAL_SQUARES//164)*164
    SQUARE_SIZE=4
    PADDING = 3
    x1,y1=174,300
    x2,y2=x1+SQUARE_SIZE, y1+SQUARE_SIZE
    COUNTER =0
    CURRENT_ROW =1
    for j in range (FULL_ROWS+1):
        if CURRENT_ROW <=FULL_ROWS:
            for i in range(164):
                if COUNTER < COMPlETED_SQUARES: #this will be the number of square to be highlighted
                    draw.rectangle(((x1, y1), (x2, y2)), fill=(255, 255, 255, 255))
                    COUNTER+=1
                else:
                    draw.rectangle(((x1, y1), (x2, y2)), fill="#4f4f4f")
                    COUNTER+=1
                x1 = x1+SQUARE_SIZE+PADDING
                x2 = x2+SQUARE_SIZE+PADDING
        if CURRENT_ROW > FULL_ROWS:
            for i in range(SQUARES_IN_LAST_ROW):
                if COUNTER < COMPlETED_SQUARES: #this will be the number of square to be highlighted
                    draw.rectangle(((x1, y1), (x2, y2)), fill=(255, 255, 255, 255))
                    COUNTER+=1
                else:
                    draw.rectangle(((x1, y1), (x2, y2)), fill="#4f4f4f")
                    COUNTER+=1
                x1 = x1+SQUARE_SIZE+PADDING
                x2 = x2+SQUARE_SIZE+PADDING
        x1=174
        x2=x1+SQUARE_SIZE
        y1 = y1+SQUARE_SIZE+PADDING
        y2 = y2+SQUARE_SIZE+PADDING
        CURRENT_ROW+=1
    base_im.save('./media/life_progress_dark.png')

def create_monthly_life_progress_light(year_of_birth, life_expectancy):

    BASE_IMAGES_SET = [
        'https://i.imgur.com/koneDzy.png',
        'https://i.imgur.com/nRzNeDi.png',
        'https://i.imgur.com/F5EnZQZ.png',
        'https://i.imgur.com/Jp1tZVP.png',
        'https://i.imgur.com/GLHWCmL.png',
        'https://i.imgur.com/DcFGChj.png',
        'https://i.imgur.com/UHT6BSj.png',
        'https://i.imgur.com/CmGXbtx.png'
    ]

    base_im = Image.open(BytesIO(requests.get(random.choice(BASE_IMAGES_SET)).content))
    draw = ImageDraw.Draw(base_im, "RGBA")

    TOTAL_SQUARES = (add_years((date(year_of_birth, 1, 1)), life_expectancy).year - date(year_of_birth,1,1).year)*12 + add_years((date(year_of_birth, 1, 1)), life_expectancy).month - date(year_of_birth, 1, 1).month
    COMPlETED_SQUARES = (date.today().year - date(year_of_birth, 1, 1).year) * 12 + date.today().month - date(year_of_birth, 1, 1).month

    title = "Months I've lived"
    subtitle = " I've lived {} months ({}%) of my {} years of life".format(COMPlETED_SQUARES, int((COMPlETED_SQUARES/TOTAL_SQUARES)*100), life_expectancy)
    draw.text(((1500 - int(draw.textlength(title, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 20)))) / 2, 200), title, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 20), align='center', fill='black')
    draw.text(((1500 - int(draw.textlength(subtitle, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18)))) / 2, 238), subtitle, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18), align='center', fill='black')
    draw.text((174, 261), "*Each square represents 1 month", font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 10), align='left', fill='black')

    FULL_ROWS, SQUARES_IN_LAST_ROW = TOTAL_SQUARES//164, TOTAL_SQUARES-(TOTAL_SQUARES//164)*164
    SQUARE_SIZE=4
    PADDING = 3
    x1,y1=174,280
    x2,y2=x1+SQUARE_SIZE, y1+SQUARE_SIZE
    COUNTER =0
    CURRENT_ROW =1
    for j in range (FULL_ROWS+1):
        if CURRENT_ROW <=FULL_ROWS:
            for i in range(164):
                if COUNTER < COMPlETED_SQUARES: #this will be the number of square to be highlighted
                    draw.rectangle(((x1, y1), (x2, y2)), fill=(0, 0, 0, 255))
                    COUNTER+=1
                else:
                    draw.rectangle(((x1, y1), (x2, y2)), fill=None, width=1, outline='grey')
                    COUNTER+=1
                x1 = x1+SQUARE_SIZE+PADDING
                x2 = x2+SQUARE_SIZE+PADDING
        if CURRENT_ROW > FULL_ROWS:
            for i in range(SQUARES_IN_LAST_ROW):
                if COUNTER < COMPlETED_SQUARES: #this will be the number of square to be highlighted
                    draw.rectangle(((x1, y1), (x2, y2)), fill=(0, 0, 0, 255))
                    COUNTER+=1
                else:
                    draw.rectangle(((x1, y1), (x2, y2)), fill=None, width=1, outline='grey')
                    COUNTER+=1
                x1 = x1+SQUARE_SIZE+PADDING
                x2 = x2+SQUARE_SIZE+PADDING
        x1=174
        x2=x1+SQUARE_SIZE
        y1 = y1+SQUARE_SIZE+PADDING
        y2 = y2+SQUARE_SIZE+PADDING
        CURRENT_ROW+=1
    base_im.save('./media/life_progress_light.png')

def create_year_progress_light():
    
    BASE_IMAGES_SET = [
        'https://i.imgur.com/koneDzy.png',
        'https://i.imgur.com/nRzNeDi.png',
        'https://i.imgur.com/F5EnZQZ.png',
        'https://i.imgur.com/Jp1tZVP.png',
        'https://i.imgur.com/GLHWCmL.png',
        'https://i.imgur.com/DcFGChj.png',
        'https://i.imgur.com/UHT6BSj.png',
        'https://i.imgur.com/CmGXbtx.png'
    ]
    BASE_IMAGE_URL = random.choice(BASE_IMAGES_SET)
    day_of_year = requests.get("http://worldtimeapi.org/api/timezone/etc/utc").json()["day_of_year"]
    perc = int(day_of_year*100/365)
    astr = str(perc)+"%"
    astr2 = 'year {} has been completed'.format(date.today().year)

    MAX_W, MAX_H = 1500, 600
    #im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
    im = Image.open(BytesIO(requests.get(BASE_IMAGE_URL).content))
    draw = ImageDraw.Draw(im, "RGBA")
    font = ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 56)
    font2 = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18)

    current_h, pad = 220, 20
    w = draw.textlength(astr, font=font)
    draw.text(((MAX_W - w) / 2, current_h), astr, font=font, align='center', fill='black')
    current_h+=pad+56
    w2= draw.textlength(astr2, font=font2)
    draw.text(((MAX_W - w2) / 2, current_h), astr2, font=font2, align='center', fill='black')

    draw.rectangle((((MAX_W - 500)/2, current_h+23+30), ((MAX_W - 500)/2+500, current_h+23+45)), fill=None, width=1, outline="black")
    draw.rectangle((((MAX_W - 500)/2, current_h+23+30), ((MAX_W - 500)/2+500*(perc/100), current_h+23+45)), fill="black")

    im.save('./media/year_progress_light.png')

def create_year_progress_dark():
    
    BASE_IMAGES_SET = [
        'https://i.imgur.com/aMBSmPe.png',
        'https://i.imgur.com/b2UTLZo.png',
        'https://i.imgur.com/be1FRF4.png',
        'https://i.imgur.com/jAk0PGo.png'
    ]
    BASE_IMAGE_URL = random.choice(BASE_IMAGES_SET)
    day_of_year = requests.get("http://worldtimeapi.org/api/timezone/etc/utc").json()["day_of_year"]
    perc = int(day_of_year*100/365)
    astr = str(perc)+"%"
    astr2 = 'year {} has been completed'.format(date.today().year)

    MAX_W, MAX_H = 1500, 600
    #im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
    im = Image.open(BytesIO(requests.get(BASE_IMAGE_URL).content))
    draw = ImageDraw.Draw(im, "RGBA")
    font = ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 56)
    font2 = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18)

    current_h, pad = 220, 20
    w = draw.textlength(astr, font=font)
    draw.text(((MAX_W - w) / 2, current_h), astr, font=font, align='center')
    current_h+=pad+56
    w2 = draw.textlength(astr2, font=font2)
    draw.text(((MAX_W - w2) / 2, current_h), astr2, font=font2, align='center')

    draw.rectangle((((MAX_W - 500)/2, current_h+23+30), ((MAX_W - 500)/2+500, current_h+23+45)), fill=None, width=1, outline="white")
    draw.rectangle((((MAX_W - 500)/2, current_h+23+30), ((MAX_W - 500)/2+500*(perc/100), current_h+23+45)), fill="white")

    im.save('./media/year_progress_dark.png')


def create_todays_moon_phase_image():
    soup = BeautifulSoup(requests.get('https://www.moongiant.com/phase/today/').content, 'lxml')
    todays_image_url = "https://www.moongiant.com"+str(soup.find("div", {"id": "todayMoonContainer"}).findChild("img").attrs["src"])
    tomorrow_image_url = "https://www.moongiant.com"+str(soup.find("div", {"id": "plus1_"}).findChild("img", {"class": "moonNotToday"}).attrs["src"])
    yesterday_image_url = "https://www.moongiant.com"+str(soup.find("div", {"id": "minus1_"}).findChild("img", {"class": "moonNotToday"}).attrs["src"])

    # today's details
    todays_date = soup.find("td", {"id": "today_"}).findChild("b").contents[0]
    todays_moon_name = soup.find("td", {"id": "today_"}).contents[4]

    # yesterday
    yesterdays_date = soup.find("div", {"id": "minus1_"}).findChild("b").contents[0]
    yesterdays_moon_name = soup.find("div", {"id": "minus1_"}).contents[8]

    # tomorrow
    tomorrows_date = soup.find("div", {"id": "plus1_"}).findChild("b").contents[0]
    tomorrow_moon_name = soup.find("div", {"id": "plus1_"}).contents[8]

    

    base_im_dark = Image.open(BytesIO(requests.get("https://i.imgur.com/b5GON6P.png").content))
    mask = Image.open(BytesIO(requests.get("https://i.imgur.com/tF0Lhra.png").content)).convert('L')
    today_moon = Image.open(BytesIO(requests.get(todays_image_url).content))

    final_todays_moon = ImageOps.fit(today_moon, mask.size, centering=(0.5, 0.5))
    final_todays_moon.putalpha(mask)
    final_todays_moon = final_todays_moon.resize((134,134))

    yesterday_moon = Image.open(BytesIO(requests.get(yesterday_image_url).content)).resize((100,100))
    tomorrow_moon = Image.open(BytesIO(requests.get(tomorrow_image_url).content)).resize((100,100))

    base_im_dark.paste(yesterday_moon, (436,250), yesterday_moon)
    base_im_dark.paste(final_todays_moon, (683,216), final_todays_moon)
    base_im_dark.paste(tomorrow_moon, (962,250), tomorrow_moon)


    draw = ImageDraw.Draw(base_im_dark, "RGBA")
    # Writing yesterday moon name
    draw.text((((100 - int(draw.textlength(yesterdays_moon_name, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 14)))) / 2)+436, 361), yesterdays_moon_name, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 14), align='center')
    # Writing yesterday date
    draw.text((((100 - int(draw.textlength(yesterdays_date, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 17)))) / 2)+436, 221), yesterdays_date, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 17), align='center')

    # Writing today's moon name
    draw.text((((134 - int(draw.textlength(todays_moon_name, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 20)))) / 2)+683, 381), todays_moon_name, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 20), align='center')
    # Writing today's date
    draw.text((((134 - int(draw.textlength(todays_date, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 17)))) / 2)+683, 356), todays_date, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 17), align='center')

    # Writing tomorrow's moon name
    draw.text((((100 - int(draw.textlength(tomorrow_moon_name, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 14)))) / 2)+962, 361), tomorrow_moon_name, font=ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 14), align='center')
    # Writing tomorrow date
    draw.text((((100 - int(draw.textlength(tomorrows_date, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 17)))) / 2)+962, 221), tomorrows_date, font=ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 17), align='center')

    base_im_dark.save('./media/todays_moon_phase.png')


def anime_quotes():
    res = requests.get("https://animechan.vercel.app/api/random").json()
    ANIME = res['anime']
    CHARACTER = res['character']
    QUOTE = res['quote']
    
    BASE_IMAGES_LIGHT = [
            "https://i.imgur.com/Nws5nk7.png",
            "https://i.imgur.com/zlLGkqU.png",
            "https://i.imgur.com/L0u5DwJ.png",
            "https://i.imgur.com/ALDqevI.png",
            "https://i.imgur.com/PmvYsXk.png"
        ]

    im = Image.open(BytesIO(requests.get(random.choice(BASE_IMAGES_LIGHT)).content))
    draw = ImageDraw.Draw(im, "RGBA")

    font1 = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 23)
    font2 = ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 18)
    font3 = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 16)
    offset = 234

    for line in textwrap.wrap(QUOTE,width=100):
        draw.text(((1500-font1.getbbox(line)[2])/2, offset), str(line), font=font1, align='center', fill="#fff")
        offset+=font1.getbbox(line)[3]
    
    offset+=20
    draw.text(((1500-font2.getbbox("-"+CHARACTER)[2])/2, offset), str("-"+CHARACTER), font=font2, align='center', fill="#fff")
    offset+=font2.getbbox(CHARACTER)[3]+10

    draw.text(((1500-font3.getbbox(ANIME)[2])/2, offset), str(ANIME), font=font3, align='center', fill="#fff")

    im.save('./media/anime_quote.png')


def random_book_generator(theme=None):
    
    while True:
        try:
            res = requests.get("https://openlibrary.org/random")
            url = URL(res.url)
            OLID = url.parts[2]
            res3 = requests.get("http://openlibrary.org/books/{}.json".format(OLID)).json()

            TITLE = res3['title']
            AUTHOR = requests.get("https://openlibrary.org/{}.json".format(res3['authors'][0]['key'])).json()['name']
            COVER = "https://covers.openlibrary.org/b/id/{}-L.jpg".format(res3['covers'][0])
            print(TITLE)
            print(AUTHOR)
            print(COVER)
            break
        except KeyError:
            pass
    # pprint(res3)


    font1 = ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 35)
    font2 = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 18)
    if theme == 'light':
        im_light = Image.open(BytesIO(requests.get("https://i.imgur.com/XY5f8zq.png").content))
        draw_light = ImageDraw.Draw(im_light, "RGBA")
        offset = 207
        for line in textwrap.wrap(TITLE,width=30):
            draw_light.text((651, offset), str(line), font=font1, align='center', fill="#000")
            offset+=font1.getbbox(line)[3]
        offset += 10
        draw_light.text((656, offset), str(AUTHOR), font=font2, align='center', fill="#000")
        cover_image = Image.open(BytesIO(requests.get(COVER).content)).resize((135, 187))
        im_light.paste(cover_image, (473, 207))

        im_light.save('./media/light_book.png')


    if theme == 'dark':
        im_dark = Image.open(BytesIO(requests.get("https://i.imgur.com/NQvXKXF.png").content))
        draw_dark = ImageDraw.Draw(im_dark, "RGBA")
        offset = 207
        for line in textwrap.wrap(TITLE,width=30):
            draw_dark.text((651, offset), str(line), font=font1, align='center', fill="#fff")
            offset+=font1.getbbox(line)[3]
        offset += 10
        draw_dark.text((656, offset), str(AUTHOR), font=font2, align='center', fill="#fff")
        cover_image = Image.open(BytesIO(requests.get(COVER).content)).resize((135, 187))
        im_dark.paste(cover_image, (473, 207))

        im_dark.save('./media/dark_book.png')




def wallstreet_bets(theme=None):
    res = requests.get('https://tradestie.com/api/v1/apps/reddit').json()
    bull_logo = Image.open(BytesIO(requests.get("https://i.imgur.com/nZUjfBB.png").content)).resize((152,152))
    bear_logo = Image.open(BytesIO(requests.get("https://i.imgur.com/Gcr0rku.png").content)).resize((152,152))

    font1 = ImageFont.truetype('./fonts/LibreBaskerville-Bold.ttf', 29)
    font2 = ImageFont.truetype('./fonts/LibreBaskerville-Regular.ttf', 13)

    if theme == 'light':
        im = Image.open(BytesIO(requests.get("https://i.imgur.com/w6P1ebr.png").content))
        draw = ImageDraw.Draw(im, "RGBA")
        
        #stock 1
        print(res[0]['sentiment'])
        if res[0]['sentiment'] == 'Bullish':
            im.paste(bull_logo, (649, 180), bull_logo)
            draw.text((((152 - int(draw.textlength("$"+res[0]['ticker'], font=font1))) / 2)+649, 340), "$"+str(res[0]['ticker']), font=font1, align='center', fill="#1BB15A")
        if res[0]['sentiment'] == 'Bearish':
            im.paste(bear_logo, (649, 180), bear_logo)
            draw.text((((152 - int(draw.textlength("$"+res[0]['ticker'], font=font1))) / 2)+649, 340), "$"+str(res[0]['ticker']), font=font1, align='center', fill="#CF343A")
        
        draw.text((((152 - int(draw.textlength(str(res[0]['no_of_comments'])+" comments say "+res[0]['sentiment'], font=font2))) / 2)+649, 376), str(res[0]['no_of_comments'])+" comments say "+res[0]['sentiment'], font=font2, align='center', fill="#595959")

        #stock 2
        print(res[1]['sentiment'])
        if res[1]['sentiment'] == 'Bullish':
            im.paste(bull_logo, (894, 180), bull_logo)
            draw.text((((152 - int(draw.textlength("$"+res[1]['ticker'], font=font1))) / 2)+894, 340), "$"+str(res[1]['ticker']), font=font1, align='center', fill="#1BB15A")
        if res[1]['sentiment'] == 'Bearish':
            im.paste(bear_logo, (894, 180), bear_logo)
            draw.text((((152 - int(draw.textlength("$"+res[1]['ticker'], font=font1))) / 2)+894, 340), "$"+str(res[1]['ticker']), font=font1, align='center', fill="#CF343A")
        
        draw.text((((152 - int(draw.textlength(str(res[1]['no_of_comments'])+" comments say "+res[1]['sentiment'], font=font2))) / 2)+894, 376), str(res[1]['no_of_comments'])+" comments say "+res[1]['sentiment'], font=font2, align='center', fill="#595959")


        #stock 3
        print(res[2]['sentiment'])
        if res[2]['sentiment'] == 'Bullish':
            im.paste(bull_logo, (1129, 180), bull_logo)
            draw.text((((152 - int(draw.textlength("$"+res[2]['ticker'], font=font1))) / 2)+1129, 340), "$"+str(res[2]['ticker']), font=font1, align='center', fill="#1BB15A")
        if res[2]['sentiment'] == 'Bearish':
            im.paste(bear_logo, (1129, 180), bear_logo)
            draw.text((((152 - int(draw.textlength("$"+res[2]['ticker'], font=font1))) / 2)+1129, 340), "$"+str(res[2]['ticker']), font=font1, align='center', fill="#CF343A")
        
        draw.text((((152 - int(draw.textlength(str(res[2]['no_of_comments'])+" comments say "+res[2]['sentiment'], font=font2))) / 2)+1129, 376), str(res[2]['no_of_comments'])+" comments say "+res[2]['sentiment'], font=font2, align='center', fill="#595959")
        
        im.save('./media/wsb_light.png')
    
    if theme == 'dark':
        im = Image.open(BytesIO(requests.get("https://i.imgur.com/bLwKXTq.png").content))
        draw = ImageDraw.Draw(im, "RGBA")
        
        #stock 1
        print(res[0]['sentiment'])
        if res[0]['sentiment'] == 'Bullish':
            im.paste(bull_logo, (649, 180), bull_logo)
            draw.text((((152 - int(draw.textlength("$"+res[0]['ticker'], font=font1))) / 2)+649, 340), "$"+str(res[0]['ticker']), font=font1, align='center', fill="#1BB15A")
        if res[0]['sentiment'] == 'Bearish':
            im.paste(bear_logo, (649, 180), bear_logo)
            draw.text((((152 - int(draw.textlength("$"+res[0]['ticker'], font=font1))) / 2)+649, 340), "$"+str(res[0]['ticker']), font=font1, align='center', fill="#CF343A")
        
        draw.text((((152 - int(draw.textlength(str(res[0]['no_of_comments'])+" comments say "+res[0]['sentiment'], font=font2))) / 2)+649, 376), str(res[0]['no_of_comments'])+" comments say "+res[0]['sentiment'], font=font2, align='center', fill="#EFEFEF")

        #stock 2
        print(res[1]['sentiment'])
        if res[1]['sentiment'] == 'Bullish':
            im.paste(bull_logo, (894, 180), bull_logo)
            draw.text((((152 - int(draw.textlength("$"+res[1]['ticker'], font=font1))) / 2)+894, 340), "$"+str(res[1]['ticker']), font=font1, align='center', fill="#1BB15A")
        if res[1]['sentiment'] == 'Bearish':
            im.paste(bear_logo, (894, 180), bear_logo)
            draw.text((((152 - int(draw.textlength("$"+res[1]['ticker'], font=font1))) / 2)+894, 340), "$"+str(res[1]['ticker']), font=font1, align='center', fill="#CF343A")
        
        draw.text((((152 - int(draw.textlength(str(res[1]['no_of_comments'])+" comments say "+res[1]['sentiment'], font=font2))) / 2)+894, 376), str(res[1]['no_of_comments'])+" comments say "+res[1]['sentiment'], font=font2, align='center', fill="#EFEFEF")


        #stock 3
        print(res[2]['sentiment'])
        if res[2]['sentiment'] == 'Bullish':
            im.paste(bull_logo, (1129, 180), bull_logo)
            draw.text((((152 - int(draw.textlength("$"+res[2]['ticker'], font=font1))) / 2)+1129, 340), "$"+str(res[2]['ticker']), font=font1, align='center', fill="#1BB15A")
        if res[2]['sentiment'] == 'Bearish':
            im.paste(bear_logo, (1129, 180), bear_logo)
            draw.text((((152 - int(draw.textlength("$"+res[2]['ticker'], font=font1))) / 2)+1129, 340), "$"+str(res[2]['ticker']), font=font1, align='center', fill="#CF343A")
        
        draw.text((((152 - int(draw.textlength(str(res[2]['no_of_comments'])+" comments say "+res[2]['sentiment'], font=font2))) / 2)+1129, 376), str(res[2]['no_of_comments'])+" comments say "+res[2]['sentiment'], font=font2, align='center', fill="#EFEFEF")
    
        im.save('./media/wsb_dark.png')

    
 