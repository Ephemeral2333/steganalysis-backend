import os
import random
import shlex
import time

import pandas as pd
from flask import Blueprint, jsonify
from flask import request
import subprocess

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/train', methods=['GET'])
def get_training_data():
    file_path = 'file/train.csv'
    sheet_name = 'Sheet1'
    # 使用 pandas 读取 Excel 数据
    dataframe = pd.read_excel(file_path, sheet_name=sheet_name)

    # 我们需要的是前三列，所以这里获取前三列的列名
    target_column_names = dataframe.columns[:3]

    # 将每一列的数据转换为列表，并存储在一个字典中
    columns_data = {}
    for column_name in target_column_names:
        # 将列的数据转换为列表（排除空值）
        columns_data[column_name] = dataframe[column_name].dropna().tolist()

    # 返回列的数据作为 JSON
    return jsonify(columns_data)
