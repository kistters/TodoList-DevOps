FROM python:3.6

ADD ./app /code

RUN pip install -r \ 
		requirements.txt