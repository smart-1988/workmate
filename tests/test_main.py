import pytest, argparse, os
from unittest.mock import patch
from main import ClickbaitReport, Handler


# Fixture для создания временного CSV-файла
@pytest.fixture
def csv_file():
    filename = 'test_data.csv'
    data = "title,ctr,retention_rate,views,likes,avg_watch_time\n" \
           "Title 1,16,45,45200,1240,4.2\n" \
           "Title 2,10,50,10500,500,3\n" \
           "Title 3,20,30,8978,269,2.4\n"

    with open(filename, 'w', newline='', encoding='utf8') as f:
        f.write(data)
    yield filename
    os.remove(filename)


def test_valid_output():
    """Проверка фильтра ctr > 15 и retention_rate < 40"""

    report = ClickbaitReport([])
    assert report._valid_output({'ctr': '16', 'retention_rate': '45'}) is None
    assert report._valid_output({'ctr': '10', 'retention_rate': '50'}) is None
    assert report._valid_output({'ctr': '16', 'retention_rate': '30'}) is True


def test_get_summary_list(csv_file):
    """Сравнение выходного списка после работы фильтра"""

    report = ClickbaitReport([csv_file])
    expected_result = [{'title': 'Title 3', 'ctr': '20', 'retention_rate': '30'}]
    result = report._get_summary_list()
    assert result == expected_result


def test_handler_invalid_report():
    """Проверка вывода при неверном имени отчёта"""

    report_name = 'invalid'
    handler = Handler()
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(report=report_name, files=[])):
        result = handler.get()
        assert result == 'Отчёт \'invalid\' не найден'


def test_handler_file_not_found():
    """Проверка вывода при неверном указании файлов"""

    handler = Handler()
    with patch('argparse.ArgumentParser.parse_args',
               return_value=argparse.Namespace(report='clickbait', files=['non_existent_file.csv'])):
        result = handler.get()
        assert result == 'Файл "non_existent_file.csv" не найден'


def test_handler_success(csv_file):
    """Проверка корректности результата через обработчик"""

    handler = Handler()
    with patch('argparse.ArgumentParser.parse_args',
               return_value=argparse.Namespace(report='clickbait', files=[csv_file])):
        result = handler.get()
        assert "Title 3" in result
        assert "Title 2" not in result
        assert "Title 1" not in result