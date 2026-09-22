extends Node2D

@export var vertical_offset: float = 100.0
@export var offset_threshold: float = 20.0

@onready var left_foot: Node2D = $"Left Foot"
@onready var right_foot: Node2D = $"Right Foot"
@onready var midpoint: Node2D = $midpoint
@onready var left_label: Label = $"Left Foot/Sprite2D/Label"
@onready var right_label: Label = $"Right Foot/Sprite2D/Label"

var feet_pos: Dictionary = {
	"left": [0.0,0.0],
	"right": [0.0,0.0],
}
var scr_size_x = 1600
var scr_size_y = 1200

func _process(delta: float) -> void:
	if get_data() is Dictionary:
		feet_pos = get_data()
	if feet_pos["left"][0] != null:
		var left_pos = Vector2(scr_size_x - feet_pos["left"][0], (scr_size_y - feet_pos["left"][1]) - vertical_offset)
		var right_pos = Vector2(scr_size_x - feet_pos["right"][0], (scr_size_y - feet_pos["right"][1]) - vertical_offset)
		if abs(left_foot.global_position.x - left_pos.x) >= offset_threshold or abs(left_foot.global_position.y - left_pos.y) >= offset_threshold:
			left_foot.global_position = lerp(left_foot.global_position, left_pos, delta*10)
		if abs(right_foot.global_position.x - right_pos.x) >= offset_threshold or abs(right_foot.global_position.y - right_pos.y) >= offset_threshold:
			right_foot.global_position = lerp(right_foot.global_position, right_pos, delta*10)
		midpoint.global_position = left_foot.global_position.lerp(right_foot.global_position, 0.5)
		left_label.text = str(left_pos)
		right_label.text = str(right_pos)

func get_data():
	var data = Server.data
	return data
