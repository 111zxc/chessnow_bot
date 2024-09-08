FROM python:3.10

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/111zxc/chessnow_bot.git /app

WORKDIR /app

RUN python -m venv env

RUN /bin/bash -c "source env/bin/activate && pip install -r requirements.txt"

CMD ["/bin/bash", "-c", "source env/bin/activate && python main.py"]