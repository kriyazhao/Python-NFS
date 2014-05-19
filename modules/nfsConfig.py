#==========================================================================================================================
# nfsConfig class for NFS configurations, which is server-side only
class nfsConfig:
    
    # initialize the configuration class and load configuration from a specified section
    def __init__(self, conFile = None, conSection = None):
        if conFile != None:
            self.fileConfig = conFile
        else:
            self.fileConfig = 'fileConfig.conf'
        if conSection != None:
            self.sectionConfig = conSection
        else:
            self.sectionConfig = 'defaultConfig'
        self.ipaddr = '198.46.132.117'
        self.port = '8080'
        self.datadir = 'data'
        self.maxsize = '25'
        # Load the configuration from the file
        self.configParams = ConfigParser.ConfigParser().read(self.fileConfig)
        try:
            logging.info("Reading from config file:")
            for key, value in self.configParams.items(self.sectionConfig):
                setattr(self, key, value)
                logging.info("{0} = {1}".format(key, value))
        except OSError as ex:
            logging.error("Failed to read the provided config file: {0}".format(ex))
            logging.error("Please check parameter names and types.")
            
    # create an IP address for the webserver to use
    def getIP(self):
        return web.net.validip("{0}:{1}".format(self.ipaddr, self.port))

    # get the specified directory and convert it to an absolute path
    def getDataDir(self):
        return os.path.abspath(self.datadir)

    # get the maximum size and convert from kb to bytes
    def getMaxSize(self):
        return int(self.maxsize) * 1024
