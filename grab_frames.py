from pypylon import pylon
import cv2
import sys
import time

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())# диспетчер подключений, уже существующий диспетчер камер, первая подключенная камера
camera.Open()


# camera.AcquisitionFrameRateEnable.SetValue(True)
# camera.AcquisitionFrameRateAbs.SetValue(10)
# converter = pylon.ImageFormatConverter()
# converter.OutputPixelFormat = pylon.PixelType_BGR8packed
# converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned#выравнивание по старшему биту
camera.StartGrabbing()

path='/Users/majagavricenkova/Desktop/frames'
img = pylon.PylonImage()
while camera.IsGrabbing():
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)#возвращение кадра присланного камерой и ошибка и задержка

    if grab_result.GrabSucceeded():
        # img = grab_result.Array

        filename="pylon_img_save" + str(time.time()) + ".tiff" 
        img.AttachGrabResultBuffer(grab_result)
        img.Save(pylon.ImageFileFormat_Tiff, path+filename)
        
        #cv2.imshow("cam",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grab_result.Release()
camera.StopGrabbing()
camera.Close()
cv2.destroyAllWindows()
