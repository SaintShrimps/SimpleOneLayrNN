# Модуль получения нейросетевой модели БФ, используя логистическую ФА (сигмоидальную).
# И нахождения наименьшее, возможное для обучения, количество векторов.


from DataIO import *
from neuronal import *
from Graphic import *
import itertools

# Функция записывает в файл процесс обучения 
# Hа минимально возможном количестве векторов
def write_min(combination, outputFile, W, kind):
    # запишем в файл найденные значения
    file = open(outputFile, 'w')
    file.write('set:\n')
    for i,x in enumerate(combination[1]):
        file.write('X(' + str(i+1) + ') = (' + str(x[0])[4:-1] + ')')
        file.write('\n')
    file.write('\n')

    nu = 0.3 # норма обучения
    E = 1 # необходимо для начала цикла прохода по эпохам
    k = 0 # необходимо для начала отсчёта эпох

    arrayE = list() # список всех суммарнах квадратичных ошибок
    arrayK = list() # список всех эпох

    Y = list() # вектор для хранения полученного реального выхода текущей эпохи

    F = [i[1] for i in combination[1]] # вектор значений БФ, на котром происходит обучение

    #Обучение до тех пор, пока квадратичная ошибка не будет = 0
    while E != 0:
        #Записываем последние полученные весовые коэффициенты на случай получения нулевой ошибки
        prev_W = list(W)

        #Проверка на достижение нулевой ошибки на последних найденных весовых коэффициентах
        for (x, f) in combination[1]:
            # 1)Подесчет net
            n = net(W, x)

            # 2)Реальный выход
            y = actual_NN(n)
            Y.append(y)

            # 3)Ошибку дельта
            d = delta(f, y)

        # 5)Подсчет сумарной квадратичной ошибки
        E = totalError(Y, F)

        #Запись полученных данные в файл
        write_Data(file, k, Y, prev_W, E)

        Y = list() #Очистка вектора от полученных данных

        # Если ошибка(Е) != 0 выполняется перерасчёт весовых коэффициентов
        if E != 0:

            for (x,f) in combination[1]:
                n = net(W, x)
                y = actual_NN(n)
                d = delta(f, y)

                #Пересчеи W(Синаптические вес)
                W = recount_W(W, x, d, n, nu, kind)

        #Добавление номера текущей эпохи и найденную в ней среднеквадратичную ошибку
        arrayK.append(k)
        arrayE.append(E)
                
        k += 1#Увеличивание количество эпох +1

    #Построение графиа зависимости среднеквадратичной ошибки от эпохи
    drawGraph(arrayE, arrayK, kind, outputFile)


#Функция проверяется комбинация на "обучаемость"
#W: входные значения весовых коэффициентов
#combination: найденная наилучшая комбинация векторов
#kind: вид ФА threshold - пороговая, logistics - логистическая
#В случае успеха возвращается W, k(эпоха), иначе  W, 0
def check_combination(W, combination, kind):
    nu = 0.3 #норма
    E = 1 #Ср^2 ошибка
    k = 0 #Эпох

    Y = list() #Вектор для хранения полученного реального выхода текущей эпохи

    #Обучение до достигжения ошибок = 0, если это возможно
    #Для этого в качестве "порога" поиска берется ограниченное число эпох для обучения
    epochs = 200
    while E != 0 and k < epochs:
        e = 0 #Переменная для поиска ошибок при обучении

        # запоминаем последние полученные весовые коэффициенты на случай получения нулевой ошибки
        prev_W = list(W)

        # проверим выходной вектор на наличие ошибок
        for (x, f) in combination:
            n = net(W, x)
            y = actual_NN(n)
            d = delta(f, y)

            #Если имеется ошибкв, прибавим её к переменной для отслеживания ошибок обучения
            if d != 0:
                e += 1

        #В случае ошибки выходного вектора
        if e != 0:
            e = 0
            #Обучение на выборке
            for (x,f) in combination:
                n = net(W, x)
                y = actual_NN(n)
                d = delta(f, y)

                if d != 0:
                    e += 1 # ошибка для обучения на векторе

                # 4) пересчитываем W
                W = recount_W(W, x, d, n, nu, kind = kind)
        E = e     
        k += 1 #Следующей эпохе +1

    if k < epochs:
        return W, k
    else:
        return W, 0


#Функция поиска минимального вектора для обучения
#inputW: входные значения весовых коэффициентов
#inputF: значения БФ
#X: вектор с значениями от 0 до 16 в двоичном представлении
#outputFile: имя файла записи
#kind: вид ФА threshold - пороговая, logistics - логистическая
def education_AF(inputW, F, X, outputFile, kind):
    for i in range(2**4, 2, -1):
        #Генерация комбинаций векторов различных длин
        combinations = list(itertools.combinations(zip(X, F), i))

        arrayKN = list()

        #Проверка каждой комбинации
        for combination in combinations:

            Y = list()

            W, k = check_combination(list(inputW), combination, kind)

            if k != -1:

                #Проверка успешности обучения
                for (x, f) in zip(X, F):
                    n = net(W, x)
                    y = actual_NN(n)
                    Y.append(y)

                # 5)Подсчет суммарной квадратичной ошибки
                E = totalError(Y, F)

                #Запись найденных векторов, кол-во эпох обучения и набор весов
                if E == 0:
                    arrayKN.append((k, combination, W))
                    best_combination = sorted(arrayKN, key = lambda education: education[0])[0]

    #Запись в файл минимальный набор с минимальным количеством эпох
    write_min(best_combination, outputFile, list(inputW), kind)
