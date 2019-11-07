# python:3-alpine is much smaller than python:3 for the runtime container.
# When using python:3, only the pip install line is needed in the RUN command. 
# Alpine requires dependencies to be installed.
FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt keyhole.py ./

# Extra packages are needed for building bcrypt and cryptography 
RUN apk --no-cache add --virtual \
    build-deps \
    build-base \
    # For bcrypt
    libffi-dev \ 
    # For cryptography 
    openssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    # Remove the installed packages that aren't needed anymore 
    apk del build-deps

CMD ["python", "./keyhole.py"]

