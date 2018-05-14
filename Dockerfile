FROM python:3.6.5

WORKDIR /usr/src/matrix

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG script
ENV SCRIPT "${script}.py"

COPY . .

CMD python ${SCRIPT}
