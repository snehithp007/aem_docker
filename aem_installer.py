import sys
import socket
import time
import subprocess
import shutil
from urllib import urlencode, quote
from time import sleep
from optparse import OptionParser

# Argument definition
usage = "usage: %prog [options] arg"
parser = OptionParser(usage)

# receive options for AEM installation from docker file
parser.add_option("-i", "--install_file", dest="filename", help="AEM install file")
parser.add_option("-r", "--runmode", dest="runmode", help="Run mode for the installation")
parser.add_option("-p", "--port", dest="port", help="Port for instance")

options, args = parser.parse_args()
option_dic = vars(options)
file_name = option_dic.setdefault('filename', 'cq-publish-4503.jar')
runmode = option_dic.setdefault('runmode', 'publish')
port = option_dic.setdefault('port', '4503')

def get_formatted_time():
  return time.strftime("%Y-%m-%d %H:%M:%S")

def log(message):
  print("%s: %s" % (get_formatted_time(), message))
  sys.stdout.flush()

# Copy out parameters
log("aem_installer.py called with params: %s" % option_dic)

def start_aem_server(aem_jar_file_name, port, runmode):
  arguments = "file: %s, port: %s, runmode: %s" % (aem_jar_file_name, port, runmode)
  log("Starting AEM with arguments: %s" % arguments)

  # Waits for connection on LISTENER_PORT, and then checks that the returned
  # success message has been received.
  LISTENER_PORT = 50007
  # Customize the install process with custom arguments as required
  install_process = subprocess.Popen(['java', '-Xms8g', '-Xmx8g', '-Djava.awt.headless=true',
    '-jar', aem_jar_file_name, '-listener-port', str(LISTENER_PORT), '-r', runmode, '-p', port, '-nofork'])

  # Starting listener
  HOST = ''
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  attempts = 0
  while True:
    attempts = attempts + 1
    log("Trying to start AEM (attempt %s)" % attempts)
    try:
      s.bind((HOST, LISTENER_PORT))
      break
    except Exception as error:
      log("Failed starting server (attempt %s): %s" % (attempts, error))
      if attempts >= 3:
        helpers.log("Tried starting server 3 times. Now exiting...")
        sys.exit(1)
      sleep(20)

  s.listen(1)
  conn, addr = s.accept()

  str_result = ""
  while True:
    data = conn.recv(1024)
    if not data:
      log("Failed starting AEM; %s" % arguments)
      install_process.kill()
      sys.exit(1)
    else:
      str_result = str_result + str(data).strip()
      if str_result == 'started':
        log("AEM started; %s" % arguments)
        break

  conn.close()
  s.close()
  return install_process.pid

log("Start installing packages")
start_aem_server(file_name, port, runmode)

sys.exit(0)