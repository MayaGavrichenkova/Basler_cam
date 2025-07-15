from pypylon import pylon
import cv2
from pypylon import genicam
import time
tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()
master = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
slave = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))

master.Open()
slave.Open()
# print(master.LineMode.GetSymbolics())
# for line in master.LineSelector.GetSymbolics():
#     master.LineSelector.SetValue(line)
#     modes = master.LineMode.GetSymbolics()
#     print(f"{line}: {modes}")
master.TriggerSelector.SetValue("AcquisitionStart")
master.TriggerMode.SetValue("On")
master.TriggerSource.SetValue("Software")
master.TriggerActivation.SetValue("RisingEdge")



master.LineSelector.SetValue("Out1")
master.LineMode.SetValue("Output")
master.LineSource.SetValue("ExposureActive")
master.LineFormat.SetValue('OptoCoupled')

slave.LineSelector.SetValue("Line1")
slave.LineMode.SetValue("Input")

slave.TriggerSelector.SetValue("AcquisitionStart")
slave.TriggerMode.SetValue("On")
slave.TriggerSource.SetValue("Line1")
slave.TriggerActivation.SetValue("RisingEdge")
slave.TriggerDelayAbs.SetValue(0.0002)

slave.StartGrabbing()
master.StartGrabbing()
img_master = pylon.PylonImage()
img_slave=pylon.PylonImage()
path='/Users/maya/Desktop/frames/'

#master.ExecuteSoftwareTrigger()

# converter = pylon.ImageFormatConverter()
# converter.OutputPixelFormat = pylon.PixelType_BGR8packed
# converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

try:
    while master.IsGrabbing() and slave.IsGrabbing():
        #master.AcquisitionStart.Execute()
        master.ExecuteSoftwareTrigger()
        master_gr = master.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        slave_gr = slave.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if master_gr.GrabSucceeded() and slave_gr.GrabSucceeded():
            filename_master="pylon_img_master_save" + str(time.time()) + ".tiff" 
            filename_slave="pylon_img_slave_save" + str(time.time()) + ".tiff" 
            # master_img = converter.Convert(master_gr).GetArray()
            # slave_img = converter.Convert(slave_gr).GetArray()
            img_master.AttachGrabResultBuffer(master_gr)
            img_slave.AttachGrabResultBuffer(slave_gr)
            img_master.Save(pylon.ImageFileFormat_Tiff, path+filename_master)
            img_slave.Save(pylon.ImageFileFormat_Tiff, path+filename_slave)
            # cv2.imshow("Master", img_master)
            # cv2.imshow("Slave", img_slave)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        master_gr.Release()
        slave_gr.Release()

finally:
    master.StopGrabbing()
    slave.StopGrabbing()
    master.Close()
    slave.Close()
    cv2.destroyAllWindows()
