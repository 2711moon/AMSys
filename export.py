from flask import Blueprint, make_response
import csv
import io
import xlsxwriter
from models import assets_collection

export_bp = Blueprint('export', __name__)

@export_bp.route('/csv')
def export_csv():
    assets = list(assets_collection.find())

    headers = ['Asset ID', 'Name', 'Category', 'Owner', 'Status']
    output = []

    for asset in assets:
        output.append([
            str(asset.get('_id')),
            asset.get('name', ''),
            asset.get('category', ''),
            asset.get('owner', ''),
            asset.get('status', '')
        ])

    response = make_response()
    response.headers["Content-Disposition"] = "attachment; filename=assets.csv"
    response.headers["Content-type"] = "text/csv"

    writer = csv.writer(response.stream)
    writer.writerow(headers)
    writer.writerows(output)

    return response

@export_bp.route('/excel')
def export_excel():
    assets = list(assets_collection.find())

    headers = ['Asset ID', 'Name', 'Category', 'Owner', 'Status']

    # Create an in-memory output file for the Excel file
    output = io.BytesIO()
    
    # Create a workbook and worksheet
    import xlsxwriter
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Assets")

    # Write header row
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write asset data rows
    for row, asset in enumerate(assets, start=1):
        worksheet.write(row, 0, str(asset.get('_id')))
        worksheet.write(row, 1, asset.get('name', ''))
        worksheet.write(row, 2, asset.get('category', ''))
        worksheet.write(row, 3, asset.get('owner', ''))
        worksheet.write(row, 4, asset.get('status', ''))

    # Finalize the workbook
    workbook.close()
    output.seek(0)

    # Create response
    response = make_response(output.read())
    response.headers["Content-Disposition"] = "attachment; filename=assets.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response

