# Build stage for compiling audiowaveform
FROM debian:bullseye as audiowaveform-builder

# Install the necessary packages for building audiowaveform
RUN apt-get update && apt-get install -y \
    git make cmake gcc g++ libmad0-dev \
    libid3tag0-dev libsndfile1-dev libgd-dev \
    libboost-filesystem-dev libboost-program-options-dev libboost-regex-dev \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone audiowaveform repository and compile
RUN git clone https://github.com/bbc/audiowaveform.git && \
    wget https://github.com/google/googletest/archive/release-1.12.1.tar.gz && \
    tar xzf release-1.12.1.tar.gz && \
    ln -s googletest-release-1.12.1 googletest && \
    mv googletest audiowaveform/ && \
    mkdir -p audiowaveform/build && \ 
    cd audiowaveform/build && \
    cmake .. -D ENABLE_TESTS=0 -D BUILD_STATIC=1 && \
    make && \
    make install

# Final stage for setting up the Python environment
FROM python:3.10.4-slim-bullseye as final-stage

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the compiled audiowaveform binary
COPY --from=audiowaveform-builder /usr/local/bin/audiowaveform /usr/local/bin/

WORKDIR /code

# Copy Python dependencies
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




 # Dockerfile.web-app

# /Users/mshittu/programming-projects/python/django/media-be/Dockerfile

