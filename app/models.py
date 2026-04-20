class VideoMetrics:
    """Модель данных для метрик видео"""
    def __init__(self, row: dict):
        self.title: str = row['title']
        self.ctr: float = float(row['ctr'])
        self.retention_rate: float = float(row['retention_rate'])
        self.views: int = int(row['views'])
        self.likes: int = int(row['likes'])
        self.avg_watch_time: float = float(row['avg_watch_time'])