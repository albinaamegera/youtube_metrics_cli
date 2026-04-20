import pytest
from app.models import VideoMetrics
from app.reports import ClickbaitReport, ReportRegistry


class TestClickbaitReport:
    """Тесты для отчета о кликбейтных видео"""

    @pytest.fixture
    def sample_videos(self):
        return [
            VideoMetrics({'title': 'Видео 1', 'ctr': '22.5', 'retention_rate': '28',
                          'views': '1000', 'likes': '100', 'avg_watch_time': '5.0'}),
            VideoMetrics({'title': 'Видео 2', 'ctr': '18.2', 'retention_rate': '35',
                          'views': '2000', 'likes': '200', 'avg_watch_time': '4.5'}),
            VideoMetrics({'title': 'Видео 3', 'ctr': '9.5', 'retention_rate': '82',
                          'views': '1500', 'likes': '150', 'avg_watch_time': '8.0'}),
            VideoMetrics({'title': 'Видео 4', 'ctr': '25.0', 'retention_rate': '22',
                          'views': '3000', 'likes': '300', 'avg_watch_time': '3.0'}),
            VideoMetrics({'title': 'Видео 5', 'ctr': '16.5', 'retention_rate': '42',
                          'views': '500', 'likes': '50', 'avg_watch_time': '4.0'}),
            VideoMetrics({'title': 'Видео 6', 'ctr': '19.0', 'retention_rate': '38',
                          'views': '800', 'likes': '80', 'avg_watch_time': '4.2'}),
        ]

    def test_clickbait_filtering(self, sample_videos):
        report = ClickbaitReport()
        result = report.generate(sample_videos)

        # Должны быть отфильтрованы только видео с ctr > 15 и retention < 40
        assert len(result) == 4
        assert all(item['ctr'] > 15 for item in result)
        assert all(item['retention_rate'] < 40 for item in result)

    def test_clickbait_sorting(self, sample_videos):
        report = ClickbaitReport()
        result = report.generate(sample_videos)

        # Проверка сортировки по убыванию CTR
        ctr_values = [item['ctr'] for item in result]
        assert ctr_values == sorted(ctr_values, reverse=True)

    def test_clickbait_headers(self):
        report = ClickbaitReport()
        headers = report.get_headers()
        assert headers == ['Название видео', 'CTR (%)', 'Удержание (%)']

    def test_empty_result(self):
        videos = [
            VideoMetrics({'title': 'Видео 1', 'ctr': '10.0', 'retention_rate': '50',
                          'views': '1000', 'likes': '100', 'avg_watch_time': '5.0'}),
            VideoMetrics({'title': 'Видео 2', 'ctr': '20.0', 'retention_rate': '45',
                          'views': '2000', 'likes': '200', 'avg_watch_time': '4.5'}),
        ]
        report = ClickbaitReport()
        result = report.generate(videos)
        assert len(result) == 0


class TestReportRegistry:
    """Тесты реестра отчетов"""

    def test_register_and_get_report(self):
        assert 'clickbait' in ReportRegistry.get_available_reports()

        report = ReportRegistry.get_report('clickbait')
        assert isinstance(report, ClickbaitReport)

    def test_get_invalid_report(self):
        with pytest.raises(ValueError, match="Неизвестный тип отчета"):
            ReportRegistry.get_report('invalid_report')