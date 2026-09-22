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
	rec_data()

func get_socket_data() -> void:
	var file = FileAccess.open("res://TTEA/sockdata.txt", FileAccess.READ)
	if not file:
		var content: String = get_available_addr_port()
		file = FileAccess.open("res://TTEA/sockdata.txt", FileAccess.WRITE)
		file.store_string(content)
	else:
		var content = file.get_as_text()
		var sockdata = content.split(":")
		IP_ADDRESS = sockdata[0]
		PORT = int(sockdata[1])

func get_available_addr_port() -> String:
	return " "

func connect_ttea() -> void:
	udp.connect_to_host(IP_ADDRESS, PORT)
	send_data("SYN")

func send_data(to_send: String) -> void:
	var data_to_send = {"value": to_send}
	var json_string = JSON.stringify(data_to_send)
	print(data_to_send)
	udp.put_packet(json_string.to_utf8_buffer())

func rec_data() -> void:
	if udp.get_available_packet_count() > 0:
		var packet = udp.get_packet()
		var json_string = packet.get_string_from_utf8()
		data = JSON.parse_string(json_string)

func calibrate() -> void:
	send_data("CAL")
