from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
                    'Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        """Возвращает сообщение в функцию main."""

        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60.0

    def __init__(
                 self,
                 action: float,
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

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
                           type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Расчет каллорий Running."""

        return (
                (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.MIN_IN_HOUR)
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    RATE_WEIGHT_1: float = 0.035
    RATE_WEIGHT_2: float = 0.029
    HEIGHT_CENTIM_IN_METER: float = 100.0
    NUM_KMH_IN_MS: float = 0.278

    def __init__(
                 self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: int
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет каллорий SportsWalking."""
        return (
                (self.RATE_WEIGHT_1 * self.weight
                 + (((self.get_mean_speed() * self.NUM_KMH_IN_MS) ** 2)
                    / (self.height / self.HEIGHT_CENTIM_IN_METER)
                    * self.RATE_WEIGHT_2 * self.weight))
                * self.duration * self.MIN_IN_HOUR
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    RATE_SPEED_1: float = 1.1
    RATE_WEIGHT_2: float = 2.0

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Расчет каллорий Swimming."""

        return (
                (self.get_mean_speed() + self.RATE_SPEED_1)
                * self.RATE_WEIGHT_2 * self.weight * self.duration
                )

    def get_mean_speed(self) -> float:
        """Расчет средней скорости Swimming."""

        return (
                self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    TRAINING_TYPE: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
        }
    if workout_type not in TRAINING_TYPE:
        raise NameError(f'Training {workout_type} is absent.')
    return TRAINING_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
        ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
