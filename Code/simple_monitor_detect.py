from operator import attrgetter
import eventlet
import numpy
import time
import random
import multiprocessing as mp
import pcap
import dpkt
import socket
import binascii
import operator
import struct
import math


from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from rui.lib.packeet import ethernet, packet, arp, ipv4, tcp, udp
from ryu.lib import hub
from math import *

trafic_before = 0 
tx_before = 0
pkt_before = 0 
n = 0
m = 0
x = 0
list_traffic = [0]
list_entropy = [0]
list_entropy2 = [0]
list_entropy_ddos = [0]
list_in = ['0']
list_dst = ['0']
std = 0

class SimpleMonitor(simple_switch_13.SimpleSwitch13):
    def __init__(self, *args, **kwargs):
        super(SimpleMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)


    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

	def _monitor(self):
		while True:
			for dp in self.datapaths.values():
				self._request_stats(dp)
			hub.sleep(1)


	def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        msg = ev.msg
		datapath = msg.datapath
		datapath = msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		body = ev.msg.body
		global eth_src
		global eth_dst
		global std
		self.logger.info('datapath         '
						'in-port  eth-dst           '
						'out-port packets  bytes')
		self.logger.info('---------------- '
						'-------- ----------------- '
						'-------- -------- --------')
		for stat in sorted([flow for flow in body if flow.priority == 1],
			key=lambda flow: (flow.match['in_port'],
								flow.match['eth_dst'])):
			self.logger.info('%016x %8x %17s %8x %8d %8d',
							ev.msg.datapath.id,
							stat.match['in_port'], stat.match['eth_dst'],
							stat.instructions[0].actions[0].port,
							stat.packet_count, stat.byte_count)
		
		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		arp_pkt = pkt.get_protocol(arp.arp)
		ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
		#fetches 3rd item from list of protocols (tcp or udp). Instead of having separate udp and tcp

		source_ip = ipv4_pkt.src
		destination_ip = ipv4_pkt.dst


		print(source_ip)
		print(destination_ip)

		# if pkt.get_protocols(tcp.tcp) or pkt.get_protocols(udp.udp):
		# #if (stat.instructions[0].actions[0].port == 1 and stat.match['in_port'] == 2):
		# 	# tx_skrg = stat.byte_count - tx_before
		# 	# pkt_skrg = stat.packet_count - pkt_before
		# 	# tx_before = stat.byte_count
		# 	# pkt_before = stat.packet_count
		# 	in_port = stat.in_port
		# 	eth_dst = stat.eth_dst
		# 	list_in.append(in_port)
		# 	list_dst.append(dst_port)
		
		# 	#print(list_in)
		# 	if len(list_in) >= 10:
		# 		list_in.reverse()
		# 		list_in.pop()
		# 		list_in.reverse()
			
		# 	#print(list_dst)
		# 	if len(list_dst) >= 10:
		# 		list_dst.reverse()
		# 		list_dst.pop()
		# 		list_dst.reverse()


    # @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    # def _port_stats_reply_handler(self, ev):
    #     body = ev.msg.body
	# 	global trafic_before
	# 	global list_traffic
	# 	global n
	# 	global x
	# 	global std
		
	# 	self.logger.info('datapath         port     '
	# 					'rx-pkts  rx-bytes rx-error '
	# 					'tx-pkts  tx-bytes tx-error')
	# 	self.logger.info('---------------- -------- '
	# 					'-------- -------- -------- '
	# 					'-------- -------- --------')
	# 	for stat in sorted(body, key=attrgetter('port_no')):
	# 		self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d', 
	# 						ev.msg.datapath.id, stat.port_no,
	# 						stat.rx_packets, stat.rx_bytes, stat.rx_errors,
	# 						stat.tx_packets, stat.tx_bytes, stat.tx_errors)
	
	# 		trafic_skrg = stat.tx_packets - trafic_before

	# 		if (stat.port_no == 1):
	# 			print 'nilai trafic :', trafic_skrg
	# 			trafic_before = stat.tx_packets
	# 		list_traffic.append(trafic_skrg)
	# 		n = n+1
	# 		mean = sum(list_traffic) / 30
	# 		#print 'nilai mean : ',mean
	# 		#hitung entropy
			
	# 		c = float(list_traffic.count(trafic_skrg))
	# 		p = c/30
	# 		float(p)
	# 		#print 'peluang:',p
	# 		#hitung nilai entropy
	# 		#-np.sum(p*np.log(p))/np.log(len(p))
	# 		if (p >0):
	# 			nilai_entropy = -p * math.log(p)
	# 			list_entropy.append(nilai_entropy)
	# 			#print 'traffic entropy:',list_entropy
	# 			entropy = sum(list_entropy)
	# 			print 'nilai entropy:', entropy
	# 			if len(list_entropy) >= 30:
	# 				list_entropy.reverse()
	# 				list_entropy.pop()
	# 				list_entropy.reverse()
				
	# 		if trafic_skrg - mean > 3*std:
	# 			print ' '
	# 			print '=Traffic - Mean > Three of the standard deviation='
	# 			print ' '
	# 			if trafic_skrg > 5000:
	# 				print 'suspect DDoS fase-1'
	# 				print 'suspect DDoS fase-1'
	# 				print 'suspect DDoS fase-1'
	# 				print ' '
	# 				print '=Checking entropy threshold='
	# 				# state nilai entropy >>> masalahnya di sini
					
	# 				#float(q)
	# 				#print 'peluang entropy:',q
	# 				#hitung nilai entropy ddos
					
	# 				#traffic_for_entropy = trafic_skrg/100
	# 				#traffic_entropy = round(traffic_for_entropy,2)
	# 				#print 'trafik entropy',traffic_entropy
	# 				#list_entropy2.append(traffic_entropy)
	# 				#list_entropy = (list_traffic)
	# 				#print 'traffic entropy ddos',list_entropy2
	# 				#d = float(list_entropy2.count(traffic_entropy))
	# 				#q = d / 30
	# 				#if (q > 0):
	# 					#nilai_entropy_ddos = -q * math.log(q)
	# 					#list_entropy_ddos.append(nilai_entropy_ddos)
	# 					#print 'list entropy ddos:',list_entropy_ddos
	# 					#if len(list_entropy_ddos) >= 30:
	# 						#list_entropy_ddos.reverse()
	# 						#list_entropy_ddos.pop()
	# 						#list_entropy_ddos.reverse()
						
						
	# 					#entropy_ddos = sum(list_entropy_ddos)
	# 					#print 'nilai entropy saat ddos:',entropy_ddos
	# 					#print 'entropy awal:',entropy_awal
	# 				nilai_entropy_awal = 5.00000
	# 				threshold_entropy = nilai_entropy_awal - entropy
	# 				if threshold_entropy > 0.7003755:
	# 					print 'Entropy threshold:', threshold_entropy
	# 					print '=Entropy threshold > 0.7003755='
	# 					print ' '
	# 					print 'DDOS attack detected !!!'
	# 					print 'DDOS attack detected !!!'
	# 					print 'DDOS attack detected !!!'
	# 					print 'DDOS attack detected !!!'
	# 					print 'DDOS attack detected !!!'
	# 					print ' ' 
			
	# 	print(list_traffic)
	# 	#print(list_entropy)
		
	# 	if len(list_traffic) >= 30:
	# 		list_traffic.reverse()
	# 		list_traffic.pop()
	# 		list_traffic.reverse()
					
	# 		#std = numpy.std(list_traffic)
	# 		#print 'nilai standart deviasi : ', std
			
				

	
#def _deteksi(self, traffic_skrg):
	#if traffic_skrg > std:
	##	return 1
	

