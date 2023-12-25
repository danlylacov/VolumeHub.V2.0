from math import sqrt



class StandartDeviation(object):

    def __init__(self, volumes: list, stream_volume: int, z_limit: float = 2.8):
        '''
        Конструктор класса
        :param volumes: список со значениями объёмов по определённой акции
        :param stream_volume: список, полученный в данный момент
        :param z_limit: параметр для сравнения с Z-оценкой default: 0.9544

        result: результат работы z-оценки(bool, True - аномальный объем, False - обычный объем

        '''
        self.volumes = volumes
        self.sream_volume = stream_volume
        self.z_limit = z_limit

        self.result = self.check_anomal()

    def sorted_and_clipping(self):
        '''
        Сортировка и отсечение 25% самых больших и маленьких зн-й
        :return:
        '''
        self.volumes.sort()
        #self.volumes = self.volumes[len(self.volumes)//4:-(len(self.volumes)//4)]


    def get_average_value(self): # -> float
        '''
        Получение среднего зн-я оюбъёмов
        :return: среднее зн-е
        '''
        avarage_value = sum(self.volumes)/len(self.volumes)
        return avarage_value


    def get_standart_deviation(self): # -> float
        '''
        получение стандартного отклонения (сигма)
        :return: стандартное отклонение
        '''
        sum_of_deviations = 0
        avarage_value = self.get_average_value()
        for i in range(len(self.volumes)):
            sum_of_deviations += (self.volumes[i] - avarage_value)**2
        return sqrt(sum_of_deviations/(len(self.volumes)-1))


    def get_z_score(self, avarage_value: float, standart_deviation: float): # -> float
        '''
        получение z-оценки
        :param avarage_value: Среднее зн-е
        :param standart_deviation: Стандартное отклонение
        :return: z-оценка
        '''
        z = (self.sream_volume - avarage_value)/ standart_deviation
        return z


    def check_anomal(self): # -> bool
        '''
        главная функция, выполняет все расчеты и проверяет  выходит ли z-оценка за пределы допустимого зн-я (self.z_limit)
        :return: bool
        '''
        self.sorted_and_clipping()
        z_deviation = self.get_z_score(self.get_average_value(), self.get_standart_deviation())
        if z_deviation > self.z_limit:
            return True, z_deviation
        else:
            return False, z_deviation































