import argparse

from tabulate import tabulate

from app.csv_reader import CSVReader
from app.reports import ReportRegistry


def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='CLI приложение для обработки CSV-файлов с метриками видео YouTube'
    )

    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам (можно указать несколько)'
    )

    parser.add_argument(
        '--report',
        type=str,
        required=True,
        help=f'Тип отчета. Доступные: {ReportRegistry.get_available_reports()}'
    )

    return parser.parse_args()


def display_report(report_data: list[dict], headers: list[str]) -> None:
    """
    Вывод отчета в виде таблицы в консоль

    :Raises:
        ValueError: если нет данных, соответствующих критериям отчета
    """
    if not report_data:
        raise ValueError("Нет данных, соответствующих критериям отчета")

    table_data = []
    for item in report_data:
        row = []
        for header in headers:
            # Маппинг заголовков на ключи в словаре
            if header == 'Название видео':
                row.append(item.get('title', ''))
            elif header == 'CTR (%)':
                row.append(item.get('ctr', ''))
            elif header == 'Удержание (%)':
                row.append(item.get('retention_rate', ''))
            else:
                # Для других заголовков пытаемся найти соответствующий ключ
                key = header.lower().replace(' (%)', '').replace(' ', '_')
                row.append(item.get(key, ''))
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def main():
    args = parse_arguments()

    try:
        all_videos = CSVReader.read_multiple_files(args.files)

        report = ReportRegistry.get_report(args.report)
        report_data = report.generate(all_videos)
        headers = report.get_headers()

        display_report(report_data, headers)
    except Exception as e:
        print(e)

