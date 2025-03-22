import bpy

# Expanded SIGN_MAP: English word -> list of (frame, bone, action, rotation)
SIGN_MAP = {
    'hello': [
        (0, 'hand.R', 'rotate', (0, 0, 45)),  # Wave at frame 0
        (10, 'hand.R', 'rotate', (0, 0, -45)), # Wave back at frame 10
        (20, 'hand.R', 'rotate', (0, 0, 0))   # Reset at frame 20
    ],
    'friend': [
        (0, 'hand.R', 'rotate', (0, 45, 0)),  # Handshake start
        (10, 'hand.L', 'rotate', (0, -45, 0)),# Mirror with left hand
        (20, 'hand.R', 'rotate', (0, 0, 0)),  # Reset
        (20, 'hand.L', 'rotate', (0, 0, 0))
    ],
    'good': [
        (0, 'hand.R', 'rotate', (90, 0, 0)),  # Thumb up
        (20, 'hand.R', 'rotate', (0, 0, 0))   # Reset
    ],
    'thank you': [
        (0, 'hand.R', 'rotate', (0, 0, 90)),   # Hand up near mouth
        (10, 'hand.R', 'rotate', (0, 0, 0)),   # Hand down
        (20, 'hand.R', 'rotate', (0, 0, 0))    # Reset
    ],
    'yes': [
        (0, 'hand.R', 'rotate', (0, 0, 30)),   # Nod hand up
        (10, 'hand.R', 'rotate', (0, 0, -30)), # Nod hand down
        (20, 'hand.R', 'rotate', (0, 0, 0))    # Reset
    ],
    'no': [
        (0, 'hand.R', 'rotate', (0, 30, 0)),   # Shake hand left
        (10, 'hand.R', 'rotate', (0, -30, 0)), # Shake hand right
        (20, 'hand.R', 'rotate', (0, 0, 0))    # Reset
    ]
}

def generate_sign_animation(english_text):
    bpy.ops.wm.open_mainfile(filepath='blender/sign_avatar.blend')
    armature = bpy.data.objects.get('Armature')
    if not armature:
        print("Armature not found!")
        return None

    armature.animation_data_clear()
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 100

    words = english_text.lower().split()
    current_frame = 0

    for word in words:
        if word in SIGN_MAP:
            for frame_offset, bone_name, action, rotation in SIGN_MAP[word]:
                frame = current_frame + frame_offset
                bpy.context.scene.frame_set(frame)
                bone = armature.pose.bones.get(bone_name)
                if bone:
                    if action == 'rotate':
                        bone.rotation_euler = rotation
                        bone.keyframe_insert(data_path="rotation_euler", frame=frame)
        current_frame += 30

    bpy.context.scene.render.filepath = 'static/animations/output.mp4'
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.ops.render.render(animation=True)

    return '/static/animations/output.mp4'

if __name__ == "__main__":
    test_text = "hello friend"
    result = generate_sign_animation(test_text)
    print(f"Animation saved at: {result}")