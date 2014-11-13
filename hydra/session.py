# _*_ coding: utf-8 _*_
# This project is fllowing Pedram Amini's sulley, the core part is sully,
#  some part overwrite by me.
# See detail sulley form https://github.com/OpenRCE/sulley
# If there is a problem, please contact tutengfei.kevin@gmail.com
# Thank you!
"""
@the first author: Pedram Amini
@the second author: tutengfei.kevin
@contact: tutengfei.kevin@gmail.com
@source: https://github.com/tutengfei/hydra
"""
import pickle
import logging
import socket
import time
import zlib
import sys
from hydra import pgraph
from hydra.utils import sex


TIME_SLEEP = 0.618
TIME_OUT = 5.0
RESTART_SLEEP_TIME = 300


class Target:
    """
        Target descriptor container.
    """
    def __init__(self, host, port, **kwargs):
        """
        @:type host: String
        @:param host: Hostname or IP address of target system

        @:type port: Integer
        @:param port: Port of target service
        :return:
        """
        self.host = host
        self.port = port

        self.netmon = None
        self.procmon = None
        self.vmcontrol = None
        self.netmon_options = {}
        self.procmon_options = {}
        self.vmcontrol_options = {}

    def pedrpc_connect(self):
        """

        :return:
        """
        if self.procmon:
            while 1:
                try:
                    if self.procmon.alive():
                        break
                except:
                    pass

                time.sleep(TIME_SLEEP)

            for key in self.procmon_options:
                eval('self.procmon.set_%s(self.procmon_options["%s"])' % (key, key))

        if self.netmon:
            while 1:
                try:
                    if self.netmon.alive():
                        break
                except:
                    pass
                time.sleep(TIME_SLEEP)

            for key in self.netmon_options:
                eval("self.netmon.set_%s(self.netmon_options['%s')" % (key, key))


class Connection(pgraph.Edge):
    def __init__(self, src, dst, callback=None):
        """

        :param src:
        :param dst:
        :param callback:
        :return:
        """
        super().__init__(src, dst)
        self.callback = callback


class Session(pgraph.Graph):
    def __init__(self, session_filename=None, skip=0, sleep_time=TIME_SLEEP,
                 log_level=30, logfile=None, logfile_level=10, proto="tcp",
                 bind=None, restart_interval=0, timeout=TIME_OUT,
                 web_port=26000, crash_threshold=3,
                 restart_sleep_time=RESTART_SLEEP_TIME):
        """

        :param session_filename:
        :param skip:
        :param sleep_time:
        :param log_level:
        :param logfile:
        :param logfile_level:
        :param proto:
        :param bind:
        :param restart_interval:
        :param timeout:
        :param web_port:
        :param crash_threshold:
        :param restart_sleep_time:
        :return:
        #================ log levels =======================
        Level	Numeric value
        CRITICAL	50
        ERROR	40
        WARNING	30
        INFO	20
        DEBUG	10
        NOTSET	0
        #====================================================
        """
        super().__init__()

        self.session_file = session_filename
        self.skip = skip
        self.sleep_time = sleep_time
        self.proto = proto
        self.bind = bind
        self.ssl = False
        self.restart_interval = restart_interval
        self.timeout = timeout
        self.web_port = web_port
        self.crash_threshold = crash_threshold
        self.restart_sleep_time = restart_sleep_time

        # Initializer logger
        self.logger = logging.getLogger("hydra_logger")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #TODO we can use logging.basicConfig
        if not logfile:
            filehandler = logging.FileHandler(logfile)
            filehandler .setLevel(logfile_level)
            filehandler.setFormatter(formatter)
            self.logger.addHandler(filehandler)

        consolehandler = logging.StreamHandler()
        consolehandler.setFormatter(formatter)
        consolehandler.setLevel(log_level)
        self.logger.addHandler(consolehandler)

        self.total_num_mutations = 0
        self.total_mutant_index = 0
        self.fuzz_node = None
        self.targets = []
        self.netmon_results = {}
        self.procmon_results = {}
        self.protmon_results = {}
        self.pause_flag = False
        self.crashing_primitives = {}

        if self.proto == "tcp":
            self.proto = socket.SOCK_STREAM
        elif self.proto == "ssl":
            self.proto = socket.SOCK_STREAM
            self.ssl = True
        elif self.proto == "udp":
            self.proto = socket.SOCK_DGRAM
        else:
            raise sex.Error("INVALID PROTOCOL SPECIFIED: %s" % self.proto)

        #import setting if they exist
        self.import_file()

        #creat a root node ,we do this because we need to start fuzzing from
        #  a single point and the user may want to specify a number of initial requests.

        self.root = pgraph.Node()
        self.root.name = "__ROOT_NODE__"
        self.root.label = self.root.name
        self.last_recv = None

        self.add_node(self.root)


    def add_node(self, node):
        """

        :param node:
        :return:
        """
        node.number = len(self.nodes)
        node.id = len(self.nodes)

        if node.id not in self.nodes:
            self.node[node.id] = node

        return self

    def add_target(self, target):
        """

        :param target:
        :return:
        """
        #pass specified target parameters to the PED-RPC server.
        target.pedrpc_connect()

        #add target to internal list
        self.targets.append(target)

    def connect(self, src, dst=None, callback=None):
        """

        :param src:
        :param dst:
        :param callback:
        :return:
        """
        # if only a source was provided, then make it the destination
        # and set the source to the root node.
        if not dst:
            dst = src
            src = self.root

        # if source or destination is a name, resolve the actual node.
        if type(src) is str:
            src = self.find_node("name", src)
        if type(dst) is str:
            dst = self.find_node("name", dst)

        #if source or destination is not in the graph , add it
        if src != self.root and not self.find_node("name", src.name):
            self.add_node(src)

        if not self.find_node("name", dst.name):
            self.add_node(dst)

        edge = Connection(src.id, dst.id, callback)
        self.add_edge(edge)

        return edge

    def export_file(self):
        """

        :return:
        """

        if not self.session_file:
            return
        data = {
            'session_filename': self.session_file,
            'skip': self.total_mutant_index,
            'sleep_time': self.sleep_time,
            'restart_sleep_time': self.proto,
            'timeout': self.timeout,
            'web_port': self.web_port,
            'crash_threshold': self.crash_threshold,
            'total_num_mutations': self.total_num_mutations,
            'total_mutant_index': self.total_mutant_index,
            'netmon_results': self.netmon_results,
            'procmon_results': self.procmon_results,
            'protmon_results': self.protmon_results,
            'pause_flag': self.pause_flag
        }

        try:
            fh = open(self.session_file, 'wb+')
            fh.write(zlib.compress(pickle.dumps(data, protocol=2)))
        except:
            raise sex.Error(sys.exc_info())
        finally:
            fh.close()

    def fuzz(self, this_node=None, path=[]):
        """

        :param this_node:
        :param path:
        :return:
        """
        if not self.targets:
            raise sex.Error("NO TARGETS SPECIFIED IN SESSION")

        if not self.edges_from(self.root.id):
            raise sex.Error("NO REQUESTS SPECIFIED IN SESSION")

        this_node = self.root
        try:
            self.server_init()
        except:
            return

        # xxx- TODO -complate parallel fuzzing, will likely have to thread out each target
        target = self.targets[0]

        #step through every edge from the current node.
        for edge in self.edges_from(this_node.id):
            self.fuzz_node = self.nodes[edge.id]
            num_mutations = self.fuzz_node.num_mutations()

        #keep track of th path as we fuzz through it, don't count the root node
        #
            path.append(edge)
            current_path = " -> ".join([self.nodes[e.src].name for e in path[1:]])
            current_path += " -> %s" % self.fuzz_node.name
            self.logger.error("current fuzz path: %s" % current_path)
            self.logger.error("fuzzed %d of %d total cases" %
                              (self.total_mutant_index, self.total_num_mutations))

            done_with_fuzz_node = False
            crash_count = 0

            #loop through all possible mutations of fuzz node
            while not done_with_fuzz_node:
                self.pause()

                #if we have exhausted the mutations of the fuzz node,
                #  break out the while(1).
                #note: when mutate() returns False, the node has been reverted to the default (valid) state.
                if not self.fuzz_node.mutate():
                    self.logger.error("all possible mutations for current fuzz noe exhausted")
                    done_with_fuzz_node = True
                    continue

                #make a record in the session that a mutation was made
                self.total_mutant_index += 1

                #if we've hit the retart interval , restart the target.
                if self.restart_interval and self.total_mutant_index % self.restart_interval == 0:
                    self.logger.error("restart interval of %d reached" % self.restart_interval)
                    self.restart_target()

                #exception error handing routine, print log message and restart target
                def error_handler(e, msg, target, sock=None):
                    if sock:
                        sock.close()
                    msg += "\n Exception caught: %s" % repr(e)
                    msg += "\n Restarting target and trying again"

                    self.logger.critical(msg)
                    self.restart_target(target)

                #if we don't need to skip the current test node.
                #TODO
                if self.total_mutant_index > self.skip:
                    self.logger.error("fuzzing %d of %d " % (self.fuzz_node.mutant_index, num_mutations))
                    #TODO












