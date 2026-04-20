import pytest
import tempfile
from pathlib import Path

from app.csv_reader import CSVReader
from app.models import VideoMetrics


class TestCSVReader:
    """Тесты для читателя CSV файлов"""

    @pytest.fixture
    def valid_csv_content(self):
        return """title,ctr,retention_rate,views,likes,avg_watch_time
Кликбейт видео,22.5,28,1000,100,5.0
Обычное видео,9.5,82,1500,150,8.0
Кликбейт видео 2,25.0,22,3000,300,3.0"""

    @pytest.fixture
    def valid_csv_content_with_extra_columns(self):
        """CSV с дополнительными колонками"""
        return """title,ctr,retention_rate,views,likes,avg_watch_time,extra_column
Кликбейт видео,22.5,28,1000,100,5.0,extra_value
Обычное видео,9.5,82,1500,150,8.0,extra_value2"""

    @pytest.fixture
    def csv_without_headers(self):
        """CSV без заголовков"""
        return """Кликбейт видео,22.5,28,1000,100,5.0
Обычное видео,9.5,82,1500,150,8.0"""

    def test_read_valid_csv(self, valid_csv_content):
        """Тест чтения корректного CSV файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(valid_csv_content)
            temp_path = f.name

        try:
            videos = CSVReader.read_file(temp_path)
            assert len(videos) == 3
            assert isinstance(videos[0], VideoMetrics)
            assert videos[0].title == "Кликбейт видео"
            assert videos[0].ctr == 22.5
            assert videos[0].retention_rate == 28
            assert videos[0].views == 1000
            assert videos[0].likes == 100
            assert videos[0].avg_watch_time == 5.0
        finally:
            Path(temp_path).unlink()

    def test_read_valid_csv_with_extra_columns(self, valid_csv_content_with_extra_columns):
        """Тест чтения CSV с дополнительными колонками"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(valid_csv_content_with_extra_columns)
            temp_path = f.name

        try:
            videos = CSVReader.read_file(temp_path)
            assert len(videos) == 2
            assert videos[0].title == "Кликбейт видео"
            assert videos[0].ctr == 22.5
            assert videos[0].retention_rate == 28
        finally:
            Path(temp_path).unlink()

    def test_read_file_not_found(self):
        """Тест на отсутствие файла"""
        with pytest.raises(FileNotFoundError, match="Файл не найден"):
            CSVReader.read_file("nonexistent.csv")

    def test_read_multiple_files_success(self, valid_csv_content):
        """Тест успешного чтения нескольких файлов"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f1:
            f1.write(valid_csv_content)
            path1 = f1.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f2:
            f2.write(valid_csv_content)
            path2 = f2.name

        try:
            videos = CSVReader.read_multiple_files([path1, path2])
            assert len(videos) == 6
            assert all(isinstance(v, VideoMetrics) for v in videos)
        finally:
            Path(path1).unlink()
            Path(path2).unlink()

    def test_read_multiple_files_empty_list(self):
        """Тест чтения пустого списка файлов"""
        videos = CSVReader.read_multiple_files([])
        assert len(videos) == 0
        assert isinstance(videos, list)

    def test_read_multiple_files_file_not_found(self):
        """Тест чтения с несуществующим файлом"""
        with pytest.raises(FileNotFoundError, match="Файл не найден"):
            CSVReader.read_multiple_files(["nonexistent.csv"])

    def test_read_csv_with_invalid_data_type(self):
        """Тест чтения CSV с некорректным типом данных"""
        content = """title,ctr,retention_rate,views,likes,avg_watch_time
Видео 1,не число,28,1000,100,5.0"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name

        try:
            # VideoMetrics выбросит ValueError при преобразовании строки в число
            with pytest.raises(ValueError):
                CSVReader.read_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_read_csv_with_missing_required_column(self):
        """Тест чтения CSV с отсутствующей обязательной колонкой"""
        content = """title,ctr,views,likes,avg_watch_time
Видео 1,22.5,1000,100,5.0"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name

        try:
            # VideoMetrics выбросит KeyError при отсутствии колонки retention_rate
            with pytest.raises(KeyError):
                CSVReader.read_file(temp_path)
        finally:
            Path(temp_path).unlink()