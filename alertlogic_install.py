import os.path
import urllib2
import sys
import platform
import re
import subprocess

## Written by timothy.hutz@thinktank.net for thinktank

SYSTEM_PLATFORM = sys.platform
SYSTEM_ARCH = platform.machine()
PYTHON_VERSION = sys.version
ALERT_LOGIC_KEY = sys.argv[1]
ALERT_LOGIC_APPLIANCE = sys.argv[2]
ALERT_LOGIC_RPM_INSTALL_CMD = '/bin/rpm -U'

    ##ensure arg 1 KEY and arg 2 VPC APPLIANCE are set correct
if re.match(r".*", ALERT_LOGIC_KEY):
    pass
else:
    print "Please enter your Alert Logic Key as the first paramater"
    exit(105)
if re.match(r"^(\d{1,9})\.(\d{1,9})\.(\d{1,9})\.(\d{1,9})$", ALERT_LOGIC_APPLIANCE):
    pass
else:
    print "Alert Logic Appliance IP addres does not appeard to be entered  correctly"
    print "It should be the second passed paramater"
    exit(104)

    ## This inspects the system for compatibility.
if re.match('linux', SYSTEM_PLATFORM):
    pass
else:
    print SYSTEM_PLATFORM, 'not currently compatible with this installer'
    exit(100)

    ## This inspects PYTHON_VERSION for correct python.
if re.match('2\.7', PYTHON_VERSION):
    pass
else:
    print PYTHON_VERSION,'not compatible with this installer'
    exit(101)

    ## Sets the SYSTEM_ARCH to pull the correct rpm and ensure on redhat.
if re.match('.86_32', SYSTEM_ARCH):
    ALERT_LOGIC_RPM_URL = 'https://scc.alertlogic.net/software/al-agent-LATEST-1.i386.rpm'
    ALERT_LOGIC_RPM_FILENAME = 'al-agent-LATEST-1.i386.rpm'
if re.match('.86_64', SYSTEM_ARCH):
    ALERT_LOGIC_RPM_URL = 'https://scc.alertlogic.net/software/al-agent-LATEST-1.x86_64.rpm'
    ALERT_LOGIC_RPM_FILENAME = 'al-agent-LATEST-1.x86_64.rpm'
else:
    print SYSTEM_ARCH, "dose not match anything compatible"
    exit(102)

    ## After Enviroment configed. Grabbing and installing agent
DOWNLOAD_FILE = urllib2.urlopen(ALERT_LOGIC_RPM_URL)
print "downloading " + ALERT_LOGIC_RPM_URL
with open(os.path.basename(ALERT_LOGIC_RPM_FILENAME), 'wb') as file:
    file.write(DOWNLOAD_FILE.read())

subprocess.call("sudo {} {}".format(ALERT_LOGIC_RPM_INSTALL_CMD,ALERT_LOGIC_RPM_FILENAME), shell=True)

    ## Now configure the agent.
subprocess.call('/usr/bin/sudo /etc/init.d/al-agent configure --host {}'.format(ALERT_LOGIC_APPLIANCE), shell=True)
subprocess.call('/usr/bin/sudo /etc/init.d/al-agent provision --key {}'.format(ALERT_LOGIC_KEY), shell=True)
subprocess.call('/usr/bin/sudo /etc/init.d/al-agent start', shell=True)
