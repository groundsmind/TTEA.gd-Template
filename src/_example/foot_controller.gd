extends Node2D

@onready var left_foot: Node2D = $"Left Foot"
@onready var right_foot: Node2D = $"Right Foot"

var feet_pos: Dictionary = {
	"left": [0.0,0.0],
	"right": [0.0,0.0],
}
var scr_size_x = 1600
var scr_size_y = 1200

func _process(_delta: float) -> void:
	if get_data():
		feet_pos = get_data()
	if feet_pos["left"][0] != null:
		var left_pos = Vector2(scr_size_x-feet_pos["left"][0], scr_size_y-feet_pos["left"][1])
		var right_pos = Vector2(scr_size_x-feet_pos["right"][0], scr_size_y-feet_pos["right"][1])
		print(left_pos, right_pos)
		left_foot.global_position = left_pos
		right_foot.global_position = right_pos

func get_data():
	var data = TteaComm.data
	return data
