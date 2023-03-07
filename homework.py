import dataclasses as dc


@dc.dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**dc.asdict(self))


@dc.dataclass
class Training:
    """Базовый класс тренировки."""

    action: int  # повторений
    duration: float  # часы
    weight: float  # кг
    LEN_STEP = 0.65  # Метры.
    M_IN_KM = 1000
    ONE_HOUR_IN_MIN = 60

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info: InfoMessage = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return training_info


@dc.dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: str = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        spent_calories: float = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
            / self.M_IN_KM * (self.duration * self.ONE_HOUR_IN_MIN))
        return spent_calories


@dc.dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int
    COEFF_1: float = 0.035
    COEFF_2: float = 0.029
    COEFF_3: float = 0.278
    ONE_M_IN_CM: int = 100

    def get_spent_calories(self) -> float:
        spent_calories: float = (
            (self.COEFF_1 * self.weight
             + ((self.get_mean_speed() * self.COEFF_3) ** 2
                / (self.height / self.ONE_M_IN_CM))
             * self.COEFF_2 * self.weight) * self.duration
            * self.ONE_HOUR_IN_MIN)
        return spent_calories


@dc.dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    SWM_COEFF_1: int = 1.1
    SWM_COEFF_2: int = 2
    LEN_STEP: float = 1.38

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed() + self.SWM_COEFF_1)
                           * self.SWM_COEFF_2 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list[str, list]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        if workout_type in workout_type_dict:
            return workout_type_dict[workout_type](*data)
    except Exception as e:
        return ('Ошибка в вводе данных!', str(e))


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
