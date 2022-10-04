#Модуль с формулами необходимыми для вычисления параметров НС функциями


from math import tanh


#Функция получения сетевого/комбинированного входа
def net(W, X):
    net = 0
    for (w,x) in zip(W[1:], X[1:]):
        net += w*x
    net += W[0]
    return net


#Функция вычисления y - реального выхода НС.
def actual_NN(net):
    if net > 0:
        return 1
    else:
        return 0


#Функция считает ошибку по текущим значениям целевого и реального выхода
#t: целевой выход (значение БФ на текущем векторе X)
#y: реальный выход
def delta(t, y):
    return t - y


#Функция получения сетевого (недискретизированного) выхода НС
def out(net):
    return (tanh(tanh(net)) + 1 ) / 2


#Функция считает текущее delta w, для корректировки согласно дельта-правилу
def delta_w(nu, delta, net, x, kind):
    if kind == 'logistics':
        return nu * delta * out(net) * (1 - out(net)) * x
    elif kind == 'threshold':
        return nu * delta * x


#Функция корректирует вектор весовых коэффициентов согласно дельта-правилу
#И подсчитывает реальный выход НС
def recount_W(W, X, d, n, nu, kind):
    for (i, w) in enumerate(W):
            W[i] += delta_w(nu, d, n, X[i], kind)
    return W


#Функция считает суммарную квадратичную ошибку
def totalError(Y, F):
    E = 0
    for (y, f) in zip(Y, F):
        if y != f:
            E += 1
    return E
