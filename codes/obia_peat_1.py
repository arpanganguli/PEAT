import numpy as np
import gdal
import scipy
from skimage import exposure
from skimage.segmentation import quickshift, slic
import time

source_image = '/Users/arpanganguli/Documents/GitHub/PEAT/images/TIF/Scotland_1.tif'

driverTiff = gdal.GetDriverByName('GTiff')
image_ds = gdal.Open(source_image)
nbands = image_ds.RasterCount
band_data = []
print('bands', image_ds.RasterCount, 'rows', image_ds.RasterYSize, 'columns',
      image_ds.RasterXSize)
for i in range(1, nbands + 1):
    band = image_ds.GetRasterBand(i).ReadAsArray()
    band_data.append(band)
band_data = np.dstack(band_data)

# scale image values from 0.0 - 1.0
img = exposure.rescale_intensity(band_data)

# do segmentation multiple options with quickshift and slic
seg_start = time.time()
# segments = quickshift(img, convert2lab=False)
# segments = quickshift(img, ratio=0.8, convert2lab=False)
# segments = quickshift(img, ratio=0.99, max_dist=5, convert2lab=False)
# segments = slic(img, n_segments=100000, compactness=0.1)
# segments = slic(img, n_segments=500000, compactness=0.01)
segments = slic(img, n_segments=5_000, compactness=0.1)
print('segments complete', time.time() - seg_start)

# save segments to raster
segments_fn = '/Users/arpanganguli/Documents/GitHub/PEAT/export/segments.tif'
segments_ds = driverTiff.Create(segments_fn, image_ds.RasterXSize, image_ds.RasterYSize,
                                3, gdal.GDT_Float32)
segments_ds.SetGeoTransform(image_ds.GetGeoTransform())
segments_ds.SetProjection(image_ds.GetProjectionRef())
segments_ds.GetRasterBand(1).WriteArray(segments)
segments_ds = None


def segment_features(segment_pixels):
    features = []
    npixels, nbands = segment_pixels.shape
    for b in range(nbands):
        stats = scipy.stats.describe(segment_pixels[:, b])
        band_stats = list(stats.minmax) + list(stats)[2:]
        if npixels == 1:
            # in this case the variance = nan, change it 0.0
            band_stats[3] = 0.0
        features += band_stats
    return features


segment_ids = np.unique(segments)
objects = []
object_ids = []
for id in segment_ids:
    segment_pixels = img[segments == id]
    object_features = segment_features(segment_pixels)
    objects.append(object_features)
    object_ids.append(id)

