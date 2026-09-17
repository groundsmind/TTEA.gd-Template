extends Node

var udp := PacketPeerUDP.new()
var player_position: Vector2
const PORT = 4242
const IP_ADDRESS = "127.0.0.1"

func _ready() -> void:
	# Connect to the Python socket
	udp.connect_to_host(IP_ADDRESS, PORT)

func _process(delta: float) -> void:
	if udp.get_available_packet_count() > 0:
		var packet = udp.get_packet()
		var json_string = packet.get_string_from_utf8()
		var data = JSON.parse_string(json_string)
		print("Received from Python: ", data)

func send_data(value) -> void:
	var data_to_send = {"value": value}
	var json_string = JSON.stringify(data_to_send)
	udp.put_packet(json_string.to_utf8_buffer())
