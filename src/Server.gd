class_name ServerNode
extends Node

var server: UDPServer
var client: PacketPeerUDP
var data
var python_pid
var last_packet_ms: float = 0
var delay_ms: float
var avg_delay_ms := 0.0
var last_t: float = 0.0

signal data_received

func _ready() -> void:
	server = UDPServer.new()
	server.listen(4242)
	print("Server started at port ", server.get_local_port())
	python_pid = OS.create_process(get_py_interpreter_path(), [get_py_script_path()], true)
	print(python_pid)

func _process(_delta) -> void:
	server.poll()
	if server.is_connection_available():
		client = server.take_connection()
		var packet = client.get_packet()
		print(packet)
		if packet:
			data = JSON.parse_string(packet.get_string_from_utf8())
			print("Accepted peer: %s:%s" % [client.get_packet_ip(), client.get_packet_port()])
			print("Received data: %s" % [packet.get_string_from_utf8()])
			send_data("ACK")
	if client:
		while client.get_available_packet_count() > 0:
			var now := Time.get_ticks_msec()
			var packet: String = client.get_packet().get_string_from_utf8()
			data = JSON.parse_string(packet)
			data_received.emit(data)
			
			if typeof(data) == TYPE_DICTIONARY:
				if data.has("t"):
					var t: float = data["t"]
					if last_t != 0.0:
						delay_ms = (t - last_t) * 1000.0
					last_t = t
					if last_packet_ms != 0:
						delay_ms = now - last_packet_ms
					last_packet_ms = now
					avg_delay_ms = lerp(avg_delay_ms, float(delay_ms), 0.1)


func _notification(what):
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		if python_pid > 0:
			print("Terminating Python process...")
			OS.kill(python_pid)

func stop() -> void:
	get_tree().quit()
	get_tree().root.propagate_notification(NOTIFICATION_WM_CLOSE_REQUEST)

func send_data(to_send: String) -> void:
	client.put_packet(to_send.to_utf8_buffer())

func get_py_script_path() -> String:
	return ProjectSettings.globalize_path("res://TTEA/main.py")

func get_py_interpreter_path() -> String:
	return ProjectSettings.globalize_path("res://TTEA/.venv/Scripts/python.exe")
