FROM python:buster
COPY ./app /app
COPY ./testPictures /app/testPictures
COPY ./geoCacheDb /app/geoCacheDb

RUN pip install requests
RUN pip install Pillow
RUN pip install pickledb
RUN pip install pandas

CMD python /app/order.py