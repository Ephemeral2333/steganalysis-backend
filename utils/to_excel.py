# model.py
from io import BytesIO
import pandas as pd


def to_excel(sql_return):
    df = pd.DataFrame(sql_return)
    f = BytesIO()  # 内存文件
    writer = pd.ExcelWriter(f, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    writer.close()
    f.seek(0)
    return f

