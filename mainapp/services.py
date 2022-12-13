import csv

from django.http import HttpResponse


class CSVStream:
    """ Response CSV file. """

    @staticmethod
    def export_csv_file(request, queryset, csv_rows: int, delimiter: str, quotechar: str):
        """ Data from model --> file.csv """
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="export.csv"'},
        )

        field_names = [column[0] for column in queryset.values_list('column_name')]
        writer = csv.writer(response, delimiter=delimiter, quotechar=quotechar)
        # First row with header information.
        writer.writerow(field_names)

        # Write data rows.
        print(queryset)
        for row in range(0, int(csv_rows)):
            writer.writerow((str(i) for i in field_names))
        return response
