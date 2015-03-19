from PIL import Image
import glob, os, fnmatch

X_MAX = 1920.0
Y_MAX = 1080.0

RESIZED_IMAGE_POSTFIX = '_R'
RESIZED_IMAGE_DIR = 'images'
RESIZED_IMAGE_EXT = '.jpg'

THUMBNAIL_DIR = 'thumbnails'
THUMBNAIL_EXT = '.thumb.jpg'

if __name__ == '__main__':
	images = []
	for root, dirnames, filenames in os.walk('.'):
		if RESIZED_IMAGE_DIR in root or THUMBNAIL_DIR in root:
			continue
		for filename in fnmatch.filter(filenames, '*.jp*g'):
			images.append(os.path.join(root, filename))
	
	if not os.path.exists(RESIZED_IMAGE_DIR):
		os.mkdir(RESIZED_IMAGE_DIR)
		print 'Image directory created'
	if not os.path.exists(THUMBNAIL_DIR):
		os.mkdir(THUMBNAIL_DIR)
		print 'Thumbnail directory created'
	
	print images
	
	for jpg in images:
		file, ext = os.path.splitext(jpg)
		path, filename = os.path.split(jpg)
		if os.path.exists(os.path.join(RESIZED_IMAGE_DIR, file + RESIZED_IMAGE_POSTFIX + RESIZED_IMAGE_EXT)):
			continue
			
		img = Image.open(jpg)
		
		x_new, y_new = 0, 0
		x_org, y_org = img.size
		
		print 'org:', x_org, y_org
		
		if (x_org / y_org) >= 1:
			x_new = (Y_MAX / y_org) * x_org
			y_new = Y_MAX
		else:
			x_new = X_MAX
			y_new = (X_MAX / x_org) * y_org
			
		print 'new: ', x_new, y_new
		
		if not os.path.exists(os.path.join(RESIZED_IMAGE_DIR, path)):
			os.makedirs(os.path.join(RESIZED_IMAGE_DIR, path))
		if not os.path.exists(os.path.join(THUMBNAIL_DIR, path)):
			os.makedirs(os.path.join(THUMBNAIL_DIR, path))
		
		img = img.resize([int(x_new), int(y_new)], Image.ANTIALIAS)
		img.save(os.path.join(RESIZED_IMAGE_DIR, file + RESIZED_IMAGE_POSTFIX + RESIZED_IMAGE_EXT), 'JPEG')
		print 'Image saved'
		
		img.thumbnail([128, 128], Image.ANTIALIAS)
		img.save(os.path.join(THUMBNAIL_DIR, file + THUMBNAIL_EXT), 'JPEG')
		print 'Thumbnail saved'
	
