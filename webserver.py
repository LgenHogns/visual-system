from flask import Flask, render_template, request, redirect, url_for, Blueprint
import json
import numpy as np


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


def int_to_ip(x):
    return '.'.join([str(x//(256**i) % 256) for i in range(3, -1, -1)])


def get_data(data_name):
    return data[data_name]


def get_flow_size():
    '''
    获取Flow size estimation页面所需数据
    '''
    result = []
    items = get_data('flow_size')
    for idx, item in enumerate(items):
        t = []
        t.append('<tr>')
        t.append('<td>' + str(idx+1) + '</td>')
        t.append('<td>' + str(item[0]) + '</td>')
        t.append('<td>' + str(item[1]) + '</td>')
        t.append('<td>' + str(item[2]) + '</td>')
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
    result = []
    items = get_data('heavy_hitter')
    for idx, item in enumerate(items):
        t = []
        t.append('<tr>')
        t.append('<td>' + str(idx+1) + '</td>')
        t.append('<td>' + str(item[0]) + '</td>')
        t.append('<td>' + str(item[1]) + '</td>')
        t.append('<td>' + str(item[2]) + '</td>')
        t.append('<td>' + str(item[3]) + '</td>')
        t.append('<td>' + str(item[4]) + '</td>')
        t.append('<td>' + str(item[5]) + '</td>')
        t.append('</tr>')
        result.append("".join(t))
    return result


def get_heavy_change():
    '''
    获取Heavy change detection页面所需数据
    '''
    result = []
    items = get_data('heavy_change')
    for idx, item in enumerate(items):
        t = []
        t.append('<tr>')
        t.append('<td>' + str(idx+1) + '</td>')
        t.append('<td>' + str(item[0]) + '</td>')
        t.append('<td>' + str(item[1]) + '</td>')
        t.append('<td>' + str(item[2]) + '</td>')
        t.append('<td>' + str(item[3]) + '</td>')
        t.append('<td>' + str(item[4]) + '</td>')
        t.append('<td>' + str(item[5]) + '</td>')
        t.append('</tr>')
        result.append("".join(t))
    return result


data = {'flow_size': [[1, 1, 1, 1, 1, 1]],
        'heavy_hitter': [[1, 1, 1, 1, 1, 1]],
        'heavy_change': [[1, 1, 1, 1, 1, 1]]}
app = Flask(__name__)


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


@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    '''
    新打开一个网页时，需要通过这个接口获取数据
    '''
    pageid = int(request.args.get('pageid'))
    dataid = request.args.get('dataid')
    result = []
    if pageid == 0:
        result = get_flow_size()
    elif pageid == 1:
        result = get_heavy_hitter()
    elif pageid == 2:
        result = get_heavy_change()
    print(result)
    return json.dumps(result, cls=CustomEncoder)


@app.route('/postdata', methods=['POST'])
def postdata():
    '''
    后端通过这个接口将数据以json格式发给前端
    '''
    global data

    rawdata = request.get_data(as_text=True)

    try:
        data = json.loads(rawdata)
    except:
        traceback.print_exc()
        return 'json syntax error'

    return 'data got'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
