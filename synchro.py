from pypylon import pylon
import cv2
from pypylon import genicam
import time


path="/Users/majagavricenkova/Desktop/frames"#прописать свой путь
tl_factory=pylon.TlFactory.GetInstance()
devices=tl_factory.EnumerateDevices()

cameras=pylon.InstantCameraArray(2)#захват нескольких камер
for i,cam in enumerate(cameras):
    cam.Attach(tl_factory.CreateDevice(devices[i]))#привязывает объект кам к реальной физической камере из списка девайсов
    cam.SetCameraContext(i)#к каждой камере номер
    cam.Open()
    node_map = cam.GetNodeMap()
    packet_size = node_map.GetNode("GevSCPSPacketSize")
    scp_delay = node_map.GetNode("GevSCPD")
    if cam.GetDeviceInfo().GetDeviceClass()=='BaslerGigE':
       
        packet_size.SetValue(1440)#размер udp пакета
     
        scp_delay.SetValue(10000)#задержка между отправкой
master=cameras[0]
master.TriggerSelector.SetValue("AcquisitionStart")
master.TriggerMode.SetValue("On")
master.TriggerSource.SetValue("Software")
master.TriggerActivation.SetValue("RisingEdge")

slave=cameras[1]
slave.TriggerSelector.SetValue("AcquisitionStart")
slave.TriggerMode.SetValue("On")
slave.LineSelector.SetValue("Line1")
slave.LineMode.SetValue("Input")
slave.TriggerSource.SetValue("Line1")
slave.TriggerActivation.SetValue("RisingEdge")
slave.TriggerDelayAbs.SetValue(0.0002)

cameras.StartGrabbing()
try:
    for i in range(100):
            master.ExecuteSoftwareTrigger()
            time.sleep(0.05)
        # for _ in range(2):
            res=cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            context=res.GetCameraContext()#каждый раз узнаем от кого пришел кадр
            img=pylon.PylonImage()
            img.AttachGrabResultBuffer(res)
            filename="pylon_img_save" + str(time.time()) + str(context)+".tiff" 
            img.Save(pylon.ImageFileFormat_Tiff, path+filename)
            res.Release()
finally:
    cam.StopGrabbing()
    for cam in cameras:
        cam.Close()
# print(master.LineMode.GetSymbolics())
# for line in master.LineSelector.GetSymbolics():
#     master.LineSelector.SetValue(line)
#     modes = master.LineMode.GetSymbolics()
#     print(f"{line}: {modes}")
# slave.StartGrabbing()
# # img_master = pylon.PylonImage()
# # img_slave=pylon.PylonImage()
# # path='/Users/maya/Desktop/frames/'

# #master.ExecuteSoftwareTrigger()

# # converter = pylon.ImageFormatConverter()
# # converter.OutputPixelFormat = pylon.PixelType_BGR8packed
# # converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# try:
#     while master.IsGrabbing() and slave.IsGrabbing():
#         #master.AcquisitionStart.Execute()
#         master.ExecuteSoftwareTrigger()
#         master_gr = master.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
#         slave_gr = slave.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

#         if master_gr.GrabSucceeded() and slave_gr.GrabSucceeded():
#             filename_master="pylon_img_master_save" + str(time.time()) + ".tiff" 
#             filename_slave="pylon_img_slave_save" + str(time.time()) + ".tiff" 
#             # master_img = converter.Convert(master_gr).GetArray()
#             # slave_img = converter.Convert(slave_gr).GetArray()
#             img_master.AttachGrabResultBuffer(master_gr)
#             img_slave.AttachGrabResultBuffer(slave_gr)
#             img_master.Save(pylon.ImageFileFormat_Tiff, path+filename_master)
#             img_slave.Save(pylon.ImageFileFormat_Tiff, path+filename_slave)
#             # cv2.imshow("Master", img_master)
#             # cv2.imshow("Slave", img_slave)

#             # if cv2.waitKey(1) & 0xFF == ord('q'):
#             #     break

#         master_gr.Release()
#         slave_gr.Release()

# finally:
#     master.StopGrabbing()
#     slave.StopGrabbing()
#     master.Close()
#     slave.Close()
#     cv2.destroyAllWindows()
