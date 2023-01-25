class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        """Вернуть информацию о тренировке"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    H_IN_M = 60
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Расчет калорий в беге: (18 * средняя скорость + 1.79)
           * вес спортсмена / M_IN_KM * время тренировки в минутах
        """
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * (self.weight / self.M_IN_KM
                * (self.duration * self.H_IN_M)))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KOEF_IN_WEIGHT = 0.035
    KOEF_IN_WEIGHT2 = 0.029
    AVG_SPEED_IN_M_S = 0.278
    HEIGHT_TO_SM = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """ Расчет калорий в Ходьбе((0.035 * вес +
            (Сред. скорость в м/сек **2 / рост в метрах)
            * 0.029 * вес) * время тренировки в минутах)
        """
        return ((self.KOEF_IN_WEIGHT * self.weight
                + (self.get_mean_speed() * self.AVG_SPEED_IN_M_S) ** 2
                / (self.height / self.HEIGHT_TO_SM)
                * self.KOEF_IN_WEIGHT2 * self.weight)
                * self.duration * self.H_IN_M)


class Swimming(Training):
    """Тренировка: плавание."""
    KOEF_IN_SWIM = 1.1
    LEN_STEP = 1.38
    DEGREE_KAL = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Расчет сред. скорости в плавании: длина бассейна
           * count_pool / M_IN_KM / время тренировки
        """
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расчёта  калорий в плавании:
           (средняя скорость + 1.1) * 2 * вес * время тренировки"""
        return ((Swimming.get_mean_speed(self) + self.KOEF_IN_SWIM)
                * self.DEGREE_KAL * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code = {'SWM': Swimming,
                     'WLK': SportsWalking,
                     'RUN': Running}
    training_class = training_code[workout_type](*data)
    return training_class


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
