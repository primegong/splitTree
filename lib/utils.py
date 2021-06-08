import numpy as np
import colorsys
import webcolors

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def randomColor(labels):
	num = len(labels)
	colors = [colorsys.hsv_to_rgb(i/num, 1, 1) for i in range(num)]
	colors = [(int(c[0]) *255, int(c[1]) *255, int(c[2]) *255) for c in colors]
	return colors

def getBbox(triangles):
	triangles = np.array(triangles)
	# print(triangles.shape)
	points_3D = np.reshape(triangles,(-1,3))
	# print(points_3D.shape)
	[x_1, y_1, z_1] = np.min(points_3D, axis = 0)
	[x_2, y_2, z_2] = np.max(points_3D, axis = 0)
	bbox = [x_1, y_1, z_1, x_2, y_2, z_2]
	return bbox

def getVolume(bbox):
	[x_1, y_1, z_1, x_2, y_2, z_2] = bbox
	delta_x = x_2-x_1
	delta_y = y_2-y_1
	delta_z = z_2-z_1
	volume = abs(delta_x * delta_y * delta_z)
	return volume

def getOverlapVolume(bbox1, bbox2):
	[overlap_x1, overlap_y1,overlap_z1] = np.maximum(bbox1[:3], bbox2[:3])
	[overlap_x2, overlap_y2,overlap_z2] = np.minimum(bbox1[3:], bbox2[3:])

	overlap_volume = 0
	if (overlap_x1 < overlap_x2 and overlap_y1 < overlap_y2 and overlap_z1 < overlap_z2 ):
		delta_ox = overlap_x2 - overlap_x1
		delta_oy = overlap_y2 - overlap_y1
		delta_oz = overlap_z2 - overlap_z1
		overlap_volume = delta_ox * delta_oy *delta_oz
	return overlap_volume
