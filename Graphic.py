#Модуль отрисовки графика


import matplotlib.pyplot as plt


#E: вектор суммарных квадратичных ошибок
#k: вектор эпох
#kind: вид ФА: threshold - пороговая, logistics - логистическая
#name: имя для сохранения
def drawGraph(E, k, kind,name = 'E(k)'):
    plt.plot(k[1:], E[1:], marker = 'o')
    plt.xlabel('Era  k')
    plt.ylabel('Error  E')
    plt.axis([0, k[-1]+1, 0, max(E[1:])+1])
    if kind == 'logistics':
        plt.title('logistics')
    elif kind == 'threshold':
        plt.title('threshold')
    plt.grid(True)
    name = name.split("/")
    plt.savefig('{0}/{1}_plt.png'.format(name[0], name[1]))
    plt.clf()
