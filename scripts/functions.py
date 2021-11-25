from scripts.config import img_extensions

def is_file_an_img(a_file):
	is_image = [file_extn in a_file for file_extn in img_extensions]
	is_image = any(is_image)
	return is_image
