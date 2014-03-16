#!/usr/bin/python
#
## @file 
#
# A TCP communication class that acts as the client side for generic communications
# between programs in the storm-control project
#
# ----------------------------------------------------------------------------------------
# Jeffrey Moffitt
# 3/8/14
# jeffmoffitt@gmail.com
# ----------------------------------------------------------------------------------------

# 
# Import
# 
import sys
import time
from PyQt4 import QtGui, QtNetwork
from sc_library.tcpMessage import TCPMessage
from sc_library.tcpCommunications import TCPCommunications

## TCPClient
#
# A TCP client class used to transfer TCP messages from one program to another
#
class TCPClient(TCPCommunications):

    ## __init__
    #
    # Class constructor
    #
    # @param parent A reference to an owning class.
    # @param port The TCP/IP port for communication.
    # @param server_name A string name for the communication server.
    # @param address An address for the TCP/IP communication.
    # @param verbose A boolean controlling the verbosity of the class
    #
    def __init__(self,
                 parent = None,
                 port=9500,
                 server_name = "default",
                 address = QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost),
                 verbose = False):
        TCPCommunications.__init__(self, parent=parent, port=port, server_name=server_name,
                                   address=address, verbose=verbose)
        
        # Create instance of TCP socket
        self.socket = QtNetwork.QTcpSocket()
        self.socket.readyRead.connect(self.handleReadyRead)

    ## connectToServer
    #
    # Attempt to establish a connection with the server at the indicated address and port
    #
    def connectToServer(self):
        if self.verbose:
            string = "Looking for " + self.server_name + " server at: \n"
            string += "    Address: " + self.address.toString() + "\n"
            string += "    Port: " + str(self.port)
            print string

        # Attempt to connect to host.
        self.socket.connectToHost(self.address, self.port)
        tries = 0
        while (not self.socket.waitForConnected() and (tries < self.num_conn_tries)):
            print "Could not find " + self.server_name + " server. Attempt: " + str(tries)
            time.sleep(1)
            self.socket.connectToHost(self.address, self.port)
            tries += 1
            
        if tries==self.num_conn_tries:
            print self.server_name + " server not found"
        else:
            print "Connected to "+ self.server_name + " server"

    ## startCommunication
    #
    # Start communications with server
    #
    def startCommunication(self):
        if not self.isConnected():
            self.connectToServer()

    ## stopCommunication
    #
    # Stop communications with server
    #
    def stopCommunication(self):
        if self.isConnected():
            self.socket.disconnectFromHost()

# ----------------------------------------------------------------------------------------
# Stand Alone Test Class
# ----------------------------------------------------------------------------------------                                                                
class StandAlone(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(StandAlone, self).__init__(parent)

        # Create client
        self.client = TCPClient(port = 9500, server_name = "Test", verbose = True)

        self.client.message_ready.connect(self.handleMessageReady)            
        self.client.startCommunication()

        self.message_ID = 1
        self.sendTestMessage()
        
    # ----------------------------------------------------------------------------------------
    # Send Test Messages
    # ----------------------------------------------------------------------------------------
    def sendTestMessage(self):
        if self.message_ID == 1:
            # Create Test message
            message = TCPMessage(message_type = "Stage Position",
                                 message_data = {"Stage_X": 100.00, "Stage_Y": 0.00})
        elif self.message_ID ==2:
            message = TCPMessage(message_type = "Movie",
                                 message_data = {"Name": "Test_Movie_01", "Parameters": 1})

        else:
            message = TCPMessage(message_type = "Done")
    
        self.message_ID += 1
        self.sent_message = message
        self.client.sendMessage(message)
        
    # ----------------------------------------------------------------------------------------
    # Handle New Message
    # ----------------------------------------------------------------------------------------
    def handleMessageReady(self, message):
        # Handle responses to messages
        if self.sent_message.getID() == message.getID():
            if message.isComplete():
                print "Completed message: "
                print message
        else:
            print "Received an unexpected message"

        self.sendTestMessage()
        
    # ----------------------------------------------------------------------------------------
    # Handle close event
    # ----------------------------------------------------------------------------------------
    def closeEvent(self, event):
        self.client.close()
        self.close()
       
# ----------------------------------------------------------------------------------------
# Test/Demo of Class
# ----------------------------------------------------------------------------------------                        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = StandAlone()
    window.show()
    sys.exit(app.exec_())
    
#
# The MIT License
#
# Copyright (c) 2013 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
