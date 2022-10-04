#Модуль генерации БФ и поиск их значений


# Функция генерирует числа от 0 до 16 в двоичной сист. исчисления.
# И находит значения истиности с модуляцией (x1+x2+x3)(x2+x3+x4) 
def get_F():
    X = bin_generation(4)
    F = list()
    for x in X:
        # x0 в расчёт не берётся. Оно необходимо лишь для правила Видроу-Хоффа
        F.append(boolean_function(x[1], x[2], x[3], x[4]))
    return X, F


#Возвращает истинность или лож вырожения (x1+x2+x3)(x2+x3+x4)
def boolean_function(x1, x2, x3, x4):
    return (x1 or x2 or x3) and (x2 or x3 or x4)


# Перевод из 10чной в 2чную сист исчисл.
def IntToByte(x):
    n = '' if x > 0 else '0'
    while x > 0:
        y = str(x % 2)
        n = y + n
        x = int(x / 2)
    return n


# Генерирует набор векторов с числами от 0 до 16 в двоич. сист. исчсл.
def bin_generation(n):
    X = list()
    count = 2**n
    for i in range(0, count):
        X.append([int(x) for x in IntToByte(i)])
        while len(X[i]) < 4:
            X[i].insert(0, 0)
        X[i].insert(0, 1) # вставили x0
    return X