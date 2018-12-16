'''
Учебно-вычислительна практика
Данная программа высчитывает маршрут для парусной гонки
Более подробное описание находится в отчете.

Переменные:
dir_data - массив диапазонов
data - матрица координат
tot_dis - общая дистанция
angle - угол поворота
total_len - пройденная дистанция
total_time - пройденное время
leg - кол-во курсов
no_pen - курсы без штрафов
tg - тангенс угла
speed - массив скоростей

Тестовый пример:
45 10 0.1 6
45 0.5 90 0.75 135 0.67
M1 15 10
M2 25 20
M3 22 30
M4 5 25
M5 10 15
M6 10 10
0 0 0 0
===============================================================================
Гонка 1 состоит из 6 шагов
Длина дистанции 58.48 nm
───────────────────────────────────────────────────────────────────────────────
Шаг 1 из отметки M1 к M2 ⇒ Направление: 45.0 Расстояние: 14.14 nm
Курс 1 > Скорость:  5.0 Направление: 90.0 Расстояние:10.0 nm
Курс 2 > Скорость:  5.0 Направление: 0.0 Расстояние:10.0 nm

Шаг 2 из отметки M2 к M3 ⇒ Направление: 343.3 Расстояние: 10.44 nm
Курс 3 > Скорость: 5.0 Направление: 343.3 Расстояние: 10.44

Шаг 3 из отметки M3 к M4 ⇒ Направление: 253.6 Расстояние: 17.72 nm
Курс 4 > Скорость: 6.7 Направление: 253.6 Расстояние: 17.72

Шаг 4 из отметки M4 к M5 ⇒ Направление: 153.4 Расстояние: 11.18 nm
Курс 5 > Скорость: 7.5 Направление: 153.4 Расстояние: 11.18

Шаг 5 из отметки M5 к M6 ⇒ Направление: 180.0 Расстояние: 5.0 nm
Курс 6 > Скорость: 6.7 Направление: 180 Расстояние: 5.0

───────────────────────────────────────────────────────────────────────────────
Гонка 1 была 64.34 nm длиной с сменой 6 курсов
Оценочная продолжительность гонки 11.47 часов с 0.5 часа штрафа
===============================================================================
'''


# Импорт библиотек для вычислений
from math import sqrt,atan,degrees,tan,radians,sin

# Стартовая функция
def start(a):
    nomer = a
    # Ввод изначальных данных 
    need_data = ('Введите: \n'
                 'Направоение ветра, скорость ветра, \
штрафное время, кол-во отметок N\n')
    dir,speed_w,penalty,N = map(float,input(need_data).split())
    speed,N = [0,0,0],int(N)
    need_data = ('Контрольный угол, контрольный коэффицент скорости\n')
    point_a,speed[0] = map(float,input(need_data).split())

    need_data = ('Доступный угол, доступный коэффицент скорости\n')
    reach_a,speed[1] = map(float,input(need_data).split())

    need_data = ('Подветренный угол, подветренный коэффицент скорости\n')
    downwind_a,speed[2] = map(float,input(need_data).split())

    # Вычесление дипазонов скорости
    dir_data = [[0 for j in range(2)] for i in range(3)]
    dir_data[0][0],dir_data[0][1] = dir - point_a,dir + point_a
    dir_data[1][0],dir_data[1][1] = dir - reach_a,dir + reach_a
    dir_data[2][0],dir_data[2][1] = dir - downwind_a,dir + downwind_a

    # Ввод координат 
    data = [[0 for j in range(2)] for i in range(N)]
    print('Введите координаты отметок')
    for i in range(N):
        data[i][0],data[i][1] = map(int,input('M' + str(i + 1) + ' ').split())
    print('0 ' + '0 ' + '0 ' + '0')
    print(79 * '=')
    print('Гонка ' + str(nomer) + ' состоит из ' + str(N) + ' шагов')
    tot_dis,total_time,no_pen = 0,0,0

    # Рассчет общей дистанции
    for i in range(len(data) - 1):
        tot_dis += distance(data[i][0],data[i][1],
                            data[i + 1][0],data[i + 1][1])
    print('Длина дистанции ' + str(round(tot_dis,2)) + ' nm')
    print(79 * '─')
    leg = 1
    total_len = 0

    # Начало главного цикла
    for i in range(N - 1):
        # Нахождение текущего местоположение
        # Нахождение следующей точки
        x,y=data[i][0],data[i][1]
        x_n,y_n=data[i + 1][0],data[i + 1][1]
        if i==0:
            old_angle = -1
        else:
            old_angle = angle
        print('Шаг ' + str(i + 1) + ' из отметки M' + str(i + 1)
              + ' к M' + str(i + 2) + ' ' + '\u21D2 Направление:',end=' ')
        # Расчет тангенса и самого угла движения
        try:
            tg = abs(y_n - y) / abs(x_n - x)
            if x_n - x > 0:
                if y_n - y > 0:
                    angle = round(90 - degrees(atan(tg)),1)
                else:
                    angle = round(90 + degrees(atan(tg)),1)
            else:
                if y_n - y > 0:
                    angle = round(270 + degrees(atan(tg)),1)
                else:
                    angle = round(270 - degrees(atan(tg)),1)
            print(angle,end=' ')
        except:
            angle = 180
            print('180.0',end=' ')
        if old_angle==angle:
            no_pen += 1
            
        # Расчет скорости по углу
        result = check(angle,dir_data)

        # Проверка не совпадает ли угл с контрольным
        if result==0:
            print('Расстояние: ' + str(round(distance(x,y,x_n,y_n),2)) + ' nm')
            # Расчет объезда
            angle1 = dir_data[0][1]-angle
            angle2 = point_a*2
            angle3 = 180-angle1-angle2
            storona2 = distance(x,y,x_n,y_n)
            s = storona2/sin(radians(angle2))
            # Решение треугольника теорема синусов
            storona1,storona3=s*sin(radians(angle1)),s*sin(radians(angle3))
            if dir_data[0][0]<0:
                a = dir_data[0][0]+360
            else:
                a = dir_data[0][0]
            if dir_data[0][1]>360:
                b = dir_data[0][1]-360
            else:
                b = dir_data[0][1]
            # Выввод результатов
            print('Курс ' + str(leg) + ' > Скорость: ',
                  str(speed[0] * speed_w),end=' ')
            print('Направление: ' + str(b)
                  + ' Расстояние:' + str(round(storona3,2)) + ' nm')
            leg+=1
            print('Курс ' + str(leg) + ' > Скорость: ',
                  str(speed[0] * speed_w),end=' ')
            print('Направление: ' + str(a)
                  + ' Расстояние:' + str(round(storona1,2)) + ' nm')
            # Добавление результа к общему значению
            total_len += storona1+storona3
            total_time += (storona1+storona3)/(speed[0]*speed_w)
        else:
            # Если угол не в контрольной зоне, делается простой выввод 
            print('Расстояние: ' + str(round(distance(x,y,x_n,y_n),2)) + ' nm')
            print('Курс ' + str(leg) + ' > Скорость: ',end='')
            print(str(speed[result - 1] * speed_w) + ' Направление: '
                  + str(angle) + ' Расстояние: ' +
                  str(round(distance(x,y,x_n,y_n),2)))
            # Добавление результа к общему значению
            total_len += distance(x,y,x_n,y_n)
            total_time += distance(x,y,x_n,y_n) / (speed[result - 1] * speed_w)
        leg += 1
        print()
    print(79 * '─')
    print(
        'Гонка ' + str(nomer) + ' была ' + str(round(total_len,2))
        + ' nm длиной с сменой ' + str(leg - 1) + ' курсов')
    print('Оценочная продолжительность гонки ' + str(
        round(total_time + penalty * (leg - 2 - no_pen),2)) + ' часов с '
          + str(round(penalty * (leg - 2 - no_pen),2)) + ' часа штрафа')
    print(79 * '=')
    reset(nomer)


def distance(a,b,c,d):
    # Нахождение расстояния по формуле пифогора
    result = sqrt((a - c) ** 2 + (b - d) ** 2)
    return result


def check(a,b):
    if a < 0:
        a += 360
    if a > 360:
        a -= 360
    # Проверка нождения угла в трех угловых зонах
    for i in range(3):
        if b[i][0] < 0:
            if b[i][0] + 360 < a <= 360 or 0 <= a < b[i][1]:
                return i
        elif b[i][1] > 360:
            if b[i][0] < a <= 360 or 0 <= a < b[i][1] - 360:
                return i
        else:
            if b[i][0] < a < b[0][1]:
                return i
    return 3

def reset(a):
    print()
    if input('Хотите провести еще один расчет? ').lower() == 'да':
        start(a+1)


start(1)
