from bs4 import BeautifulSoup

with open('List_of_Chinese_monarchs.html') as f:
    HTML_TO_PARSE = f.read()


class TableParse:
    def __init__(self, table):
        self.table = table
        self._headers = []
        self._header_count = 0
        self._column_count = 0
        self._parse_header()

    def _parse_header(self):
        first_row = self.table.find('tr')
        for column in first_row.find_all('th'):
            colspan = column.get('colspan')
            column_count = int(colspan) if colspan else 1
            self._headers.append({
                'name': column.text.strip(),
                'index': self._header_count,
                'column_count': column_count,
                'column_start': self._column_count,
                'column_end': self._column_count + column_count,
            })
            self._header_count += 1
            self._column_count += column_count

    def iter_column_by_header(self, *header_names):
        table_content = self.table.find_all('tr')
        if self._headers:
            table_content = table_content[1:]

        column_index_list = [(header['column_start'], header['column_end'])
                             for header in self._headers if header['name'] in header_names]

        if not column_index_list:
            return

        for row in table_content:
            columns = row.find_all('td')
            find_columns = []
            for start, end in column_index_list:
                find_columns.append(columns[start:end])
            yield find_columns


def parse_chinese_name():
    soup = BeautifulSoup(HTML_TO_PARSE, 'lxml')
    tables = soup.find_all('table', {'class': 'wikitable'})
    chinese_names = []
    for table in tables:
        parser = TableParse(table)

        for column in parser.iter_column_by_header('Personal name'):
            if column[0]:
                chinese_names.append(column[0][-1].text.strip())
    return chinese_names


if __name__ == '__main__':
    pass
