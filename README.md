# Basler_cam
https://github.com/basler/pypylon/tree/master - гит с хорошим кодом для basler

Для корректной работы кода синхронизации на macOS необходимо:
Указать тип камеры, в случае работы с acA 1600 60 gm- GigEcamera
Ограничить размер посыдаемых пакетов 
Прописать задержку между пакетами от двух камер


На macOS от Basler совместим только Basler Socket Driver- не настоящий драйвер, а способ взаимодействия через стандартный сокет
Ссылка на источник: https://assets-ctf.baslerweb.com/dg51pdwahxgw/2cevzPRHqqWzf1tiQh6rgn/e562d5084d6fd699c077ec45c27497d3/AW00144501000_GigE_Vision_Network_Drivers_and_Bandwidth_Management.pdf?utm_source=chatgpt.com 