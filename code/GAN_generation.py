from PIL import Image
import os
import os.path

# imgs = list()
# path = 'images'
# valid_images = [".jpg", ".gif", ".png", ".tga", ".tiff"]
# for f in os.listdir(path):
#     ext = os.path.splitext(f)[1]
#     if ext.lower in valid_images:
#         continue
#     imgs.append(Image.open(os.path.join(path, f)))

# src_img = Image.open('images/Peak_District_False_Colour.jpeg')
# src_img.show()

from keras.datasets.cifar10 import load_data
# load the images into memory
(trainX, trainy), (testX, testy) = load_data()
# summarize the shape of the dataset
print('Train', trainX.shape, trainy.shape)
print('Test', testX.shape, testy.shape)


# plot raw pixel data
pyplot.imshow(trainX[i])
