# Dockerfile for binder
# References:
# - https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html
# - https://github.com/sagemath/sage-binder-env/blob/master/Dockerfile

FROM sagemath/sagemath:9.0-py3
RUN sudo apt-get update
RUN sage -pip install jupyterlab

# Copy the contents of the repo in ${HOME}
COPY --chown=sage:sage . ${HOME}
