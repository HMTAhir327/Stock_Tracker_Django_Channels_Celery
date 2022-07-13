from asyncio import threads
from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread

# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    return render(request, 'mainapp/stockpicker.html', {'stockpicker': stock_picker})

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    print('stockpicker:',stockpicker)
    data = {}
    check = [x for x in stockpicker if x not in tickers_nifty50()]

    #implimented threading for the commented for loop statement
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()

    # for stock in stockpicker:
    #     if check:
    #         return HttpResponse('Error')
    #     else:
    #         result = get_quote_table(stock)
    #         data[stock] = result 

    for i in range(n_threads):
        if check:
            return HttpResponse('Error')
        else:
            # below commented line was suggested by copilote for else statement
            # thread_list.append(threads.Thread(target=get_quote_table, args=(stockpicker[i],)))
            thread = Thread(target= lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}) , args=(que,stockpicker[i]))  
            thread_list.append(thread)
            thread_list[i].start()

    for thread in thread_list:
        thread.join() 

    while not que.empty():
        data.update(que.get())
    end = time.time()
    taken_time = end - start
    print('taken_time:',taken_time)
    #thread part finish here and time counted for better performance

    print('data:',data)
    return render(request, 'mainapp/stocktracker.html', {'data': data})