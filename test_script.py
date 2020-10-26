import cv2 as cv
import numpy as np
from pypylon import pylon


camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# demonstrate some feature access
new_width = camera.Width.GetValue() - camera.Width.GetInc()
if new_width >= camera.Width.GetMin():
    camera.Width.SetValue(new_width)

numberOfImagesToGrab = 10000
camera.StartGrabbingMax(numberOfImagesToGrab)

converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Convert to OpenCV image format
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv.namedWindow('title', cv.WINDOW_NORMAL)
        cv.imshow('title', img)
        k = cv.waitKey(1)
        if k == 27:
            break
    grabResult.Release()

# Turn off the camera
camera.StopGrabbing()
# close the window

#
# camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# print(camera)
# ret, img = camera.read()
# print(type(img))
#
# cv2.imwrite('color_img.jpg', img)
# cv2.imshow("image", img)
# cv2.waitKey()
