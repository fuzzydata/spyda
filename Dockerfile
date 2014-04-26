# Docker Image for spyda

FROM prologic/crux-python
MAINTAINER James Mills <prologic@shortcircuitnet.au>

# Add Source
ADD . /usr/src/spyda

# Build and Install
RUN cd /usr/src/spyda && python setup.py install
