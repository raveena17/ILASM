
from django.db.models.query import QuerySet
from django.http import HttpResponse

import datetime
import StringIO

class ExcelResponse(HttpResponse):

    def __init__(self, data, output_name='excel_data', headers=None,
                 force_csv=False, encoding='utf8'):

        # Make sure we've got the right type of data to work with
        self.encoding = encoding
        valid_data = False
        fromobj = False
        if isinstance(data, QuerySet):
            data = list(data.values())
        if hasattr(data, '__getitem__') and len(data)>0 :
            if isinstance(data[0], dict):
                if headers is None:
                    headers = data[0].keys()
                data = [[row[col] for col in headers] for row in data]
                data.insert(0, headers)
                fromobj = True
            if hasattr(data[0], '__getitem__'):
                valid_data = True
        assert valid_data is True, "ExcelResponse requires a sequence of sequences"

        self.output = StringIO.StringIO()
        # Excel has a limit on number of rows; if we have more than that, make a csv
        use_xls = False
        if len(data) <= 65536 and force_csv is not True:
            try:
                import xlwt
            except ImportError:
                # xlwt doesn't exist; fall back to csv
                pass
            else:
                use_xls = True
        if use_xls:
            book = xlwt.Workbook(encoding=self.encoding)
            self.sheet = book.add_sheet('Sheet 1')
            self.styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'default': xlwt.Style.default_style}

            self.rowx = 0
            self.colx = 0
            if(fromobj == True):
                self.WriteExcel(data)
            else:
                    self.header_style = xlwt.easyxf("font: bold on , colour_index 4;")
                    for  row in (data[0]):
                         cell_style = self.styles['default']
                         self.sheet.write(self.rowx, self.colx, row, style=self.header_style)
                         self.colx = self.colx + 1
                    self.rowx = 1
                    self.WriteExcel(data[1])
            book.save(self.output)
            mimetype = 'application/vnd.ms-excel'
            file_ext = 'xls'
        else:
            if(fromobj == True):
                self.WriteCSV(data)
            else:
                out_row = []
                for row in data[0]:
                    out_row.append(row.replace('"', '""'))
                self.output.write('\n"%s"' %
                                 '","'.join(out_row))
                self.WriteCSV(data[1])
            mimetype = 'text/csv'
            file_ext = 'csv'
        self.output.seek(0)
        super(ExcelResponse, self).__init__(content=self.output.getvalue(),
                                            mimetype=mimetype)
        self['Content-Disposition'] = 'attachment;filename="%s.%s"' % \
            (output_name.replace('"', '\"'), file_ext)

    def WriteExcel(self,datalist):
        self.colx = 0
        for  row in (datalist):
            for  value in (row):
                if isinstance(value, datetime.datetime):
                    cell_style = self.styles['datetime']
                elif isinstance(value, datetime.date):
                    cell_style = self.styles['date']
                elif isinstance(value, datetime.time):
                    cell_style = self.styles['time']
                else:
                    cell_style = self.styles['default']
                self.sheet.write(self.rowx, self.colx, value, style=cell_style)
                self.colx = self.colx + 1
            self.rowx = self.rowx + 1
            self.colx = 0


    def WriteCSV(self,datalist):
        for row in datalist:
            out_row = []
            for value in row:
                if not isinstance(value, basestring):
                    value = unicode(value)
                value = value.encode(self.encoding)
                out_row.append(value.replace('"', '""'))
            self.output.write('\n"%s"' %  '","'.join(out_row))

