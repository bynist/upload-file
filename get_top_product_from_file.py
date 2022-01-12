import codecs
import csv

from fastapi import UploadFile, HTTPException
from starlette import status
from starlette.responses import JSONResponse


def get_top_product_from_file_(csv_file: UploadFile):

    if csv_file.content_type != 'text/csv':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unacceptable file type")

    data = get_data_from_csv_file(file_name=csv_file)

    top_product_dict = max(data, key=lambda x: x['customer_average_rating'])

    result = {
        "top_product": top_product_dict["products_name"] if top_product_dict['products_name'] is not None else "unknown",
        "product_rating": top_product_dict["customer_average_rating"] if top_product_dict['customer_average_rating'] is not None else "unknown",
    }

    filename = "top_product.json"
    response = JSONResponse(content=result)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


def get_data_from_csv_file(file_name: UploadFile):
    file_dict_reader = csv.DictReader(codecs.iterdecode(file_name.file, 'utf-8'))
    data = []
    try:
        for row in file_dict_reader:
            row_dict = get_values(data_row=dict(row))
            if row_dict:
                data.append(row_dict)
    except ValueError as ve:
        print(f'---- ValueError Raised {ve}')
    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="empty file")
    return data


def get_values(data_row: dict):
    # prepare valid data
    id = data_row.get('id', 1)
    products_name = data_row.get('products_name', None)
    customer_average_rating = data_row.get('customer_average_rating', None)
    if products_name is not None and customer_average_rating is not None:
        return {
            "id": id,
            "products_name": str(products_name),
            "customer_average_rating": float(customer_average_rating)
        }
    else:
        raise ValueError('Unable to get values')
