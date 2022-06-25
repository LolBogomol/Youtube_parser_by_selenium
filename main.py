from os import  system
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import httplib2 
import PySimpleGUI as sg
import apiclient
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.firefox.options import Options
import webbrowser
import re
from fake_useragent import UserAgent
system('CLS')
#77 x 132
# Интерфейс
# Фоновой режим
# Сылка на документ
# ФОТО
need_more_than = 1
class GUI:
    def __init__(self):
        self.layout = [
            [sg.Text('Сылка на видео'), sg.InputText(),],
            [sg.Text('Минимально количество просмотров'), sg.InputText(),sg.Submit(),]]
    def run_gui(self):
        window = sg.Window('Ютуб парсер', self.layout)
        while True:  
            event,values = window.read()
            global url1
            url1 = values.get(0)
            print(url1)
            global need_more_than
            need_more_than = values.get(1) + '000'
            print(need_more_than)
            if need_more_than != None and url1 != None:
                window.close()
                break
class get_source:
    def __init__(self):
        self.useragent = UserAgent()
        self.path = os.path.abspath('chromedriver.exe')
        print(self.path)
    def get_source_html(self):
        #options = webdriver.ChromeOptions()
        #options.add_argument("headless")
        #options.add_argument(f'user-agent={self.useragent.random}')
        #options.add_argument("--proxy-server=46.44.56.223:8081")
        driver = webdriver.Chrome(executable_path = self.path)#chrome_options=options)
        #driver.delete_all_cookies()
        print("открываем url")
        driver.get(url=url1)
        with open("source-page.html","w",encoding='utf-8') as file:
            file.write(driver.page_source)
        time.sleep(5)
        print('Начинаем скролить страницу!')
        try:
            time.sleep(3)
            b = 0
            h_prev = 0
            i = 0
            while True:
                time.sleep(1)
                os.system('CLS')
                i += 1 
                print('страницы скролиться',i)
                with open("source-page.html","w",encoding='utf-8') as file:
                    h = driver.execute_script('return window.innerHeight + window.scrollY;')
                    driver.execute_script(f'window.scrollTo(0,{h});')
                    if h == h_prev:
                        print('условие активировано')
                        print('проверка на конец страницы {} из 10'.format(b))
                        b += 1
                        if b == 10 and h_prev == h:
                            file.write(driver.page_source)
                            break
                    time.sleep(0.5)
                    h_prev = h
        except Exception as ex:
            print(ex)
        
        finally:
           print('скролинг закончен.')
           driver.close()
           driver.quit()

data_dict = {}
video_url = []
titles = []
views = []
lenght_of_video = []
url_for_img = []
publication_date = []
chanell_name = str()
images = []

class parser:
    def __init__(self):
        self.file_path = os.path.abspath('source-page.html')
    def get_items(self):
        try:
            with open(self.file_path,encoding='utf-8') as file:
                src = file.read()
            print('укажите чилсо от 1 - 999. т.к как еденица интерпритируеться как тысяча')
            soup =  BeautifulSoup(src,"lxml")
            chanell_name1 = soup.find('div',id="text-container").find('yt-formatted-string').get_text()
            global subb
            subb = soup.find('yt-formatted-string',id = 'subscriber-count').get_text()
            global chanell_name
            chanell_name = chanell_name1
            items = soup.find_all('div',id = 'dismissible')
            i = 0
            for item in items:
                i += 1
                print('Итерация номер {} из {}!'.format(i,len(items)))
                date = item.find('div',id = 'metadata-line').find('span').find_next('span').get_text()
                url_video = item.find('ytd-thumbnail').find('a',id = 'thumbnail').get('href')
                view = item.find('div', id = 'metadata-line').find('span',class_='style-scope ytd-grid-video-renderer').get_text()
                item_title = item.find('a',id = 'video-title').get_text()
                lenght = item.find('ytd-thumbnail-overlay-time-status-renderer').find('span',id = 'text').get_text()
                img_url = item.find('yt-img-shadow').find('img',id = 'img').get("src")
                try:
                    print('i am line 124')
                    if view.split()[1] == 'тыс.' and int(view.split()[0] + '000') < int(need_more_than):
                        print('мало просмотров! итерациия прервана')
                        continue
                except ValueError:
                    A  = view.split()[0].replace(',','.')
                    print('i am line 129')
                    if view.split()[1] == 'тыс.' and float(A + '00') < int(need_more_than):
                        print('мало просмотров! итерациия прервана')
                        continue
                video_url.append('youtube.com/'+url_video)
                titles.append(item_title)
                lenght_of_video.append(lenght)
                url_for_img.append(img_url)
                images.append('=IMAGE("{}")'.format(img_url))
                publication_date.append(date)
                try:
                    if  ',' not in view[0] and view.split()[1] == "тыс.":
                        if ',' in view.split()[0]:
                            print(view)
                            real_view = view.split()[0].replace(',','') + '00'
                            views.append(int(real_view))
                            print('result', real_view)
                            continue
                        else:
                            real_view = view.split()[0] +'000'
                            print(view)
                            print(real_view)
                            views.append(int(real_view))
                            continue
                    elif ',' in view[0] and view[1] == "тыс.":
                        print('maga')
                        real_view = view.split()[0].replace(',','') + '00'
                        views.append(int(real_view))
                        print(view)
                        continue
                        print(real_view)
                    elif ',' not in view[0] and view.split()[1] == "млн":
                        if ',' in view.split()[0]:
                            print(view)
                            real_view = view.split()[0].replace(',','') + '00000'
                            views.append(real_view)
                            print('result', real_view)
                            continue
                        real_view = re.sub(",","",view.split()[0]) +'000000'
                        print(real_view)
                        views.append(int(real_view))
                    elif ',' in view[0] and view[1] == "млн":
                        real_view = re.sub(",","",view.split()[0]) + '000000'
                        print(real_view)
                        views.append(int(real_view))
                        print(real_view)
                        continue
                except ValueError:
                    if view.split()[1] == 'млн' and  len(view.split()) == 3:
                        real_view = view.split()[0] = re.sub(",","",view.split()[0]) + '000000'
                        views.append(int(real_view))
                        print(view)
                        print(real_view)
                        continue
                    else:
                        real_view = view.split()[0].replace(',','') + '000'
                        views.append(int(real_view))
                        print(view)
                        print(real_view)
                        continue
        except Exception as ex:
            print(ex)
            while True:
                time.sleep(1)
            '''
            video_url.append('youtube.com/'+url_video)
            titles.append(item_title)
            lenght_of_video.append(lenght)
            url_for_img.append(img_url)
            images.append('=IMAGE("{}")'.format(img_url))
            publication_date.append(date)
            try:
                if  ',' not in view[0] and view.split()[1] == "тыс.":
                    if ',' in view.split()[0]:
                        print(view)
                        real_view = view.split()[0].replace(',','') + '00'
                        views.append(int(real_view))
                        print('result', real_view)
                        continue
                    else:
                        real_view = view.split()[0] +'000'
                        print(view)
                        print(real_view)
                        views.append(int(real_view))
                        continue
                elif ',' in view[0] and view[1] == "тыс.":
                    print('maga')
                    real_view = view.split()[0].replace(',','') + '00'
                    views.append(int(real_view))
                    print(view)
                    continue
                    print(real_view)
                elif ',' not in view[0] and view.split()[1] == "млн":
                    if ',' in view.split()[0]:
                        print(view)
                        real_view = view.split()[0].replace(',','') + '00000'
                        views.append(real_view)
                        print('result', real_view)
                        continue
                    real_view = re.sub(",","",view.split()[0]) +'000000'
                    print(real_view)
                    views.append(int(real_view))
                elif ',' in view[0] and view[1] == "млн":
                    real_view = re.sub(",","",view.split()[0]) + '000000'
                    print(real_view)
                    views.append(int(real_view))
                    print(real_view)
                    continue
            except ValueError:
                if view.split()[1] == 'млн' and  len(view.split()) == 3:
                    real_view = view.split()[0] = re.sub(",","",view.split()[0]) + '000000'
                    views.append(int(real_view))
                    print(view)
                    print(real_view)
                    continue
                else:
                    real_view = view.split()[0].replace(',','') + '000'
                    views.append(int(real_view))
                    print(view)
                    print(real_view)
                    continue
            '''
        print("Парсинг закончен")


class google_shit:
    def __init__(self) -> None:
        try:
            self.path = os.path.abspath('chromedriver.exe')
            print("Начинаем запись в таблицу! Инициализация классов.")
            self.list_name = "Данные с канала {}-{}".format(chanell_name,subb)
            '''Время копипасты!'''
            self.CREDENTIALS_FILE = 'pyproject-351410-2a36ee4c2c17.json'  # Имя файла с закрытым ключом, вы должны подставить свое
            # Читаем ключи из файла
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE,  ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
            self.httpAuth = self.credentials.authorize(httplib2.Http()) # Авторизуемся в системе
            try:
                self.service = apiclient.discovery.build('sheets', 'v4', http = self.httpAuth) # Выбираем работу с таблицами и 4 версию API       
            except:
                DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
                self.service = apiclient.discovery.build('sheets', 'v4', credentials=self.credentials, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
            
            self.spreadsheet = self.service.spreadsheets().create(body = {
                'properties': {'title': self.list_name, 'locale': 'ru_RU'},
                'sheets': [{'properties': {'sheetType': 'GRID',
                                        'sheetId': 0,
                                        'title': self.list_name,
                                        'gridProperties': {'rowCount': 50, 'columnCount': 100}}}]
            }).execute()
            self.spreadsheetId = self.spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
            self.driveService = apiclient.discovery.build('drive', 'v3', http = self.httpAuth)
            self.shareRes = self.driveService.permissions().create(
                fileId = self.spreadsheet['spreadsheetId'],
                body = {'type': 'anyone', 'role':'writer',},  # доступ на чтение кому угодно
                fields = 'id'
            ).execute()
            self.shit = self.service.spreadsheets()
        except Exception as ex:
            print(ex)
            while True:
                time.sleep(1)

    def set_width(self):        
        try:
            response = self.service.spreadsheets().batchUpdate(  
                spreadsheetId = self.spreadsheetId,
                body = {
                "requests": [
                    {
                    "updateDimensionProperties": {
                        "range": {
                        "sheetId": 0,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": 1
                        },
                        "properties": {
                        "pixelSize": 200
                        },
                        "fields": "pixelSize"
                    }}]}
                    ).execute()
            response = self.service.spreadsheets().batchUpdate(  
                    spreadsheetId = self.spreadsheetId,
                    body = {
                        "requests": [
                            {
                            "updateDimensionProperties": {
                                "range": {
                                "sheetId": 0,
                                "dimension": "ROWS",
                                "startIndex":0
                                },
                                "properties": {
                                "pixelSize": 77
                                },
                                "fields": "pixelSize"
                            }}]}
                            ).execute()
            response = self.service.spreadsheets().batchUpdate(  
                    spreadsheetId = self.spreadsheetId,
                    body = {
                        "requests": [
                            {
                            "updateDimensionProperties": {
                                "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 3,
                                "endIndex": 4,
                                },
                                "properties": {
                                "pixelSize": 500
                                },
                                "fields": "pixelSize"
                            }}]}
                            ).execute()
            response = self.service.spreadsheets().batchUpdate(  
                    spreadsheetId = self.spreadsheetId,
                    body = {
                        "requests": [
                            {
                            "updateDimensionProperties": {
                                "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 1,
                                "endIndex": 2,
                                },
                                "properties": {
                                "pixelSize": 400
                                },
                                "fields": "pixelSize"
                            }}]}
                            ).execute()
        except Exception as ex:
            print(ex)
            while True:
                time.sleep(1)
                
    def write_update(self):
        try:
            body = {
                'valueInputOption': 'USER_ENTERED',
                'data': [{
                    "majorDimension": "COLUMNS",
                    'range': "Данные с канала {}-{}!A1".format(chanell_name,subb),
                    'values':[video_url,url_for_img,images,titles,views,publication_date,lenght_of_video]
                    }]}
            resp = self.shit.values().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()
            # Оба способа записи в таблицу работают, ту тдолжно быть подвох поэтому сохраню другой в коментариях
            '''
            resp = self.shit.values().update(
                    spreadsheetId = self.spreadsheetId,
                    range = "Данные с канала {}-{}!A1".format(chanell_name,subb),
                    valueInputOption="RAW",
                    body={"values":[titles,views,publication_date,lenght_of_video,video_url,url_for_img], "majorDimension": "COLUMNS"}).execute()
            '''
            print('Запись в таблицу окончена, вот ваша сылка')
            webbrowser.open('https://docs.google.com/spreadsheets/d/' + self.spreadsheetId,new = 2)
            #'https://docs.google.com/spreadsheets/d/' + self.spreadsheetId
            print('https://docs.google.com/spreadsheets/d/' + self.spreadsheetId)
            A = input('Нажмите любую кнопку')
            S = input('Нажмите любую кнопку')
        except Exception as ex:
            print(ex)
            while True:
                time.sleep(1)

def main():
    try:
        gui = GUI()
        gui.run_gui()
        get_source1 = get_source()
        time.sleep(3)
        get_source1.get_source_html()
        get_item1 = parser()
        get_item1.get_items()
        shit = google_shit() #i hate this shit
        shit.set_width()
        shit.write_update()
    except Exception as ex:
            print(ex)
            while True:
                time.sleep(1)

if __name__ == "__main__":
    main()