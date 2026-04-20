import argparse
from app.csv_reader import CSVReader


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

    return parser.parse_args()

def display_report():
    pass


def main():
    args = parse_arguments()

    try:
        all_videos = CSVReader.read_multiple_files(args.files)
        for video in all_videos:
            print(video)
    except Exception as e:
        print(e)

