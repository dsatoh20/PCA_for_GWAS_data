# 共分散を求める関数
# x = [1,2,3,4,5]
# y = [2,3,4,5,6]

def covar(x,y):
    n = len(x)
    x_bar = sum(x)/n
    y_bar = sum(y)/n
    delta_x = [a - x_bar for a in x]
    delta_y = [b - y_bar for b in y]
    delta_x_y = sum([a * b for (a,b) in zip(delta_x, delta_y)])
    
    return delta_x_y/n

# S = covar(x,y)
# print(S)
    