"""
Code to do fractal geometry analysis:
    surface area of simple curves
    volume of simple curves
    find all line segment intersections
"""

import numpy as np
from scipy.spatial import ConvexHull
#from shapely.geometry import LineString
#from shapely.geometry.polygon import LinearRing



def poly_point_pairs(curve):
    pairs = [(x_n, x_np1) for x_n, x_np1 in zip(curve[:-1], curve[1:])]
    pairs.append((curve[-1], curve[0]))
    return pairs

def pppair_2_det(pppair):
    pt_1, pt_2 = pppair
    x1, y1 = pt_1
    x2, y2 = pt_2
    return x1*y2 - x2*y1

def pppair_2_len(pppair):
    pt_1, pt_2 = pppair
    return np.linalg.norm(pt_2 - pt_1)

def simple_surface_area(curve):
    pppairs = poly_point_pairs(curve)
    lens = [pppair_2_len(pppair) for pppair in pppairs]
    return np.sum(lens)

def simple_volume(curve):
    pppairs = poly_point_pairs(curve)
    dets = [pppair_2_det(pppair) for pppair in pppairs]
    return 0.5 * np.sum(dets)

def curve_2_tuples(curve):
    return [(x,y) for x,y in curve]

def is_simple(curve):
    is_simple = False
    tuples = curve_2_tuples(curve)
    lr = LinearRing(tuples)
    try:
        test = lr.area
        is_simple = True
    finally:
        return is_simple

def do_intersect_shp(p_n, p_np1, p_m, p_mp1):
    ln = LineString([tuple(p_n), tuple(p_np1)])
    lm = LineString([tuple(p_m), tuple(p_mp1)])
    return ln.intersects(lm)

def get_intersect(p_n, p_np1, p_m, p_mp1):
    xm1, ym1 = p_m
    xm2, ym2 = p_mp1
    xn1, yn1 = p_n
    xn2, yn2 = p_np1
    slope_n = (yn2 - yn1)/(xn2 - xn1)
    slope_m = (ym2 - ym1)/(xm2 - xm1)
    x_star = (ym1 - yn1 + slope_n * xn1 - slope_m * xm1)/(slope_n - slope_m)
    y_star = slope_n * (x_star - xn1) + yn1
    return [x_star, y_star]

def does_intersect(p_n, p_np1, p_m, p_mp1):
    xm1, ym1 = p_m
    xm2, ym2 = p_mp1
    xn1, yn1 = p_n
    xn2, yn2 = p_np1
    slope_n = (yn2 - yn1)/(xn2 - xn1)
    slope_m = (ym2 - ym1)/(xm2 - xm1)
    x_star = (ym1 - yn1 + slope_n * xn1 - slope_m * xm1)/(slope_n - slope_m)
    y_star = slope_n * (x_star - xn1) + yn1
    cond_x = min(xn1,xn2) <= x_star <= max(xn1,xn2)
    cond_y = min(yn1,yn2) <= y_star <= max(yn1,yn2)
    return cond_x and cond_y

def cclockwise_order(p1,p2,p3):
    slope_12 = (p3[1] - p1[1]) * (p2[0] - p1[0])
    slope_13 = (p2[1] - p1[1]) * (p3[0] - p1[0])
    # those are not errors, i think
    return slope_12 > slope_13   

def do_intersect_ccw(p_n, p_np1, p_m, p_mp1):
    cond_n = cclockwise_order(p_n,p_m,p_mp1) != cclockwise_order(p_np1,p_m,p_mp1)
    cond_m = cclockwise_order(p_n,p_np1,p_m) != cclockwise_order(p_n,p_np1,p_mp1)
    return cond_n and cond_m

def intersects(curve):
    '''
    returns list of intersections, if at=None then there was a div by 0 issue
    '''
    pppairs = poly_point_pairs(curve)
    buffer = 2
    intersect_list = []
    for n, (p_n, p_np1) in enumerate(pppairs[:-buffer]):
        pppairs_ahead = pppairs[n + buffer:]
        for k, (p_m, p_mp1) in enumerate(pppairs_ahead):
            m = n + k + buffer
            if np.linalg.norm(p_n-p_m)<2.5 and k>5 and does_intersect(p_n, p_np1, p_m, p_mp1):
                try:
                    point = get_intersect(p_n, p_np1, p_m, p_mp1)
                except:
                    point = None    
                desc = {'n':n, 'm':m, 'at':point}
                intersect_list.append(desc)
    return intersect_list

def complex_to_simples(curve, intersect_list):
    '''
    https://web.archive.org/web/20100805164131/http://www.cis.southalabama.edu/~hain/general/Theses/Subramaniam_thesis.pdf

    '''
    simples = []
    smallest = sorted(intersect_list, key=lambda d: d['m']-d['n'])
    base = curve
    for intersect in intersect_list:
        pass

    





def convex_hull(curve, len_line_seg=None):
    # need to configure to keep maximum hull line segment length small
    # enough to include non-overlapped points
    
    if len_line_seg is None:
        deltas = curve[:-1] - curve[1:]
        dists = np.linalg.norm(deltas, axis=1)
        dmin, dmax, dmean = np.amin(dists), np.amax(dists), np.mean(dists)

        double_deltas = curve[:-2] - curve[2:]
        double_dists = np.linalg.norm(double_deltas, axis=1)
        ddmin, ddmax, ddmean = np.amin(double_dists), np.amax(double_dists), np.mean(double_dists)

        #expectations:

        # dmean:
        # dmean = dmin = dmax; give or take some rounding error

        # ddmax:
        # ddmax = 2*dmean (2 line segments, no change in heading)

        # ddmin:
        # ddmin = 2 line segments, one bend at angle alpha
        # ddmin = len of 3rd leg of isoceles triangle where angle is alpha and leg len is dmean
        # ddmin = dmean * sin(alpha) / sin((pi - alpha)/2)
        # ddmin = dmean * 2 sin(alpha / 2)

        # ddmean:
        # dmean * 2sin(alpha/2) <= ddmean <= 2 dmean 
        # let the ratio of 1's to 0's be r_c
        # ddmean = 2 dmean (r_c + (1-r_c) sin(alpha/2))

    hull = ConvexHull(curve)
    return hull