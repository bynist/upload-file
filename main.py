from fastapi import FastAPI, UploadFile, File
from get_top_product_from_file import get_top_product_from_file_

app = FastAPI()


@app.post('/import')
def get_top_product_from_file(csv_file: UploadFile = File(...)):
    return get_top_product_from_file_(csv_file)
