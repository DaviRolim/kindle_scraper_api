FROM public.ecr.aws/lambda/python@sha256:2203844d7263f9c38a7f03f25bbb181772e93abc944de2b26ccca1689e1dde55 as build

FROM public.ecr.aws/lambda/python@sha256:2203844d7263f9c38a7f03f25bbb181772e93abc944de2b26ccca1689e1dde55
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY user_streak.py ./
COPY freeadwise-0324a980ef62.json ./
CMD [ "user_streak.handler" ]
