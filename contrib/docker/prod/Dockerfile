FROM tipboard-base
MAINTAINER PyLabs pylabs@allegrogroup.com

RUN /opt/tipboard/bin/pip install tipboard
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]
