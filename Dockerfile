FROM chenaoki/nb_basic:latest

MAINTAINER chenaoki <chenaoki@gmail.com>

USER root

##########################

WORKDIR $HOME
#RUN apt-get install -y cuda

##########################

RUN pip3 install --upgrade pip setuptools
RUN pip3 install scipy
RUN pip3 install numba

##########################

#RUN mkdir -p $NOTEBOOK_HOME 
#CMD ["sh", "-c", "/bin/bash"]
CMD ["sh", "-c", "jupyter notebook --allow-root > $NOTEBOOK_HOME/log.txt 2>&1"]
