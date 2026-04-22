import argparse, csv
from tabulate import tabulate


class MainReport:
    @staticmethod
    def _parser_func():
        parser = argparse.ArgumentParser(description='my parser')
        parser.add_argument('--files', type=str, default=['stats1.csv', 'stats2.csv'], nargs='+',
                            help='list of current files with location')
        parser.add_argument('--report', type=str, default='clickbait', help='report name')
        namespace = parser.parse_args()
        return namespace.files

    def _valid_output(self, d):
        pass

    def _get_summary_list(self):
        sum_list = []
        for file in self._parser_func():
            with open(file, 'r', newline='', encoding='utf8') as csv_file:
                current_list = csv.DictReader(csv_file)
                sum_list.extend(list(current_list))
        return sum_list

    def print_result(self):
        result = tabulate(self._get_summary_list(), headers={}, tablefmt="grid")
        print(result)
        return


class ClickbaitReport(MainReport):
    ROWS = ('title', 'ctr', 'retention_rate')

    def _valid_output(self, d):
        if d.get('ctr') and d.get('retention_rate'):
            if float(d['ctr']) > 15 and float(d['retention_rate']) > 40:
                return True

    def _get_summary_list(self):
        sum_list = super()._get_summary_list()
        filter_sort_list = sorted(filter(self._valid_output, sum_list), key=lambda x: -float(x['ctr']))
        result = [{row: x[row] for row in self.ROWS} for x in filter_sort_list]
        return result


obj1 = MainReport()
obj2 = ClickbaitReport()
obj1.print_result()
obj2.print_result()