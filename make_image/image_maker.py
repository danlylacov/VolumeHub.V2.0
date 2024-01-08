import os
import time

from dotenv import load_dotenv
from html2image import Html2Image
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import requests
from PIL import Image


class ImageMaker():

    def __init__(self, figi: str, action_name: str, ticket: str, price: str, volume_lots: str, volume_rub: str,
                 today_growth: str,
                 growth: str, buy: str, sell: str, name_of_logo_photo: str = ''):
        self._create_image(action_name, ticket, price, volume_lots, volume_rub, today_growth, growth, buy, sell)
        self._create_chart(figi)
        self._overlay_and_resize_images('background.jpg', 'plot.png', 'result.png')


    def _create_image(self, action_name: str, ticket: str, price: str, volume_lots: str, volume_rub: str,
                      today_growth: str,
                      growth: str, buy: str, sell: str, name_of_logo_photo: str = ''):
        hti = Html2Image(size=(515, 650))

        html = f"""
                <!DOCTYPE html>
        <html>
        <head>
            <title>lox Den</title>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>

            <i>
                <table border="0" align="center" width="500px">
                    <TR align="left" height="50px">
                        <th rowspan="2" height="70px" width="90px">
                            <img src="{name_of_logo_photo}" height="60px" width="60px"> 
                        </th>
                        <th style="vertical-align: bottom;">
                            <h1 class="text">{action_name}</h1>
                        </th>
                        <th width="215px" style="vertical-align: bottom;">
                            <h3 class="sm_tx">Текущая цена:</h3>
                        </th>
                    </TR>
                    <TR align="left">
                        <th width="215px">
                            <h3 class="sm_tx">{ticket}</h3>
                        </th>
                        <th width="215px">
                            <h3 class="text">{price} ₽</h3>
                        </th>
                    </TR>
                </table>

                <br><br>

                <table border="0" align="center" width="500px"> 
                    <TR align="left">
                        <th width="250px">
                            <h3 class="sm_tx">Аномальный объем:</h3>
                        </th>
                        <th colspan="2">
                            <h3 class="sm_tx">Изменение цены:</h3>
                        </th>
                    </TR>
                    <TR align="left">
                        <th rowspan="2" width="250px">
                            <h1 class="text">{volume_lots} лот</h1>
                        </th>
                        <th width="105px">
                            <h3 class="sm_tx">сегодня:</h3>
                        </th>
                        <th colspan="2">
                            <h3 class="text">{today_growth}%</h3>
                        </th>
                    </TR>
                    <tr align="left">
                        <th width="105px">
                            <h3 class="sm_tx">на объеме:</h3>
                        </th>
                        <th colspan="2">
                            <h3 class="text">{growth}%</h3>
                        </th>
                    </tr>
                </table>

                <table border="0" align="center" width="500px">
                    <TR align="left">
                        <th width="155px"> 
                            <h3 class="sm_tx">Объем в рублях:</h3>
                        </th>
                        <th colspan="3">
                            <h3 class="sm_tx">{volume_rub} млн</h3>
                        </th>
                    </TR>    
                </table>

                <table border="0" align="center" width="500px">
                    <TR align="left">
                        <th width="80px">
                            <h4 class="sm_tx">Покупка:</h4>
                        </th>
                        <th colspan="3">
                            <h4 class="text">{buy}%</h4>  
                        </th>
                    </TR> 
                    <TR align="left">
                        <th width="80px">
                            <h4 class="sm_tx">Продажа:</h4>   
                        </th>
                        <th colspan="3">
                            <h4 class="text">{sell}%</h4>  
                        </th>
                    </TR> 
                </table>

            </i> 
            <br>

            <table border="0" align="center" width="500px">
                <TR align="left">
                    <th>
                        <img src="my_plot.png" height="252px" width="420px"> 
                    </th>
                </TR> 
            </table>

        </body>
        </html>
        """

        css = """@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@200&display=swap');

        body {
            weight: 600px; height: 700px;
            font-family: 'Raleway', sans-serif;
            text-align: center;
            font-size: 16px;
            margin-top: 50px;
            margin-bottom: 50px;
            color: #fff; 
            background: #1A1B26;

            no-repeat;
            margin: 50px;


        }

        .text {
            border: 0px;
            display: flex;

            align-items: flex-end;
            margin: 0px;
            padding: 0px;
        }
        .sm_tx{
            font-weight: lighter;
            border: 0px;
            display: flex;
            align-items: flex-end;
            margin: 0px;
            padding: 0px;
        }

        .green {
            color: green;
          }

          .red {
            color: red;
          }"""

        hti.screenshot(html_str=html, css_str=css, save_as='background.jpg')


    def _create_chart(self, figi: str):
        load_dotenv()
        API_ADRESS = os.environ['API_ADRESS']
        stocks = list(requests.get(f'{API_ADRESS}/get_hour_data/{figi}').json())

        stock_prices = pd.DataFrame({'open': [float(stocks[i][1]) for i in range(60)],
                                     'close': [float(stocks[i][4]) for i in range(60)],
                                     'high': [float(stocks[i][2]) for i in range(60)],
                                     'low': [float(stocks[i][3]) for i in range(60)]},
                                    index=pd.date_range(str(stocks[0][-1]).split('+')[0], periods=60, freq="1min"))

        # Создание фигуры и оси
        fig, ax = plt.subplots(figsize=(10, 6), facecolor=(0x1A / 255, 0x1B / 255, 0x26 / 255))

        # Установка цвета фона графика (под свечами)
        ax.set_facecolor((0x1A / 255, 0x1B / 255, 0x26 / 255))

        up = stock_prices[stock_prices.close >= stock_prices.open]
        down = stock_prices[stock_prices.close < stock_prices.open]

        col2 = (1, 0, 0)  # Красный
        col1 = (0, 1, 0)  # Зеленый

        width = 0.0005
        width2 = 0.0001

        plt.bar(up.index, up.close - up.open, width, bottom=up.open, color=col1)
        plt.bar(up.index, up.high - up.close, width2, bottom=up.close, color=col1)
        plt.bar(up.index, up.low - up.open, width2, bottom=up.open, color=col1)

        plt.bar(down.index, down.close - down.open, width, bottom=down.open, color=col2)
        plt.bar(down.index, down.high - down.open, width2, bottom=down.open, color=col2)
        plt.bar(down.index, down.low - down.close, width2, bottom=down.close, color=col2)

        plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
        plt.xticks(rotation=0, ha='center')

        # Добавление сетки
        plt.grid(True, linestyle='--', alpha=0.7)

        # Установка цвета меток на черный
        plt.tick_params(axis='both', colors='white')

        # Установка цвета осей на черный
        plt.gca().spines['bottom'].set_color('white')
        plt.gca().spines['top'].set_color('white')
        plt.gca().spines['right'].set_color('white')
        plt.gca().spines['left'].set_color('white')

        plt.savefig('plot.png', format='png', bbox_inches='tight')

    def _overlay_and_resize_images(self, background_path, overlay_path, output_path):
        background = Image.open(background_path)
        overlay = Image.open(overlay_path)

        overlay = overlay.convert("RGBA")

        overlay = overlay.resize((440, 280), Image.LANCZOS)

        background.paste(overlay, (40, 355), overlay)

        background.save(output_path)



