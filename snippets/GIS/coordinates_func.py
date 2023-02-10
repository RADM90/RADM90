from rasterio import warp, crs


def for_map(dataset, targetEPSG):
    gt = dataset.read_transform()
    new_crs = crs.CRS.from_epsg(targetEPSG)
    old_crs = dataset.crs
    x_base = gt[0]
    y_base = gt[3]
    x_geo = gt[0] + dataset.width * gt[1] + dataset.height * gt[2]
    y_geo = gt[3] + dataset.width * gt[4] + dataset.height * gt[5]
    '''
    gt[0] : x-coordinate of the upper-left corner of the upper-left pixel.
    gt[1] : west-east pixel resolution / pixel width.
    gt[2] : row rotation (typically zero).
    gt[3] : y-coordinate of the upper-left corner of the upper-left pixel.
    gt[4] : column rotation (typically zero).
    gt[5] : north-south pixel resolution / pixel height (negative value for a north-up image).
    '''
    new_x_base, new_y_base = warp.transform(old_crs, new_crs, xs=[x_base], ys=[y_base])
    new_x_geo, new_y_geo = warp.transform(old_crs, new_crs, xs=[x_geo], ys=[y_geo])

    top_left = [new_y_base[0], new_x_base[0]]
    bottom_right = [new_y_geo[0], new_x_geo[0]]

    return top_left, bottom_right


def for_coordinates(oldEPSG, targetEPSG, x, y):
    old_crs = crs.CRS.from_epsg(oldEPSG)
    new_crs = crs.CRS.from_epsg(targetEPSG)
    new_x_base, new_y_base = warp.transform(old_crs, new_crs, xs=[x], ys=[y])

    return new_y_base[0], new_x_base[0]