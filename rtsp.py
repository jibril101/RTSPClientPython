import io, socket, sys, time, random
from threading import Thread, Event, Timer, Lock
import _thread
# from bitstring import BitArray

# exit_event = Event()
buffer = []
bufferIdx = 0
lock = Lock()
def sortBySequenceNum(ele):
    return ele[2]

class RTSPException(Exception):
    def __init__(self, response):
        super().__init__(f'Server error: {response.message} (error code: {response.response_code})')

class Response:
    def __init__(self, reader):
        '''Reads and parses the data associated to an RTSP response'''
        first_line = reader.readline().split(' ', 2)
        if len(first_line) != 3:
            raise Exception('Invalid response format. Expected first line with version, code and message')
        self.version, _, self.message = first_line
        if self.version != 'RTSP/1.0':
            raise Exception('Invalid response version. Expected RTSP/1.0')
        self.response_code = int(first_line[1])
        self.headers = {}
        
        while True:
            line = reader.readline().strip()
            if not line or ':' not in line: break
            hdr_name, hdr_value = line.split(':', 1)
            self.headers[hdr_name.lower()] = hdr_value
            if hdr_name.lower() == 'cseq':
                self.cseq = int(hdr_value)
            elif hdr_name.lower() == 'session':
                self.session_id = int(hdr_value)
        
        if self.response_code != 200:
            raise RTSPException(self)
    
class Connection:
    def __init__(self, session, address):
        '''Establishes a new connection with an RTSP server. No message is
	sent at this point, and no stream is set up.
        '''
        self.session = session
        self.serverAddress = (address[0], int(address[1]))
        self.BUFFER_LENGTH = 0x10000
        self.state = "init"
        self.exit_event = Event()
        self.sessionID = None
        self.seqNum = 0
        
        self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rtspSocket.connect(self.serverAddress)

    def send_request(self, command, include_session=True, extra_headers=None):
        '''Helper function that generates an RTSP request and sends it to the
        RTSP connection.
        '''
        # TODO
        self.rtspSocket.send(command.encode('utf-8'))

    def start_rtp_timer(self):
        '''Starts a thread that reads RTP packets repeatedly and process the
	corresponding frame (method ). The data received from the
	datagram socket is assumed to be no larger than BUFFER_LENGTH
	bytes. This data is then parsed into its useful components,
	and the method `self.session.process_frame()` is called with
	the resulting data. In case of timeout no exception should be
	thrown.
        '''
        global buffer
        allFramesLoaded = ['False']
        self.rtpThread = Thread(target=self.thread_func, args=[buffer, allFramesLoaded])
        rtpThread1 = Thread(target=self.thread_func_1)
        rtpThread2 = Thread(target=self.thread_func_2, args=[buffer, allFramesLoaded])
        self.rtpThread.start()
        rtpThread1.start()
        rtpThread1.join()
        rtpThread2.start()
        #buffer = []
        #bufferLen = len(buffer)
        
    def thread_func_1(self):
        time.sleep(3)

    def thread_func_2(self, buffer, allFramesLoaded):
        global bufferIdx
        if self.exit_event.is_set():
            return
        stopEvent = Event()
        while bufferIdx < len(buffer):
        #for frame in buffer:
            if self.exit_event.is_set():
                return
            if (abs(bufferIdx - len(buffer)) <= 1) and (allFramesLoaded[0] == 'False'):
                time.sleep(2.5)
            frame = buffer[bufferIdx]
            stopEvent.wait(0.04)
            self.session.process_frame([0], frame[1], frame[2], frame[3], frame[4])
            bufferIdx += 1
        # if 'True' in allFramesLoaded and bufferIdx >= (len(buffer) - 1):
        #     return

    
    def thread_func(self, buffer, allFramesLoaded):
        t0 = time.time()
        numPackets = 0
        outOfOrder = 0
        previousIdx = -1
        movie0TotalPackets = 231
        while(True):
            if self.exit_event.is_set():
                break
            try:
                continueRecieving = True
                rtpPacket = self.udpSocket.recv(self.BUFFER_LENGTH)
                if len(rtpPacket) != 0:
                    numPackets += 1
                marker2 = rtpPacket[1] >> 7
                payloadType2 = rtpPacket[1] & 0b01111111
                sequenceNumber2 = int.from_bytes(rtpPacket[2 : 4],"big")
                if sequenceNumber2 != 0 and (sequenceNumber2 - previousIdx) != 1:
                    outOfOrder += 1
                previousIdx = sequenceNumber2
                timeStamp = int.from_bytes(rtpPacket[4: 8], "big")
                payload = rtpPacket[12: ]
                with lock:
                    buffer.append([payloadType2, marker2, sequenceNumber2, timeStamp, payload])
                    buffer.sort(key=sortBySequenceNum)
                # self.session.process_frame(payloadType2, marker2, sequenceNumber2, timeStamp, payload)
            except (socket.timeout, socket.error):
                break
        allFramesLoaded[0] = 'True'
        t1 = time.time()
        # buffer.sort(key=sortBySequenceNum)
        rate =  numPackets / (t1 - t0)
        lossRate = (movie0TotalPackets - numPackets) / (t1 - t0)
        print("rate: ", rate)
        print("num packets lost: ", movie0TotalPackets - numPackets)
        print("packet loss / sec: ", lossRate)
        print("out of order: ", outOfOrder)
        print("last sequence #: ", sequenceNumber2)



    def stop_rtp_timer(self):
        '''Stops the thread that reads RTP packets'''
        # TODO
        self.exit_event.set()

    def setup(self):
        '''Sends a SETUP request to the server. This method is responsible for
	sending the SETUP request, receiving the response and
	retrieving the session identification to be used in future
	messages. It is also responsible for establishing an RTP
	datagram socket to be used for data transmission by the
	server. The datagram socket should be created with a random
	UDP port number, and the port number used in that connection
	has to be sent to the RTSP server for setup. This datagram
	socket should also be defined to timeout after 1 second if no
	packet is received.
        '''
        #if self.state == "init":
        updPort = random.randint(40000, 50000)
        command = "SETUP " + str(self.session.video_name) + " RTSP/1.0" + "\r\n" + "CSeq: " + str(self.seqNum + 1) + "\r\n" + "Transport: RTP/UDP; client_port= " + str(updPort) + "\r\n\r\n"
        self.send_request(command)
        recievedPacket = self.rtspSocket.recv(4096)
        print(recievedPacket)
        if "200" in recievedPacket.decode('utf-8'):
            self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udpSocket.bind(("", updPort))
            self.udpSocket.settimeout(1)
            recievedPacket = recievedPacket.decode('utf-8')
            self.sessionID = recievedPacket[recievedPacket.find("Session:") + 9 : recievedPacket.find("\r\n\r\n")] 
            print("sessionId: ", self.sessionID)
            self.seqNum += 1
            self.state = "ready"
        else:
            serverMsg = recievedPacket.decode().rstrip().replace("RTSP/1.0 ", ' ')
            errMsg = "Error in SETUP:" + serverMsg
            raise Exception(errMsg)


    def play(self):
        '''Sends a PLAY request to the server. This method is responsible for
	sending the request, receiving the response and, in case of a
	successful response, starting the RTP timer responsible for
	receiving RTP packets with frames.
        '''

        if self.state != "ready":
            raise Exception("OPEN needs to first be called.")
        command = "PLAY " + str(self.session.video_name) + " RTSP/1.0" + "\r\n" + "CSeq: " + str(self.seqNum + 1) + "\r\n" + "Session: " + str(self.sessionID) + "\r\n\r\n"
        self.send_request(command)
        rtspReply = self.rtspSocket.recv(4096)
        print(rtspReply)
        if "200" in rtspReply.decode('utf-8'):
            self.exit_event = Event()
            self.state = "playing"
            self.seqNum += 1
            self.start_rtp_timer()
            self.state = "ready"
        else:
            serverMsg = rtspReply.decode().rstrip().replace("RTSP/1.0 ", ' ')
            errMsg = "Error in PLAY:" + serverMsg
            raise Exception(errMsg)
            #self.state = "ready"


    def pause(self):
        '''Sends a PAUSE request to the server. This method is responsible for
	sending the request, receiving the response and, in case of a
	successful response, cancelling the RTP thread responsible for
	receiving RTP packets with frames.
        '''
        if self.state != "ready":
            raise Exception("PAUSE called in invalid state.")
        command = "PAUSE " + str(self.session.video_name) + " RTSP/1.0" + "\r\n" + "CSeq: " + str(self.seqNum + 1) + "\r\n" + "Session: " + str(self.sessionID) + "\r\n\r\n"
        self.send_request(command)
        rtspReply = self.rtspSocket.recv(4096)
        print(rtspReply)
        if "200" in rtspReply.decode('utf-8'):
                self.seqNum += 1
                self.stop_rtp_timer()
                self.state = "ready"
        else:
            serverMsg = rtspReply.decode().rstrip().replace("RTSP/1.0 ", ' ')
            errMsg = "Error in PAUSE:" + serverMsg
            raise Exception(errMsg)

    def teardown(self):
        '''Sends a TEARDOWN request to the server. This method is responsible
	for sending the request, receiving the response and, in case
	of a successful response, closing the RTP socket. This method
	does not close the RTSP connection, and a further SETUP in the
	same connection should be accepted. Also this method can be
	called both for a paused and for a playing stream, so the
	timer responsible for receiving RTP packets will also be
	cancelled.
        '''
        # TODO
        if self.state != "ready":
            return
        command = "TEARDOWN " + str(self.session.video_name) + " RTSP/1.0" + "\r\n" + "CSeq: " + str(self.seqNum + 1) + "\r\n" + "Session: " + str(self.sessionID) + "\r\n\r\n"
        self.send_request(command)
        rtspReply = self.rtspSocket.recv(4096)
        print(rtspReply)
        if "200" in rtspReply.decode('utf-8'):
            self.stop_rtp_timer()
            self.udpSocket.shutdown(socket.SHUT_RDWR)
            self.udpSocket.close()
            global buffer, bufferIdx
            buffer.clear()
            bufferIdx = 0
            self.seqNum += 1
            #self.state = "init"
        else:
            serverMsg = rtspReply.decode().rstrip().replace("RTSP/1.0 ", ' ')
            errMsg = "Error in TEARDOWN:" + serverMsg
            raise Exception(errMsg)

    def close(self):
        '''Closes the connection with the RTSP server. This method should also
	close any open resource associated to this connection, such as
	the RTP connection, if it is still open.
        '''
        if self.exit_event.is_set():
            self.stop_rtp_timer()
        if "udpSocket" in Connection.__dict__:
            self.udpSocket.shutdown(socket.SHUT_RDWR)
            self.udpSocket.close()
        self.rtspSocket.shutdown(socket.SHUT_RDWR)
        self.rtspSocket.close()
        
