import argparse, csv
from tabulate import tabulate


class MainReport:
    """Класс родительского отчёта по умолчанию - выводит записи всех указанных файлов"""
    def __init__(self, lst):
        self._lst = lst

    def _valid_output(self, d):
        raise NotImplementedError('В дочернем классе необходимо определить метод _valid_output')

    def _get_summary_list(self):
        sum_list = []
        for file in self._lst:
            with open(file, 'r', newline='', encoding='utf8') as csv_file:
                current_list = csv.DictReader(csv_file)
                sum_list.extend(list(current_list))
        return sum_list

    def get_result(self):
        result = tabulate(self._get_summary_list(), headers={}, tablefmt="grid")
        return result


class ClickbaitReport(MainReport):
    _COLS = ('title', 'ctr', 'retention_rate')

    def _valid_output(self, d):
        if d.get('ctr') and d.get('retention_rate'):
            if float(d['ctr']) > 15 and float(d['retention_rate']) > 40:
                return True

    def _get_summary_list(self):
        sum_list = super()._get_summary_list()
        filter_sort_list = sorted(filter(self._valid_output, sum_list), key=lambda x: -float(x['ctr']))
        result = [{row: x[row] for row in self._COLS} for x in filter_sort_list]
        return result


class Handler:
    REPORTS = {'main': MainReport, 'clickbait': ClickbaitReport}

    @staticmethod
    def _parser_func():
        parser = argparse.ArgumentParser(description='my parser')
        parser.add_argument('--files', type=str, default=[], nargs='+',
                            help='list of current files with location')
        parser.add_argument('--report', type=str, default='main', help='report name')
        namespace = parser.parse_args()
        return {'report': namespace.report, 'files': namespace.files}

    def get(self):
        try:
            report_obj = self.REPORTS[self._parser_func()['report']](self._parser_func()['files'])
            print(report_obj.get_result())
        except KeyError as e:
            print(f'Отчёт {e} не найден')
        except FileNotFoundError as e:
            print(f'Файл "{e.filename}" не найден')
        return


if __name__ == '__main__':
    handler = Handler()
    handler.get()