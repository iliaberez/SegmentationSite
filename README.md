## Пункт 1. Установка фреймворка Django.
Руководство: https://metanit.com/python/django/1.2.php
Создавать виртуальную машину не обязательно, можно работать и с глобальной версией Python на вашем ПК.
## Пункт 2. Установка библиотек.
```
pip install keras, uuid, nibabel, numpy, base64, matplotlib, django-bootstrap4
```
## Пункт 2.1 Перенос вычислений на видеокарту.
Руководство: https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781
Вам нужно установить Cuda Toolkit с оф. сайта Nvidia, cuDNN, tensorflow для GPU, а также указать переменные среды в Windows для них.
```
pip3 install --upgrade tensorflow-gpu
```
## Пункт 3. Скачивание весов нейронной сети.
GitHub не позволяет хранить большие файлы в репозитории, поэтому придётся скачивать .hdf5 с Google Drive
https://drive.google.com/file/d/1k-lo9uXzhIfdOrKf2EnXa7N6_wvwhBT7/view?usp=sharing
Скаченный файл нужно разместить в каталоге 
```
/MySite/static/
```
## Пункт 4. Выполнение миграций и запуск проекта.
Миграции, запускать командs из терминала в основном каталоге где лежит файл manage.py
Создание миграции:
```
python manage.py makemigrations DiplomaSite
```
Выполнение миграции:
```
python manage.py migrate DiplomaSite
```
Запуск проекта:
```
python manage.py runserver
```
Для отслеживания работы сайта http://127.0.0.1:8000/
## Пункт 5. Датасет.
https://drive.google.com/drive/folders/1nU9pa69pY5W-Lm7FYH55Idbm7A8bpF5m?usp=sharing
Датасет состит из файлов NIFTI формата, в папке image лежат изображения компьютерной томографии.
В других папках находяться маски для каждой доли соответствующего оригинального изображения.
В файле intervals.txt находятся интервалы размеченных данных.

## Пункт 6. Работа с нейронной сетью.
https://colab.research.google.com/drive/1OCTUgEyU7TOve_PnTc3viHiUpS5vTQKx?usp=sharing

## Пункт 7. Рекомендации.
Сгенерируйте свой секретный ключ для обеспечения безопасности
https://djecrety.ir/
Замените в файле setting.py в папке mysite
