extends Node

var udp: PacketPeerUDP = PacketPeerUDP.new()
var data
var PORT
var IP_ADDRESS

func _ready() -> void:
	# Connect to the Python socket
	get_socket_data()
	udp.connect_to_host(IP_ADDRESS, PORT)
	send_data("SYN")

func _process(_delta: float) -> void:
	if udp.get_available_packet_count() > 0:
		var packet = udp.get_packet()
		var json_string = packet.get_string_from_utf8()
		data = JSON.parse_string(json_string)

func get_socket_data() -> void:
	var file = FileAccess.open("res://TTEA/sockets.txt", FileAccess.READ)
	var content = file.get_as_text()
	var sockdata = content.split(":")
	IP_ADDRESS = sockdata[0]
	PORT = int(sockdata[1])

func connect_ttea() -> void:
	#                        TODO                          #
	# keep sending SYN requests until comm.py sends an ACK #
	udp.connect_to_host(IP_ADDRESS, PORT)

func send_data(to_send: String) -> void:
	var data_to_send = {"value": to_send}
	var json_string = JSON.stringify(data_to_send)
	print(data_to_send)
	udp.put_packet(json_string.to_utf8_buffer())

func calibrate() -> void:
	send_data("CAL")
