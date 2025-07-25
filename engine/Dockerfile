FROM python:3.12.0

WORKDIR /

# Default configuration
ENV FLASK_APP=app

# Host settings
ENV HOST=0.0.0.0
ENV PORT=8080

# Datetime settings
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Prepare server structure
COPY . /engine

# Install app dependencies
RUN pip install --upgrade pip
RUN pip install -r /engine/requirements.txt

# Clean-up IDE files from local build
RUN python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
RUN python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

# Entrypoint for application start
RUN chmod +x /engine/entrypoint.sh
RUN mv /engine/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]