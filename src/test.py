import numpy as np
im = np.random.randint(0, 256, (2, 3, 3))
print(im)
im_reversed = im[..., ::-1]
print(im_reversed)
