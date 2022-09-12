FROM amazon/aws-glue-libs:glue_libs_3.0.0_image_01 
USER root
RUN yes | yum install postgresql-devel gcc python3-devel.x86_64 musl-devel
WORKDIR /opt
ADD ./oracle-instantclient-basic-21.6.0.0.0-1.el8.x86_64.rpm  /opt
RUN yes | yum install oracle-instantclient-basic-21.6.0.0.0-1.el8.x86_64.rpm
RUN /bin/sh -c pip3 install --upgrade pip && pip3 install psycopg2==2.9.3 && pip3 install aws-psycopg2==1.2.1 && pip3 install boto3==1.23.6 && pip3 install cx-Oracle==8.3.0
