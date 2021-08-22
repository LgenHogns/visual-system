from flask import Flask, render_template, request, redirect, url_for, Blueprint
import json
import numpy as np
from data import DBData
import threading
import random


class RWlock(object):
    def __init__(self):
        self._lock = threading.Lock()
        self._extra = threading.Lock()
        self.read_num = 0

    def read_acquire(self):
        with self._extra:
            self.read_num += 1
            if self.read_num == 1:
                self._lock.acquire()

    def read_release(self):
        with self._extra:
            self.read_num -= 1
            if self.read_num == 0:
                self._lock.release()

    def write_acquire(self):
        self._lock.acquire()

    def write_release(self):
        self._lock.release()


def int2ip(x):
    return '.'.join(
        [str(x//(256**i) % 256) for i in range(3, -1, -1)])


def takeSixth(item):
    return item[5]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)


def get_color(x):
    colors = [[0x2e, 0xc7, 0xc9],
              [0xb6, 0xa2, 0xde],
              [0x5a, 0xb1, 0xef],
              [0xff, 0xb9, 0x80],
              [0xd8, 0x7a, 0x80],
              [0x8d, 0x98, 0xb3],
              [0xe5, 0xcf, 0x0d],
              [0x97, 0xb5, 0x52]]
    return '#%02x%02x%02x' % (colors[x % 8][0], colors[x % 8][1], colors[x % 8][2])


def get_flow_size():
    '''
    获取Flow size estimation页面所需数据
    '''
    result = []
    items = json_data['flows']
    random.shuffle(items)
    for idx, item in enumerate(items):
        t = []
        t.append('<tr>')
        t.append('<td>' + int2ip(item[0]) + '</td>')
        t.append('<td>' + str(item[2]) + '</td>')
        t.append('<td>' + int2ip(item[1]) + '</td>')
        t.append('<td>' + str(item[3]) + '</td>')
        t.append('<td>' + str(item[4]) + '</td>')
        t.append('<td>' + str(item[5]) + '</td>')
        t.append('</tr>')
        result.append("".join(t))
    return result


def get_heavy_hitter():
    '''
    获取Heavy hitter detection页面所需数据
    '''
    flow_data = []
    total_data = {}
    items = json_data['heavy_hitter']
    items.sort(key=takeSixth, reverse=True)
    for idx, item in enumerate(items):
        now = {
            'name': '',
            'value': [len(flow_data) + 1, item[5]],
            'ID': idx,
            'itemStyle': {
                'color': get_color(len(flow_data) + 1),
                'borderColor': '#d0d0d0',
                'borderWidth': 2
            }
        }
        flow_data.append(now)
        total_data[item[5]] = total_data.get(item[5], 0) + 1

    total_data1 = []
    for key, value in total_data.items():
        total_data1.append([key, value])

    return {'flow_data': flow_data, 'total_data': list(total_data.items())}


def get_heavy_change():
    '''
    获取Heavy change detection页面所需数据
    '''
    flow_data = []
    total_data = {}
    items = json_data['heavy_change']
    items.sort(key=takeSixth, reverse=True)
    print(items)
    for idx, item in enumerate(items):
        now = {
            'name': '',
            'value': [len(flow_data) + 1, item[5]],
            'ID': idx,
            'itemStyle': {
                'color': get_color(len(flow_data) + 1),
                'borderColor': '#d0d0d0',
                'borderWidth': 2
            }
        }
        flow_data.append(now)
        total_data[item[5]] = total_data.get(item[5], 0) + 1

    total_data1 = []
    for key, value in total_data.items():
        total_data1.append([key, value])

    return {'flow_data': flow_data, 'total_data': list(total_data.items())}


def get_distri_entr():
    '''
    获取流分布和熵
    '''
    tmp = json_data['distribution']
    card = json_data['cardinality']
    num = [0, 0, 0, 0, 0, 0]
    entropy = json_data['entropy']
    for item in tmp:
        print(item)
        if item[1] > 0:
            if item[0] <= 20:
                num[0] += 1
            elif 20 < item[0] <= 50:
                num[1] += 1
            elif 50 < item[0] <= 200:
                num[2] += 1
            elif 200 < item[0] <= 500:
                num[3] += 1
            elif 500 < item[0] <= 2048:
                num[4] += 1
            else:
                num[5] += 1
    return {
        'flow_dis': num,
        'entropy': round(entropy, 2),
        'card': card
    }


def get_latency():
    result = []
    items = json_data['inflated_latency']
    random.shuffle(items)
    for idx, item in enumerate(items):
        t = []
        t.append('<tr>')
        t.append('<td>' + int2ip(item[0]) + '</td>')
        t.append('<td>' + str(item[2]) + '</td>')
        t.append('<td>' + int2ip(item[1]) + '</td>')
        t.append('<td>' + str(item[3]) + '</td>')
        t.append('<td>' + str(item[4]) + '</td>')
        t.append('<td>' + str(item[5]) + '</td>')
        t.append('</tr>')
        result.append("".join(t))
    return result


app = Flask(__name__)
json_data = {'flows': [],
             'heavy_hitter': [],
             'heavy_change': [],
             'dirtribution': [],
             'cardinality': 0,
             'entropy': 0,
             'inflated_latency': []}


@app.route('/')
def index():
    dataid = 1
    chart = {'dataid': dataid}
    return render_template('show0.html', pageid=0, sidedata=chart)


@app.route('/show/0')
def show0():
    dataid = 1
    chart = {'dataid': dataid}
    return render_template('show0.html', pageid=0, sidedata=chart)


@app.route('/show/1')
def show1():
    dataid = 1
    chart = {'dataid': dataid}
    return render_template('show1.html', pageid=1, sidedata=chart)


@app.route('/show/2')
def show2():
    dataid = 1
    chart = {'dataid': dataid}
    return render_template('show2.html', pageid=2, sidedata=chart)


@app.route('/show/3')
def show3():
    dataid = 1
    chart = {'dataid': dataid}
    return render_template('show3.html', pageid=3, sidedata=chart)


@app.route('/show/4')
def show4():
    dataid = 1
    chart = {'dataid': dataid}
    return render_template('show4.html', pageid=4, sidedata=chart)


@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    '''
    新打开一个网页时，需要通过这个接口获取数据
    '''
    pageid = int(request.args.get('pageid'))
    dataid = request.args.get('dataid')
    result = []
    print('getdata')
    lock.read_acquire()
    if pageid == 0:
        result = get_flow_size()
    elif pageid == 1:
        result = get_heavy_hitter()
    elif pageid == 2:
        result = get_heavy_change()
    elif pageid == 3:
        result = get_distri_entr()
    else:
        result = get_latency()
    lock.read_release()
    print('getdataend')
    return json.dumps(result, cls=CustomEncoder)


@app.route('/postdata', methods=['POST'])
def postdata():
    '''
    以json格式接收数据
    '''
    global json_data

    rawdata = request.get_data(as_text=True)

    lock.write_acquire()
    try:
        json_data = json.loads(rawdata)
    except:
        traceback.print_exc()
        return 'json syntax error'
    lock.write_release()

    lock1.acquire()

    tid = data.get_tid()[0][0]+1

    data.set_tid(tid)

    data.set_size(tid, json_data['flows'])

    data.set_heavy_hitter(tid, json_data['heavy_hitter'])

    data.set_heavy_change(tid, json_data['heavy_change'])

    data.set_distri(tid, json_data['distribution'])

    data.set_switch(tid, json_data['inflated_latency'])

    data.set_cardinality(tid, json_data['cardinality'])

    data.set_entropy(tid, json_data['entropy'])
    lock1.release()

    return 'data got'


if __name__ == '__main__':
    lock = RWlock()
    lock1 = threading.Lock()
    lock1.acquire()
    data = DBData()
    lock1.release()
    app.run(host='0.0.0.0', port=5000, debug=False)
