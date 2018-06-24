import numpy as np
import cv2
import yaml


def main():
    op = raw_input('Calibrate? (y/n)\n')
    if op == 'y':
        calibrate_color()
    find_object()

def nothing(x):
    pass

def calibrate_color():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow('HSV')
    cv2.createTrackbar("Hmin", "HSV",0,360,nothing)
    cv2.createTrackbar("Hmax", "HSV",0,360,nothing)
    cv2.createTrackbar("Smin", "HSV",0,255,nothing)
    cv2.createTrackbar("Smax", "HSV",0,255,nothing)
    cv2.createTrackbar("Vmin", "HSV",0,255,nothing)
    cv2.createTrackbar("Vmax", "HSV",0,255,nothing)

    param = {}

    while True:
        ret_val, img = cam.read()
        cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # get current positions of four trackbars
        h_min = cv2.getTrackbarPos('Hmin','HSV')
        h_max = cv2.getTrackbarPos('Hmax','HSV')
        s_min = cv2.getTrackbarPos('Smin','HSV')
        s_max = cv2.getTrackbarPos('Smax','HSV')
        v_min = cv2.getTrackbarPos('Vmin','HSV')
        v_max = cv2.getTrackbarPos('Vmax','HSV')

        minHSV = np.array([h_min, s_min, v_min])
        maxHSV = np.array([h_max, s_max, v_max])

        param['minHSV'] = minHSV.tolist()
        param['maxHSV'] = maxHSV.tolist()

        mask = cv2.inRange(img, minHSV, maxHSV)

        # cv2.imshow('CAM',img)
        cv2.imshow('HSV',mask)
        cv2.imshow('Source',img)
        if cv2.waitKey(1) == 115:
            print param
            with open('data.yml', 'w') as outfile:
                yaml.dump(param, outfile, default_flow_style=False)
            break
    cv2.destroyAllWindows()


def find_object():

    cam = cv2.VideoCapture(0)

    with open("data.yml", 'r') as stream:
        try:
            param = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    minHSV = np.array(param['minHSV'])
    maxHSV = np.array(param['maxHSV'])


    while True:
        ret_val, img = cam.read()
        cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(img, minHSV, maxHSV)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        img = draw_biggest_contour(contours, img)
        cv2.imshow('CONTOURS',img)

        if cv2.waitKey(1) == 27:
            break


def draw_biggest_contour(contours, img):
    min_area = 0
    if len(contours) > 0:
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    return img


if __name__ == "__main__":
    main()
