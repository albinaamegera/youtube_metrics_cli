from abc import ABC, abstractmethod
from typing import List, Dict, Type

from app.models import VideoMetrics


class Report(ABC):
    """Абстрактный базовый класс для всех отчетов"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Название отчета (ключ для --report)"""
        pass

    @abstractmethod
    def generate(self, videos: List[VideoMetrics]) -> List[Dict]:
        """
        Генерация отчета из списка видео

        Args:
            videos: список всех видео

        Returns:
            List[Dict]: список словарей с данными для таблицы
        """
        pass

    @abstractmethod
    def get_headers(self) -> List[str]:
        """Возвращает заголовки колонок для таблицы"""
        pass


class ClickbaitReport(Report):
    """Отчет о кликбейтных видео (CTR > 15, retention < 40)"""

    @property
    def name(self) -> str:
        return "clickbait"

    def generate(self, videos: List[VideoMetrics]) -> List[Dict]:
        filtered = [
            video for video in videos
            if video.ctr > 15 and video.retention_rate < 40
        ]

        # Сортировка по убыванию CTR
        sorted_videos = sorted(filtered, key=lambda x: x.ctr, reverse=True)

        return [
            {
                'title': video.title,
                'ctr': round(video.ctr, 2),
                'retention_rate': round(video.retention_rate, 2)
            }
            for video in sorted_videos
        ]

    def get_headers(self) -> List[str]:
        return ['Название видео', 'CTR (%)', 'Удержание (%)']

# Пример добавления нового отчета
class NewReport(Report):
    @property
    def name(self) -> str:
        return "new_report"

    def generate(self, videos):
        # логика фильтрации
        return []

    def get_headers(self):
        return ['Колонка 1', 'Колонка 2']


class ReportRegistry:
    """Реестр доступных отчетов"""

    _reports: Dict[str, Type[Report]] = {}

    @classmethod
    def register(cls, report_class: Type[Report]) -> None:
        """Регистрация нового отчета"""
        instance = report_class()
        cls._reports[instance.name] = report_class

    @classmethod
    def get_report(cls, name: str) -> Report:
        """Получение экземпляра отчета по имени"""
        if name not in cls._reports:
            raise ValueError(f"Неизвестный тип отчета: {name}. Доступные: {list(cls._reports.keys())}")
        return cls._reports[name]()

    @classmethod
    def get_available_reports(cls) -> List[str]:
        """Получение списка доступных отчетов"""
        return list(cls._reports.keys())


# Регистрация доступных отчетов
ReportRegistry.register(ClickbaitReport)
ReportRegistry.register(NewReport)
