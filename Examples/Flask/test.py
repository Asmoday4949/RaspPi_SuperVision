from web_cam import SharedCamera

camera = SharedCamera.get_instance()
camera.print()
print(camera)
camera = SharedCamera.get_instance()
camera.print()
print(camera)
