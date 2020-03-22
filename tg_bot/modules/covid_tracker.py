from telegram import ParseMode, Update, Bot, Chat
from telegram.ext import CommandHandler, MessageHandler, BaseFilter, run_async

from tg_bot import dispatcher

import requests
from parsel import Selector


# TODO: Switch to Parsel instead of Scrapy
def cov(bot: Bot, update: Update):
    country = ''
    confirmed = 0
    deceased = 0
    recovered = 0
    message = update.effective_message
    try:
        selected = message.text.split(' ')[1]
    except:
        selected = 'TOTAL'
    url = 'https://ncov2019.live/'
    text = requests.get(url).text
    selector = Selector(text = text)
    table = selector.css('#sortable_table_Global')
    rows = table.css('tr')
    for row in rows:
        country = row.css('.text--gray::text').getall()[0].strip()
        if country.lower() == selected.lower():
            confirmed = row.css('.text--green::text').getall()[0].strip()
            deceased = row.css('.text--red::text').getall()[0].strip()
            recovered = row.css('.text--blue::text').getall()[0].strip()
            break
        country = selected

    bot.send_message(
        message.chat.id,
        '`COVID-19 Tracker`\n*Number of confirmed cases in %s:* %s\n*Deceased:* %s\n*Recovered:* %s\n\n_Source:_ ncov2019.live' % (country, confirmed, deceased, recovered),
        parse_mode = ParseMode.MARKDOWN,
        disable_web_page_preview = True
    )

__mod_name__ = 'COVID-19 Tracker'

COV_HANDLER = CommandHandler('cov', cov)

dispatcher.add_handler(COV_HANDLER)