from flask import Flask, redirect, send_file, request
import notion
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    return("Welcome to Dynamic Notion Covers!")


@app.route('/instagram')
def instagram():
    notion.create_instagram_cover(request.args.get('username'))
    filename = 'media/instagram_profile.png'
    return send_file(filename, mimetype='image/png')


@app.route('/dark_stoic_quote')
def dark_stoic_quote():
    notion.download_stoic_quote(random.choice(notion.DARK_STOIC_COVERS))
    filename = 'media/stoic_quote.png'
    return send_file(filename, mimetype='image/png')


@app.route('/light_stoic_quote')
def light_stoic_quote():
    notion.download_stoic_quote(random.choice(notion.LIGHT_STOIC_COVERS))
    filename = 'media/stoic_quote.png'
    return send_file(filename, mimetype='image/png')


@app.route('/weather')
def weather():
    notion.create_weather_image(request.remote_addr)
    filename = 'media/weather_image.png'
    return send_file(filename, mimetype='image/png')

@app.route('/horoscope')
def horoscope():
    notion.create_todays_horoscope(request.args.get('sign'))
    filename = 'media/todays_horoscope.png'
    return send_file(filename, mimetype='image/png')

@app.route('/crypto')
def crypto_fng():
    notion.create_crypto_fng_image()
    filename = 'media/crypto_fng_image.png'
    return send_file(filename, mimetype='image/png')

@app.route('/reddit')
def reddit():
    notion.create_reddit_hot_post(request.args.get('subreddit'))
    filename = 'media/reddit_hot_post.png'
    return send_file(filename, mimetype='image/png')

@app.route('/year_progress_dark')
def year_progress_dark():
    notion.create_year_progress_dark()
    filename = 'media/year_progress_dark.png'
    return send_file(filename, mimetype='image/png')

@app.route('/year_progress_light')
def year_progress_light():
    notion.create_year_progress_light()
    filename = 'media/year_progress_light.png'
    return send_file(filename, mimetype='image/png')

@app.route('/life_progress_dark')
def life_progress_dark():
    notion.create_monthly_life_progress_dark(year_of_birth=int(request.args.get('yob')), life_expectancy=int(request.args.get('life')))
    filename = 'media/life_progress_dark.png'
    return send_file(filename, mimetype='image/png')

@app.route('/life_progress_light')
def life_progress_light():
    notion.create_monthly_life_progress_light(year_of_birth=int(request.args.get('yob')), life_expectancy=int(request.args.get('life')))
    filename = 'media/life_progress_light.png'
    return send_file(filename, mimetype='image/png')


@app.route('/breathing_break')
def breathing_break():
    return redirect("https://imgur.com/seoMoIU.gif", code=302)

@app.route('/moon_phase')
def moon_phase():
    notion.create_todays_moon_phase_image()
    filename = 'media/todays_moon_phase.png'
    return send_file(filename, mimetype='image/png')


@app.route('/anime_quote')
def anime_quote():
    notion.anime_quotes()
    filename = 'media/anime_quote.png'
    return send_file(filename, mimetype='image/png')


@app.route('/dark_book')
def dark_book():
    notion.random_book_generator('dark')
    filename = 'media/dark_book.png'
    return send_file(filename, mimetype='image/png')


@app.route('/light_book')
def light_book():
    notion.random_book_generator('light')
    filename = 'media/light_book.png'
    return send_file(filename, mimetype='image/png')


@app.route('/wsb_dark')
def wsb_dark():
    notion.wallstreet_bets('dark')
    filename = 'media/wsb_dark.png'
    return send_file(filename, mimetype='image/png')


@app.route('/wsb_light')
def wsb_light():
    notion.wallstreet_bets('light')
    filename = 'media/wsb_light.png'
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


# gunicorn --certfile="/etc/letsencrypt/live/dnc1.xyz/fullchain.pem" --keyfile="/etc/letsencrypt/live/dnc1.xyz/privkey.pem" --reload -w 5 --threads 3 --bind 0.0.0.0:443 wsgi:app 