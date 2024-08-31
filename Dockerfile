FROM jupyter/scipy-notebook

# -- Install dependencies

# RUN pip install ...

RUN mkdir /home/jovyan/app

WORKDIR /home/jovyan/app
