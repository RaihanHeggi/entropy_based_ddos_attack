from operator import attrgetter
import eventlet
import numpy as np
import math
# import time
# import random
# import multiprocessing as mp
# import pcap
# import dpkt
# import socket
# import binascii
# import operator
# import struct

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet import ethernet, packet, arp, ipv4, tcp, udp


n = 0
m = 0
x = 0
list_traffic = [0]
list_in = ['0']
list_dst = ['0']
std = 0

class SimpleMonitor13(simple_switch_13.SimpleSwitch13):

	def __init__(self, *args, **kwargs):
		super(SimpleMonitor13, self).__init__(*args, **kwargs)
		self.datapaths = {}
		self.monitor_thread = hub.spawn(self._monitor)

	@set_ev_cls(ofp_event.EventOFPStateChange,
				[MAIN_DISPATCHER, DEAD_DISPATCHER])
	def _state_change_handler(self, ev):
		datapath = ev.datapath
		if ev.state == MAIN_DISPATCHER:
			if datapath.id not in self.datapaths:
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
			hub.sleep(5)

	def _request_stats(self, datapath):
		self.logger.debug('send stats request: %016x', datapath.id)
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		req = parser.OFPFlowStatsRequest(datapath)
		datapath.send_msg(req)

		req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
		datapath.send_msg(req)

	def count_unique(self, listdata, n):
		list_hasil = []
		for x in listdata[1:]:
			if str(x[n]) in list_hasil:
				continue 
			else:
				list_hasil.append(x[n])
		return len(list_hasil)

	def count_entropy(self, count_data, count_dst, n):
		e_h = 0 
		list_h = [] 
		#threshold awal_berapa
		threshold = 0.0732
		print('========================PACKET IN CLASSIFICATION=============================\n')
		for x in count_data:
			# can change 10 to specific value wanted (windows_size)
			h = -(count_dst/10)*((x[1]/10)*math.log(x[1]/10))
			list_h.append(h)
			for h in list_h:
				#nilai e_h itu apa ? dan kalkulasinya bagaimana
				difference = h - e_h 
				#initial threshold berapa 
				if h < 0.0732:
					n += 1 
					# apakah nilai H akan sama n, karena nilai n yang bulat
					# h_i itu apa panjangnya atau apa
					if len(list_h) == n :
						e_h = sum(list_h) /n 
						sum_h = 0 
						for x in list_h :
							sum_h += (x - e_h)**2
						stdeviation = math.sqrt(sum_h/n)
						threshold = count_dst * stdeviation

				if difference > threshold:
					print("Intrusi")
				else:
					print("Normal")
		print('============================================================================\n')
		return


	def get_unique_list(self, listdata):
		unique_list = []
		for x in listdata:
			if x in unique_list:
				continue 
			else:
				unique_list.append(x)
		return unique_list
	
	def count_data(self, unique_list, listdata):
		count_data = 0
		list_hasil = []
		for x in unique_list:
			count_data = 0
			for j in listdata:
				if j == x :
					count_data += 1
			list_hasil.append([x, count_data])
		return list_hasil

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def _flow_stats_reply_handler(self, ev):
		msg = ev.msg		
		# body = ev.msg.body
		global eth_src
		global eth_dst
		global std
		# self.logger.info('datapath         '
		# 				'in-port  eth-dst           '
		# 				'out-port packets  bytes')
		# self.logger.info('---------------- '
		# 				'-------- ----------------- '
		# 				'-------- -------- --------')
		# for stat in sorted([flow for flow in body if flow.priority == 1],
		# 	key=lambda flow: (flow.match['in_port'],
		# 						flow.match['eth_dst'])):
		# 	self.logger.info('%016x %8x %17s %8x %8d %8d',
		# 					ev.msg.datapath.id,
		# 					stat.match['in_port'], stat.match['eth_dst'],
		# 					stat.instructions[0].actions[0].port,
		# 					stat.packet_count, stat.byte_count)

		datapath = msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		pkt = packet.Packet(msg.data)

		# eth = pkt.get_protocols(ethernet.ethernet)[0]
		# print("SRC : ",eth.src)
		# print("DST : ",eth.dst)
		# arp_pkt = pkt.get_protocol(arp.arp)
		# ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
		# tcp_pkt = pkt.get_protocol(tcp.tcp)
		# udp_pkt = pkt.get_protocol(udp.udp)

		# print("\nEth pkt: {0}".format(eth))
		# print("\nIPV4 pkt: {0}".format(ipv4_pkt))
		# print("\nARP pkt: {0}".format(arp_pkt))
		# print("\nTCP pkt: {0}".format(tcp_pkt))
		# print("\nUDP pkt: {0}".format(udp_pkt))

		if pkt.get_protocols(ethernet.ethernet):
			eth = pkt.get_protocols(ethernet.ethernet)[0]
			eth_src = eth.src
			eth_dst = eth.dst
			list_in.append(eth_src)
			list_dst.append(eth_dst)
			list_traffic.append([eth_src, eth_dst])

		if len(list_in) >= 50 or len(list_dst) >= 50:
			unique_src = self.count_unique(list_traffic,0)
			unique_dst = self.count_unique(list_traffic,1)
			unique_traffic = self.get_unique_list(list_traffic)
			count_data = self.count_data(unique_traffic, list_traffic)

			self.count_entropy(count_data, unique_dst, unique_src)


			#restore list in and list destination
			list_in.reverse()
			list_in.pop()
			list_in.reverse()

			list_dst.reverse()
			list_dst.pop()
			list_dst.reverse()
		
		

		# #if (stat.instructions[0].actions[0].port == 1 and stat.match['in_port'] == 2):
		# 	# tx_skrg = stat.byte_count - tx_before
		# 	# pkt_skrg = stat.packet_count - pkt_before
		# 	# tx_before = stat.byte_count
		# 	# pkt_before = stat.packet_count
		# 	in_port = stat.in_port
		# 	eth_dst = stat.eth_dst
		# 	list_in.append(in_port)
		# 	list_dst.append(dst_port)
		
			


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


