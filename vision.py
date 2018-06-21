import numpy as np
import cv2
import yaml


def main():
    calibrate_color()

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
        if cv2.waitKey(1) == 115:
            print param
            with open('data.yml', 'w') as outfile:
                yaml.dump(param, outfile, default_flow_style=False)
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
