# Импорт библиотек для вычислений
from math import sqrt,atan,degrees,tan,radians

# Стартовая функция
def start():

    # Ввод изначальных данных 
    need_data = ('Введите: \n'
                 'Направоение ветра, скорость ветра, \
штрафное время, кол-во отметок N\n')
    dir,speed,penalty,N = map(float,input(need_data).split())
    speed,nomer,N = [0,0,0],1,int(N)
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
            # Расчет объезда
            print('Расстояние: ' +
                  str(round(distance(x,y,x_n,y_n),2)) + ' nm')
            m = max(abs(angle - dir_data[0][0]),abs(angle - dir_data[0][1]))
            katet1 = distance(x,y,x_n,y_n) / 2
            katet2 = katet1 * tan(radians(m))
            dis = round(sqrt(katet1 ** 2 + katet2 ** 2),2)
            print('Курс ' + str(leg) + ' > Скорость: ',
                  str(speed[check(angle + m,dir_data) - 1] * 10),end=' ')
            print('Направление: ' + str(angle + m)
                  + ' Расстояние:' + str(dis) + ' nm')
            leg += 1
            total_time += dis / (speed[check(angle + m,dir_data) - 1] * 10)
            print('Курс ' + str(leg) + ' > Скорость: ',
                  str(speed[check(angle - m,dir_data) - 1] * 10),end=' ')
            print('Направление: ' + str(angle - m)
                  + ' Расстояние:' + str(dis) + ' nm')
            # Добавление результа к общему значению
            total_len = total_len + dis * 2
            total_time += dis / (speed[check(angle - m,dir_data) - 1] * 10)
        else:
            # Если угол не в контрольной зоне, делается простой выввод 
            print('Расстояние: ' + str(round(distance(x,y,x_n,y_n),2)) + ' nm')
            print('Курс ' + str(leg) + ' > Скорость: ',end='')
            print(str(speed[result - 1] * 10) + ' Направление: '
                  + str(angle) + ' Расстояние: ' +
                  str(round(distance(x,y,x_n,y_n),2)))
            # Добавление результа к общему значению
            total_len += distance(x,y,x_n,y_n)
            total_time += distance(x,y,x_n,y_n) / (speed[result - 1] * 10)
        leg += 1
        print()
    print(79 * '─')
    print(
        'Гонка ' + str(nomer) + ' была ' + str(round(total_len,2))
        + ' nm длиной с сменой ' + str(leg - 1) + ' курсов')
    print('Оценочная продолжительность гонки ' + str(
        round(total_time + penalty * (leg - 2 - no_pen),2)) + ' часов с '
          + str(penalty * (leg - 2 - no_pen)) + ' часа штрафа')
    print(79 * '=')


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


start()
