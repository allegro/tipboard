FROM tipboard-base
MAINTAINER PyLabs pylabs@allegrogroup.com

# install tipboard with -e flag to get proper egg-link to mounted source code
RUN apt-get install -y git
RUN git clone git://github.com/allegro/tipboard.git /root/src/tipboard
RUN /opt/tipboard/bin/pip install -e /root/src/tipboard

VOLUME /root/src
