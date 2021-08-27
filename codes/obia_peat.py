import numpy as np
import gdal
from skimage import exposure
from skimage.segmentation import quickshift
import time

naip_fn = '/Users/arpanganguli/Documents/GitHub/PEAT/images/PNG/Outer_Hebrides_with_Grips_5.png'

driverTiff = gdal.GetDriverByName('GTiff')
naip_ds = gdal.Open(naip_fn)
nbands = naip_ds.RasterCount
band_data = []
print('bands', naip_ds.RasterCount, 'rows', naip_ds.RasterYSize, 'columns',
      naip_ds.RasterXSize)
for i in range(1, nbands+1):
    band = naip_ds.GetRasterBand(i).ReadAsArray()
    band_data.append(band)
band_data = np.dstack(band_data)