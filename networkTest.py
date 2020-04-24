import subprocess
import time
import logging

failureTresh = 100
testIP = '8.8.8.8'


def pingTest(networkInfo):
    logging.info("Running Ping Test")

    command = 'ping ' + networkInfo._testIP + ' -n ' + str(networkInfo._pingCount)

    logging.info(command)

    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
    output = str(proc.communicate()[0])

    logging.info(output)

    try:
        maxStart = (output.find('Maximum ='))
        maxEnd = (output.index('ms,', output.find('Maximum =')))
        maxPingValue = (output[(maxStart + 10):maxEnd])
    except:
        logging.warning("Problem Detected")

    if output.find("Request timed out.") != -1:
        logging.info("Request timed out Detected.")
        flag = True
    elif int(maxPingValue) > networkInfo._failureTresh:
        logging.info("Latency of: " + str(maxPingValue) + "ms Detected. This is over the Threshold of: " + str(
            networkInfo._failureTresh) + "ms")
        flag = True
    else:
        flag = False

    return flag


class networkInfo:

    def __init__(self, pingCount=1, googleDNS='8.8.8.8', failureTresh=100):
        self._testIP = googleDNS
        self._failureTresh = failureTresh
        self._pingCount = pingCount

    def set_pingCount(self, x):
        self._pingCount = x

    def set_failureTresh(self, x):
        self._failureTresh = x

    def set_testIP(self, x):
        self._testIP = x

    def get_pingCount(self):
        return self._pingCount

    def get_failureTresh(self):
        return self._failureTresh

    def get_testIP(self):
        return self._testIP


def traceRoute(networkInfo):
    logging.warning("Running Trace Route. Please Wait.")

    command = 'tracert -d ' + networkInfo._testIP
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
    output = str(proc.communicate()[0])

    logging.warning(output)





logging.basicConfig(filename='Output.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(funcName)s %(message)s')
networkTest = networkInfo()

while True:
    logging.info("Starting Network Testing")

    if pingTest(networkTest) == True:
        traceRoute(networkTest)
    else:
        time.sleep(1)
