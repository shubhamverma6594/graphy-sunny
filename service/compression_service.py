import PIL.Image
from io import BytesIO
import numpy as np

def do_compress(data_bytes, story_type):
	if story_type == 1:
		return do_image_compression(data_bytes)

	if story_type == 2:
		return do_video_compression(data_bytes)

def do_image_compression(data_bytes):
	file_like = BytesIO(data_bytes)
	img = PIL.Image.open(file_like)
	width, height = img.size  
	print("do image do_compress")
	left = top = 0
	bottom = height
	right = width

	if width > 600:
		diff = (width - 600) / 2
		left = diff
		right = width - diff
	if height > 1200:
		diff = (width - 600) / 2
		top = diff
		bottom = height - diff
	im1 = img.crop((left, top, right, bottom))

	
	stream = BytesIO()
	im1.save(stream, format="JPEG")
	imagebytes = stream.getvalue()
	return imagebytes