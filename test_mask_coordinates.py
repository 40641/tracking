import numpy as np

zeros = np.zeros((100, 100), dtype=np.uint8)
zeros[:5,:5] = 255

indices = np.where(zeros == [255])
print (indices)
coordinates = zip(indices[0][7], indices[1][7])
print (coordinates)