
import requests

from bs4 import BeautifulSoup
from datetime import date
from config import keys




class APIException(Exception):
    pass


class GetLesson:

    @staticmethod
    def get_lessons(name: str, command: str):

        try:
            today = date.today()
            day_number = today.weekday() + 1

        except KeyError:
            raise APIException(f"Дата не получена")

        # на сайте дни нумеруются с нуля
        # мы берем уроки на следующий день, поэтому в пятницу нам нужно смотреть уже на понедельник
        try:
            if day_number > 4:
                url_user = f'https://39school11.eljur.ru/journal-app/{name}/week.-1'
                day_number = 0
            elif day_number >= 1 and day_number <= 4:
                url_user = f'https://39school11.eljur.ru/journal-app/{name}'
            else:
                return 0
        except KeyError:
            raise APIException(f"Не корректный параметр: {name}")


        url_login = f"https://39school11.eljur.ru/?user={keys['username']}&domain=39school11"
        url_main = 'https://39school11.eljur.ru/'



        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36',
            'Referer': url_main,
            'Connection': 'keep-alive',
        }


        data = {
            'username': keys['username'],
            'password': keys['password'],
            'return_uri': '/'
        }

        s = requests.Session()
        d = s.post(url_login, data=data, headers=headers).text

        dd = s.get(url_user)

        soup = BeautifulSoup(dd.text, "html.parser")
        # soup = BeautifulSoup(dd.text, "lxml")

        now_day = soup.find("div", class_="dnevnik").find_all("div", class_="dnevnik-day")[day_number]

        lessons = now_day.find("div", class_="dnevnik-day__lessons")

        list_lesson = []

        for lesson in lessons:
            try:
                lesson_name = lesson.find("div", class_="dnevnik-lesson__subject").find("span", class_="js-rt_licey-dnevnik-subject").text.strip()
                lesson_task = lesson.find("div", class_="dnevnik-lesson__hometask").find("div", class_="dnevnik-lesson__task").text.strip()
                list_lesson.append(f'{str(lesson_name).upper()}: {lesson_task}')

            except:
                lesson_name = "No"
                lesson_task = "No"

        return list_lesson


