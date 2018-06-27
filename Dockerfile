FROM python:3.6.5

WORKDIR /usr/src/matrix

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ARG script
ARG mongodb_uri
ARG api_url

ENV SCRIPT "${script}.py"
ENV MONGODB_URI ${mongodb_uri}
ENV API_URL ${api_url}

COPY . .

CMD python ${SCRIPT}
