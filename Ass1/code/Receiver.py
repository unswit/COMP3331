#!/usr/bin/python

# Simple Transport Protocol (STP)
#
# Receiving side program

# Sender -> Packet (seq = 10) -> Receiver
# if match seq number
# 		keep packet
#		send back ACK indicating next packet with 10 + len(data)
# else
#		discard packet (or buffer)

# Example: Sender
# (seq 1) get ACK 11 -> send which packet to repeat
# (seq 11)
# (seq 21)

import pickle
import sys
from socket import *

class STPPacket:
	def __init__(self, data, seq_num, ack_num, ack=False, syn=False, fin=False):
		self.data = data
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack = ack
		self.syn = syn
		self.fin = fin

class Receiver:
	# you need to create this
	# receiver needs to have a sequence number so it can deal with out-of-order pakes
	# receiver receives stp_packet and then writes the data inside the packet

	# initialise sender data: seq number, timeout
	def __init__(self, port, file):
		self.port = int(port)
		self.file = file

	# create UDP socket
	socket = socket(AF_INET, SOCK_DGRAM)
	#socket.setblocking(0)		# temp fix
	#socket.settimeout(100)		# temp fix

	# receive packet from sender
	# convert packet to dict format
	def stp_rcv(self):
		data, client_addr = self.socket.recvfrom(2048)   # extracts sender IP and port number
		stp_packet = pickle.loads(data)			  # converts data back to packet
		return stp_packet, client_addr 			  # return both packet + client_addr

	# grab payload from packet
	#def get_data(self, packet):
	#	data = stp_packet.data
	#	return data

	# append packet data to single receiver txt file
	def stp_append(self, data):
		print("data = {}".format(data))
		#f = open("r_test.txt", "a+")
		#f.write(data)
		#f.close()

	# create ACK packet without payload
	# RECEIVER SYNACK
	def make_ACK(self):
		# no payload (data = empty)
		SYNACK = STPPacket(0, self.init_seq_num, self.init_ack_num, True, True, False)
		return SYNACK

	# receiver send a packet to sender (ACKS, NAKS etc.)
	def udp_send(self, packet, addr):
		# sender explicitly attaches IP destination address and port no. to each packet
		self.socket.sendto(pickle.dumps(packet), addr)
		#return_msg, server_add = socket.recvfrom(2048)	# receives data from server

	# FIN close
	def stp_close(self):
		self.socket.close()

###################
# MAIN FUNCTION???
###################

# Check correct usage
num_args = 3
if len(sys.argv) != num_args:				# check num args
	print("Usage: ./Receiver.py port file.txt")
# Continue to main operation
else:
	### SET UP VARIABLES ###
	# init seq ack numbers
	seq_num = 0
	ack_num = 0
	client_addr = None
	# receiver states
	state_listen = True
	state_syn_rcv = False
	state_synack_sent = False
	state_established = False
	# grab args, create receiver socket
	port, file = sys.argv[1:]				# grab args
	receiver = Receiver(port, file)			# create instance of sender
	receiver.socket.bind(('', receiver.port))
	print("Receiver is ready ...")
	log = open("Receiver_log.txt","w")		# create log for recording segment info
	# waiting for file from sender
	count = 0
	while True:
		count += 1
		print("{} loop".format(count))
	### CLOSED STATE ###
		if state_listen == True:
			print("STATE: LISTEN")
			syn_pkt, client_addr = receiver.stp_rcv() # wait for SYN packet
			syn_bit = syn_pkt.syn 					 # grab SYN bit after receiving packet
			print("syn data = {}".format(syn_pkt.data))
			if syn_bit == True:
				print("SYN = inside synack creation")
				synack_pkt = STPPacket('2. SYNACK', 1, 1, ack=True, syn=True, fin=False)
				print("SYNACK created")
				receiver.udp_send(synack_pkt, client_addr)
				print("SYNACK sent")
				state_synack_sent = True
				state_listen = False
		if state_synack_sent == True:
			print("STATE: SYNACK SENT")
			ack_pkt, client_addr = receiver.stp_rcv()  		# wait for ACK packet
			ack_bit = ack_pkt.ack
			print("ACK = {}".format(ack_bit))
		# generate ACK immediately after receiving segment (ACK = STP segment - payload)
		#data = stp_packet.data 					# obtain payload from packet
		#receiver.stp_append(data)		 		# append packet data to r_file.txt
		break	# temp break to stop loop
	# print test the output file
	print("Current file content:\n")
	f = open("r_test.txt","r")
	print(f.read())
	# everything finished -> close connection
	receiver.stp_close()


# on receive
# The receiver should generate ACK immediately after receiving a data segment
#self.timer.cancel()

'''
The receiver is expected to buffer out-of-order arrival packets.
 The receiver should first open a UDP listening socket on receiver_port and then wait for segments to arrive from the Sender.
 The first segment to be sent by the Sender is a SYN segment and the receiver is expected to reply a SYNACK segment.
 After the completion of the three-way handshake, the receiver should create a new text file called file.txt.
 All incoming data should be stored in this file.
 The Receiver should first extract the STP packet from the arriving UDP datagrams and then extract the data (i.e. payload) from the STP packet.
 Note that, the Receiver is allowed to examine the header of the UDP datagram that encapsulates the STP Packet to determine the UDP port and IP address that the Sender is using.
 The data should be written into file.txt.
At the end of the transfer, the Receiver should have a duplicate of the text file sent by the Sender.
 You can verify this by using the diff command on a Linux machine (diff file1.txt file2.txt).
 The Receiver should also maintain a log file titled Receiver_log.txt where it records the information about each segment that it sends and receives.
 The format should be exactly similar to the sender log file as outlined in the Sender specification.
The Receiver should terminate after the connection closure procedure initiated by the sender concludes.
The Receiver should also print the following statistics at the end of the log file (i.e. Receiver_log.txt):
'''


# 1. Sender waits for data to be passed down from app layer
# 		wait()
# 2. stp_send(data) is called by app layer.
# 3. sender creates packet sndpkt + checksum
# 		stp_send(data)
# 4. send packet via. udp_send
# 		udp_send()
'''
# On packet arrival, receiver replies with ACK/NAK depending on if packet is corrupted
Corrupted = stp_rcv(rcvpkt) && corrupt()
#     -> send NAK packet via. udp_send()
Uncorrupted = rdt_rcv(rcvpkt) && notCorrupt()
#     -> cont. to next step

# Extract data
extract()

# Deliver data to upper layer
deliver()

# Send ACK packet back
udt_send()




# wait for ACK packet -> ACK comes back
# if waiting, can't receive more data from app layer = stp_send() can't occur
# if ACK, go back to waiting for data from app layer
stp_rcv(rcvpkt) && isACK


# wait for ACK packet -> NAK comes back
# if waiting, can't receive more data from app layer = stp_send() can't occur
# if NAK, retransmit last packet + wait for ACK again
stp_rcv(rcvpkt) && isNAK

'''




