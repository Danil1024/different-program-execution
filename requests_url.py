import asyncio
import os
import aiohttp
import requests
from datetime import datetime
import threading
from multiprocessing import Process


urls = {
		'youtube': 'https://www.youtube.com',
		'yandex': 'https://ya.ru/',
		'google': 'https://google.com'
		}

def sync_funck(url, url_name):
    for _ in range(5):
        response = requests.get(url)
        print(response.status_code, url_name, _)
 
def sync_funck_run():
    start = datetime.now()
    for url_name, url in urls.items(): 
        sync_funck(url, url_name)
    return (datetime.now()-start)
 

def threading_funck(url, name_url): 
    print(f'поток {threading.get_ident()} начал работать!')
    for _ in range(5):
        response = requests.get(url)
        print(response.status_code, name_url, _)
    print(f'поток {threading.get_ident()} завершился!')
 
def threading_funck_run():
    start = datetime.now()
    th_list = [threading.Thread(target=threading_funck, args=(url, name_url,)) for name_url, url in urls.items()]
    for th in th_list:
        th.start()
    for th in th_list:
        th.join()
    return (datetime.now()-start)
 

def process_funck(url, url_name): 
    print(f'процесс {os.getpid()} начал работать!')
    for _ in range(5):
        response = requests.get(url)
        print(response.status_code, url_name, _)
    print(f'процесс {os.getpid()} завершился!')
 
def process_funck_run():
    start = datetime.now()
    p_list = [Process(target=process_funck, args=(url, url_name)) for url_name, url in urls.items()]
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    return (datetime.now()-start)
 

async def async_funk(url, name_url):
    async with aiohttp.ClientSession() as session:
        for num in range(5): 
            response = await session.get(url)
            print(response.status, name_url, 'вызов номер ' + str(num))

async def create_list_tasks():
    tasks = []
    for name_url, url in urls.items():
        task = asyncio.create_task(async_funk(url, name_url)) 
        tasks.append(task)
    return tasks

def async_funk_run():
    start = datetime.now()
    main_loop = asyncio.get_event_loop()
    tasks = main_loop.run_until_complete(create_list_tasks())
    main_loop.run_until_complete(asyncio.gather(*tasks))
    return (datetime.now()-start)
    #main_loop.run_forever()

 
if __name__ == '__main__':
    sync_funck_run_time = sync_funck_run()
    threading_funck_run_time = threading_funck_run()
    process_funck_run_time = process_funck_run()
    async_funk_run_time = async_funk_run()
    print('синхронно: ' + str(sync_funck_run_time)) # 10.1 сек
    print('мультипоточно: ' + str(threading_funck_run_time)) # 4.8 сек
    print('мультипроцессорно: ' + str(process_funck_run_time)) # 6.2 сек
    print('асинхронно: ' + str(async_funk_run_time)) # 1.9 сек

