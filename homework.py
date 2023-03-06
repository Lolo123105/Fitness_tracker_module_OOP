class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Метры.
    M_IN_KM: int = 1000
    ONE_HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,  # повторений
                 duration: float,  # часы
                 weight: float,  # кг
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM  # км
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        test_distance: float = self.get_distance()
        mean_speed: float = test_distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info: InfoMessage = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: str = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories: float = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
            / self.M_IN_KM * (self.duration * self.ONE_HOUR_IN_MIN))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_1: float = 0.035
    COEFF_2: float = 0.029
    COEFF_3: float = 0.278
    ONE_M_IN_CM: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories: float = (
            (self.COEFF_1 * self.weight
             + ((self.get_mean_speed() * self.COEFF_3) ** 2
                / (self.height / self.ONE_M_IN_CM))
             * self.COEFF_2 * self.weight) * self.duration
            * self.ONE_HOUR_IN_MIN)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    SWM_COEFF_1: int = 1.1
    SWM_COEFF_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,  # повторений
                 duration: int,  # часы
                 weight: int,  # кг
                 length_pool: int,  # м
                 count_pool: int  # повторений
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed() + self.SWM_COEFF_1)
                           * self.SWM_COEFF_2 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return workout_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # Гребки, часы, кг, метры, повторений.
        ('RUN', [15000, 1, 75]),  # Шагов, часы, кг.
        ('WLK', [9000, 1, 75, 180]),  # Шагов, часы, кг, см.
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
