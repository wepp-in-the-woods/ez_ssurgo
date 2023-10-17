from urllib.request import urlopen

from os.path import exists as _exists

import numpy as np

def isfloat(f):
    # noinspection PyBroadException
    try:
        float(f)
        return True
    except Exception:
        return False


wmesque_url = 'https://wepp.cloud/webservices/wmesque/'


def read_tif(fn, dtype=np.float64, band=1):
    """
    use gdal to read an tif file and return the data and the
    transform
    """
    assert _exists(fn), "Cannot open %s" % fn

    ds = gdal.Open(fn)
    assert ds is not None

    transform = ds.GetGeoTransform()
    data = np.array(ds.GetRasterBand(band).ReadAsArray(), dtype=dtype).T
    wkt_text = ds.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt_text)
    proj = srs.ExportToProj4().strip()

    del ds

    data = np.array(data, dtype=dtype)

    return data, transform, proj


def wmesque_retrieve(dataset, extent, fname, cellsize, resample=None):
    global wmesque_url

    assert isfloat(cellsize)

    assert all([isfloat(v) for v in extent])
    assert len(extent) == 4

    extent = ','.join([str(v) for v in extent])

    if fname.lower().endswith('.tif'):
        fmt = 'GTiff'

    elif fname.lower().endswith('.asc'):
        fmt = 'AAIGrid'

    elif fname.lower().endswith('.png'):
        fmt = 'PNG'

    else:
        raise ValueError('fname must end with .tif, .asc, or .png')

    url = f'{wmesque_url}{dataset}/?bbox={extent}&cellsize={cellsize}&format={fmt}'

    if resample is not None:
        url += f'&resample={resample}'

    try:
        output = urlopen(url, timeout=60)
        with open(fname, 'wb') as fp:
            fp.write(output.read())
    except Exception:
        raise Exception("Error retrieving: %s" % url)

    return 1