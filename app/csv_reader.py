import csv
from pathlib import Path

from app.models import VideoMetrics


class CSVReader:
    """Читатель CSV файлов с метриками видео"""

    @staticmethod
    def read_file(file_path: str) -> list[VideoMetrics]:
        """
        Чтение одного CSV файла и преобразование в список VideoMetrics

        Args:
            file_path: путь к CSV файлу

        Returns:
            list[VideoMetrics]: список метрик видео

        Raises:
            ValueError: если файл не содержит заголовки
            FileNotFoundError: если файл не найден
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        videos = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                raise ValueError(f"Файл {file_path} не содержит заголовков")


            for row in reader:
                video = VideoMetrics(row)
                videos.append(video)

        return videos

    @staticmethod
    def read_multiple_files(file_paths: list[str]) -> list[VideoMetrics]:
        """
        Чтение нескольких CSV файлов и объединение результатов

        Args:
            file_paths: список путей к CSV файлам

        Returns:
            list[VideoMetrics]: объединенный список метрик из всех файлов

        Raises:
            ValueError: если файл не содержит заголовки
            FileNotFoundError: если файл не найден
        """
        all_videos = []
        for file_path in file_paths:
            try:
                videos = CSVReader.read_file(file_path)
                all_videos.extend(videos)
            except Exception as e:
                raise e

        return all_videos