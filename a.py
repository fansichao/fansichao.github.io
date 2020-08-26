"""

求解方法
1. 暴力统计所有情况
2. 动态规划

"""

n = int(input().strip())
m = int(input().strip())


# 所有路径信息 设置 起点为 0 
distance_info = list()
for i in range(n):
    _ll = str(input().strip()).split(' ')
    distance_info.append([0] + [int(l) for l in _ll])
for i in range(m):
    _ll = str(input().strip()).split(' ')
    distance_info.append([int(l) for l in _ll])

# 快递站-客户
station_node = [info[1] for info in distance_info if info[0] == 0]
# 客户-客户
node_node = [info[1] for info in distance_info if info[0] != 0]
run_path = []

# 0 - 客户信息必然存在
 

# 数据结构转换
dic = dict()
# '0':[{'node':1,'distance':100}]
for info in distance_info:
    if info[0] not in dic.keys():
        dic[info[0]] = []
    dic[info[0]].append({'node':info[1], 'distance':info[2]})
for info in distance_info:
    if info[1] not in dic.keys():
        dic[info[1]] = []
    dic[info[1]].append({'node':info[0], 'distance':info[2]})

max_lens = []
max_len = distance_info[0][2]
for info in dic.values():
    max_lens.append(min([i['distance'] for i in info]))
# TODO
print(sum(max_lens))











    
    
    
 





