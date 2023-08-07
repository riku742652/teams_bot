import datetime
import logging
import pymsteams
import jpholiday
from config import TEAMS_WEB_HOOK_URL, \
                   DELIVERY_SHOP, \
                   MESSAGE

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
file_handler = logging.FileHandler('teams_bot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def search_business_day():
    '''
        翌日以降の最短営業日(YYYY/MM/DD)を返却する
        特定日数以内に見つからなかった場合はNoneを返却
    '''
    today_date = datetime.date.today()
    target_date = ''
    for i in range(1, 10):
        target_date = today_date + datetime.timedelta(days=i)
        # 土日でも祝日でもない
        if target_date.isoweekday() not in [6, 7] and \
            not jpholiday.is_holiday(target_date):
            break
    else:
        logger.error('business day not found')
        return
    return target_date.strftime('%Y/%m/%d')

def post_teams_message(message):
    '''
        Teamsに投稿する
    '''

    teams = pymsteams.connectorcard(TEAMS_WEB_HOOK_URL)
    teams.title("【{prefix}】 {title}".format(prefix=DELIVERY_SHOP,
                                             title=message))
    teams.text(MESSAGE)
    teams.send()

if __name__ == '__main__':
    logger.info("---START---")
    target_date = search_business_day()
    logger.info("target_date: {}".format(target_date))
    post_teams_message(target_date)
    logger.info("---END---")
