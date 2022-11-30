import asyncio
from datetime import datetime
import threading
from multiprocessing import Process
import os


digits = [2, 3, 5]

async def async_funk(digit): 
	result = digit ** 1000000
	print(result)

async def create_list_tasks():
	tasks = []
	for digit in digits:
		task = asyncio.create_task(async_funk(digit)) 
		tasks.append(task)
	return tasks

def async_funk_run():
	start = datetime.now()
	main_loop = asyncio.get_event_loop()
	tasks = main_loop.run_until_complete(create_list_tasks())
	main_loop.run_until_complete(asyncio.gather(*tasks))
	return (datetime.now()-start)


def sync_funck(digit):
    result = digit ** 1000000
    print(result)
 
def sync_funck_run():
    start = datetime.now()
    for digit in digits: 
        sync_funck(digit)
    return (datetime.now()-start)
 

def threading_funck(digit): 
    print(f'поток {threading.get_ident()} начал работать!')
    result = digit ** 1000000
    print(f'{result}\n')
    print(f'поток {threading.get_ident()} завершился!')
 
def threading_funck_run():
    start = datetime.now()
    th_list = [threading.Thread(target=threading_funck, args=(digit,)) for digit in digits]
    for th in th_list:
        th.start()
    for th in th_list:
        th.join()
    return (datetime.now()-start)
 

def process_funck(digit): 
    print(f'процесс {os.getpid()} начал работать!')
    result = digit ** 1000000
    print(f'{result}\n')
    print(f'процесс {os.getpid()} завершился!')
 
def process_funck_run():
    start = datetime.now()
    p_list = [Process(target=process_funck, args=(digit,)) for digit in digits]
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    return (datetime.now()-start)
 
 
if __name__ == '__main__':
    sync_funck_run_time = sync_funck_run()
    threading_funck_run_time = threading_funck_run()
    process_funck_run_time = process_funck_run()
    async_funk_run_time = async_funk_run()
    print('синхронно: ' + str(sync_funck_run_time)) # 25 сек
    print('мультипоточно: ' + str(threading_funck_run_time)) # 25 сек
    print('мультипроцессорно: ' + str(process_funck_run_time)) # 17 сек
    print('асинхронно: ' + str(async_funk_run_time)) # 25 сек

