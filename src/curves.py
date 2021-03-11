"""
code to generate curves for arbitrary words
"""
import numpy as np

def update_coeff(idx, symb):
    if symb == '0':
        if idx % 2 == 0:
            return 1
        else:
            return -1
    elif symb == '1':
        return 0
    else:
        return np.nan

def get_coeff_arr(word):
    headings = [0]
    for idx, char in enumerate(word):
        update = update_coeff(idx, char)
        if not np.isnan(update):
            headings.append(headings[-1] + update)
    return np.array(headings)

def heading_2_vec(heading, offset=0):
    return np.array([np.cos(heading+offset), np.sin(heading+offset)])

def headings_2_vert(headings, origin=[0,0], offset=0):
    verts = [np.array(origin)]
    for heading in headings:
        step = heading_2_vec(heading)
        position = verts[-1]
        verts.append(position + step)
    return np.array(verts)

def get_curve_and_state(word, alpha, origin=[0,0], offset=np.pi/2):
    angles = alpha * get_coeff_arr(word)
    headings, final_angle = angles[:-1], angles[-1] 
    verts = headings_2_vert(headings, origin, offset)
    return verts, verts[-1], final_angle

def get_curve(word, alpha, origin=[0,0], offset=np.pi/2):
    angles = alpha * get_coeff_arr(word)
    headings = angles[:-1]
    verts = headings_2_vert(headings, origin, offset)
    return verts

def rot_mat(angle):
    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    return R

def norm_mat(endpoint, origin=[0,0]):
    origin = np.array(origin)
    e2e = endpoint - origin
    x,y = e2e
    len_curve = np.linalg.norm(e2e)
    angle_e2e = np.arctan2(x,y)
    return rot_mat(angle_e2e - np.pi/2) / len_curve

def norm_curve(curve, origin = [0,0]):
    mat = norm_mat(curve[-1], origin)
    return np.matmul(mat, curve.T).T

def get_normed_curve(word, alpha, origin=[0,0], offset=np.pi/2):
    curve = get_curve(word, alpha, origin, offset)
    return norm_curve(curve, origin)