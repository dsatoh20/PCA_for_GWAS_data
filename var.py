# 標本分散を求める関数
# x = [1,2,3,4,5]

def var(x):
    n = len(x)
    x_bar = sum(x)/n
    delta_x_2 = sum([(a - x_bar)**2 for a in x])
    return float(delta_x_2/n)

# S = var(x)
# print(S)
