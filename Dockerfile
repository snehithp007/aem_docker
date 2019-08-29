FROM centos:7

# Install packages
# ld-linux.so.2, glibc.i686 and libuuid.i686 are added to enable XMP extraction and write-back on 64-bit RedHat Linux
# See https://helpx.adobe.com/experience-manager/kb/enable-xmp-write-back-64-bit-redhat.html.
RUN yum -y install epel-release && yum clean all
RUN yum -y --enablerepo=centosplus update \
    && yum install -y \
      tar \
      wget \
      java-1.8.0-openjdk \
      libselinux-devel \
      epel-release \
      ipython3 \
      python-pip \
      python-psutil \
      python-pycurl \
      ld-linux.so.2 \
      glibc.i686 \
      libuuid.i686 \
    && yum clean all \
    && rm -rf /var/cache/yum

# Copy required build media
COPY ./cq-quickstart-6.3.0.jar /opt/aem/cq-quickstart-6.3.0.jar
COPY ./license.properties /opt/aem/license.properties
COPY ./aem_installer.py /opt/aem/aem_installer.py

# Extracting AEM without installation allows custom steps that could be performed while installing
WORKDIR /opt/aem

# Ensure that docker has atleast 8G memory allocated
RUN java -Djava.awt.headless=true -Xms8g -Xmx8g -jar cq-quickstart-6.3.0.jar -unpack

# Installing using phython handler for Author mode
RUN python aem_installer.py -i cq-quickstart-6.3.0.jar -r author,nosamplecontent,local -p 4502

EXPOSE 4502
CMD java -Xms4g -Xmx4g -Djava.awt.headless=true -Xdebug -Xnoagent -agentlib:jdwp=transport=dt_socket,address=30303,server=y,suspend=n -jar cq-quickstart-6.3.0.jar -p 4502 -r publish,nosamplecontent,local -v -nofork