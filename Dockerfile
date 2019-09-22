FROM ubuntu

LABEL maintainer="Dynulo"

RUN dpkg --add-architecture i386
RUN apt-get update
RUN apt-get install wget python3 lib32gcc1 libstdc++6 libstdc++6:i386 libtbb2:i386 libtbb2 -y
RUN apt-get clean
RUN rm /var/lib/apt/lists/* -r

RUN mkdir /arma3

ENV ARMA_CONFIG=main.cfg
ENV ARMA_PROFILE=main
ENV ARMA_WORLD=empty

EXPOSE 2301/udp
EXPOSE 2302/udp
EXPOSE 2303/udp
EXPOSE 2304/udp
EXPOSE 2305/udp

ADD steamcmd /steamcmd
ADD launch.py /launch.py

RUN chmod +x /steamcmd/steamcmd.sh

WORKDIR /arma3

STOPSIGNAL SIGINT

CMD ["python3","/launch.py"]