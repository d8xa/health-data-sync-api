# Stage 1: Build environment
FROM continuumio/miniconda3:latest AS builder
WORKDIR /build

# Copy the necessary build files
COPY environment.yml .

# Create the environment
RUN conda env create -f environment.yml && \
    conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n flask-env -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


##############################
# Stage 2: Runtime environment
FROM debian:buster AS runtime

# Set the working directory
WORKDIR /code

# Copy the built environment from the previous stage
COPY --from=builder /venv /venv

# Activate the environment
SHELL ["/bin/bash", "-c"]

# Copy the necessary runtime files
COPY app ./app
COPY run.py .
COPY credentials.json .

EXPOSE 5000

# Set the entry point
ENTRYPOINT source /venv/bin/activate && \
    gunicorn -w 4 --bind 0.0.0.0:5000 --log-level debug --capture-output run:app