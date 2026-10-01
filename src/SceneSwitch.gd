extends Node

var previous_scene: String = ""

func switch_scene(next) -> void:
	previous_scene = get_tree().current_scene.scene_file_path
	get_tree().change_scene_to_file(next)

func switch_to_previous() -> void:
	var old_prev: String = previous_scene
	previous_scene = get_tree().current_scene.scene_file_path
	get_tree().change_scene_to_file(old_prev)
