from flask import Flask, render_template, jsonify, request
import json
from flask_cors import CORS
import numpy as np
import tifffile as tiff
import netCDF4 as nc
from scipy.ndimage import zoom
import random
'''
Author: DC
Date: 2025-01-05 10:27:16
LastEditTime: 2025-01-05 11:03:01
LastEditors: DC
Description: 
FilePath: \森林圈层展示数据\flask1.py
Never lose my passion
108.019413,20.007713
111.013573,18.012854

109.019766,19.408213
110.15465,18.73582
'''
app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    data = {'key': 'value'}
    return render_template('index.html', data=data)

@app.route('/api/data',methods=['get'])
# @CrossOrigin()
def post_data():
    # 返回json数据的方法
    data = {
        "name":"zhangsan",
        "age":18
    }
    # 第二种 jsonify帮助转为json数据，并设置响应头 Content-Type 为 application/json
    return jsonify(data)

@app.route('/api/tif1',methods=['get'])
# @CrossOrigin()
def post_data1():
    tif_file_path = r'D:\A透视地球\森林圈层展示数据\forest_type.tif'

    # Read the TIFF file
    image = tiff.imread(tif_file_path)
    x=np.linspace(109.019766,110.15465,2268)
    y=np.linspace(19.408213,18.73582,2243)
    data = {
        "x": x.tolist(),
        "y": y.tolist(),
        'data':image.tolist()
    }
    return jsonify(data)

@app.route('/api/nc1',methods=['get'])
# @CrossOrigin()
def post_data2():
    file_path = r'D:\FY4A-_AGRI--_N_DISK_1047E_L2-_CTH-_MULT_NOM_20190807070000_20190807071459_4000M_V0001.NC'
    dataset = nc.Dataset(file_path, 'r')
    cth_data_array = np.array(dataset['CTH'])
    zoom_factors = (144 / cth_data_array.shape[0], 73 / cth_data_array.shape[1])
    resized_cth_data = zoom(cth_data_array, zoom_factors, order=1)
    normalized_cth_data = (resized_cth_data - np.min(resized_cth_data)) / (
                np.max(resized_cth_data) - np.min(resized_cth_data)) +random.randint(-200,200)/100

    data = {
        'data':normalized_cth_data.tolist()
    }



    return jsonify(data)


@app.route('/api/wind1',methods=['get'])
# @CrossOrigin()
def post_data3():
    file_path = r'D:\FY4A-_AGRI--_N_DISK_1047E_L2-_CTH-_MULT_NOM_20190807070000_20190807071459_4000M_V0001.NC'
    dataset = nc.Dataset(file_path, 'r')
    cth_data_array = np.array(dataset['CTH'])
    zoom_factors = (144 / cth_data_array.shape[0], 73 / cth_data_array.shape[1])
    resized_cth_data = zoom(cth_data_array, zoom_factors, order=1)
    normalized_cth_data = (resized_cth_data - np.min(resized_cth_data)) / (
                np.max(resized_cth_data) - np.min(resized_cth_data)) +random.randint(-200,200)/100

    data = {
        'data':normalized_cth_data.tolist()
    }



    return jsonify(data)


@app.route('/MakeCanvasParticles',methods=['get'])
# @CrossOrigin()
def MakeCanvasParticles():
    # -209.5271, 44.536456
    # -96.641286, -13.240786
    lat=[]
    lng=[]
    for i in range(0,canvasParticlesLen):
        lat.append(random.uniform(-209.5271,-96.641286))
        lng.append(random.uniform(44.536456,-13.240786))
    data = {
        'lat':lat,
        'lng':lng
    }



    return jsonify(data)

@app.route('/GetCanvasParticlesLen', methods=['POST'])
def process_data():
    data = request.get_json()
    global canvasParticlesLen
    canvasParticlesLen = data['canvas1']

    # age = data['age']

    # 处理数据的逻辑代码
    # print(name)

    response = {'message': 'Data received successfully'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)