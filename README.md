# visual-system

## 安装所需依赖

```shell
sudo pip install -r requirements.txt
```

## 运行

先修改settings.ini为mysql数据库的账号密码等，然后运行

```shell
python webserver.py
```

## 向服务器发送数据格式

使用postdata接口以json格式发送,
flows为[src_ip,dst_ip,src_port,dst_port,protocol,size],
heavy_hitter为[src_ip,dst_ip,src_port,dst_port,protocol,size],
heavy_change为[src_ip,dst_ip,src_port,dst_port,protocol,increment],
distribution为[idx,num]，表示大小为idx的流预估有num个（只包含num大于0的）,
inflated_latency为[src_ip,dst_ip,src_port,dst_port,protocol,switch_id]
样例：

``` json

{
    "flows":[[3232235784,3232235783,1,4753,6,4369],
             [3232235784,3232235783,1,1,6,1],
             [3232235784,3232235783,1,5557,6,3246]],
    "heavy_hitter":[[3232235784,3232235783,1,4753,6,4369],
                    [3232235784,3232235783,1,5359,6,3154],
                    [3232235784,3232235783,1,5557,6,3246]],
    "heavy_change":[[3232235784,3232235783,1,4279,6,-3145],
                    [3232235784,3232235783,1,4527,6,-3670],
                    [3232235784,3232235783,1,3241,6,3862]],
    "cardinality":3904,
    "entropy":9.655649,
    "distribution":[[1,0],
                    [2,2.2]],
    "inflated_latency":[[3232235528,3232235783,1,1707,6,0],
                        [3232235528,3232235783,1,1097,6,0],
                        [3232235528,3232235783,1,3382,6,0]]
}

```
