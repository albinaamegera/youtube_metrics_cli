import pytest
import tempfile
from pathlib import Path

from app.csv_reader import CSVReader
from app.reports import ClickbaitReport


class TestIntegration:
    """Интеграционные тесты"""

    @pytest.fixture
    def sample_csv_file1(self):
        content = """title,ctr,retention_rate,views,likes,avg_watch_time
Я бросил IT и стал фермером,18.2,35,45200,1240,4.2
Как я спал по 4 часа и ничего не понял,22.5,28,128700,3150,3.1
Почему сеньоры не носят галстуки,9.5,82,31500,890,8.9"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name

    @pytest.fixture
    def sample_csv_file2(self):
        content = """title,ctr,retention_rate,views,likes,avg_watch_time
Секрет который скрывают тимлиды,25.0,22,254000,8900,2.5
Купил джуну макбук и он уволился,19.0,38,87600,2100,4.5
Честный обзор на печеньки в офисе,6.0,91,12300,450,10.2"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name

    def test_full_pipeline_multiple_files(self, sample_csv_file1, sample_csv_file2):
        """Полный тест: чтение файлов + генерация отчета"""
        # Чтение файлов
        all_videos = CSVReader.read_multiple_files([sample_csv_file1, sample_csv_file2])

        assert len(all_videos) == 6

        # Генерация отчета
        report = ClickbaitReport()
        result = report.generate(all_videos)

        # Ожидаемые кликбейтные видео из обоих файлов
        # (ctr > 15 и retention_rate < 40)
        assert len(result) == 4

        # Проверка сортировки (по убыванию CTR)
        assert result[0]['title'] == "Секрет который скрывают тимлиды"
        assert result[0]['ctr'] == 25.0
        assert result[0]['retention_rate'] == 22

        assert result[1]['title'] == "Как я спал по 4 часа и ничего не понял"
        assert result[1]['ctr'] == 22.5
        assert result[1]['retention_rate'] == 28

        # Очистка
        Path(sample_csv_file1).unlink()
        Path(sample_csv_file2).unlink()

    def test_empty_result_with_no_matching_videos(self):
        """Тест, когда нет видео, подходящих под критерии"""
        content = """title,ctr,retention_rate,views,likes,avg_watch_time
Обычное видео,10.0,50,1000,100,5.0
Нормальное видео,5.0,60,2000,200,4.0"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name

        try:
            videos = CSVReader.read_file(temp_path)
            report = ClickbaitReport()
            result = report.generate(videos)
            assert len(result) == 0
        finally:
            Path(temp_path).unlink()

    def test_pipeline_with_error_file(self, sample_csv_file1):
        """Тест с ошибочным файлом (без заголовков)"""
        invalid_content = """Я бросил IT и стал фермером,18.2,35,45200,1240,4.2
Как я спал по 4 часа и ничего не понял,22.5,28,128700,3150,3.1"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(invalid_content)
            invalid_path = f.name

        try:
            # Должно выбросить ValueError из-за отсутствия заголовков
            with pytest.raises(ValueError, match="не содержит заголовков"):
                CSVReader.read_multiple_files([sample_csv_file1, invalid_path])
        finally:
            Path(sample_csv_file1).unlink()
            Path(invalid_path).unlink()