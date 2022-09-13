FROM python:3.10.6-slim

RUN pip install jupyterlab notebook jupyter_http_over_ws &&\
    jupyter serverextension enable --py jupyter_http_over_ws

EXPOSE 8888

# disable authentication since everything is over ssh
ENTRYPOINT ["jupyter", "notebook", "--NotebookApp.allow_origin='https://colab.research.google.com'", "--NotebookApp.token=''", "--NotebookApp.password=''", "--allow-root", "--port", "8888", "--NotebookApp.port_retries=0", "--ip", "0.0.0.0"]