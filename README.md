# OpenVino-Face-Recognition
![image](https://github.com/MisterFoziljon/OpenVino-Face-Recognition/blob/main/source/openvino.png)
## Introduction
- [```OpenVINO```](https://docs.openvino.ai/2023.1/home.html) toolkit (yoki Intel Distribution of ```OpenVINO``` Toolkit) - bu dasturchilarga turli xil video tizimlarda foydalanish uchun yuqori samarali yechimlarni ishlab chiqishni tezlashtirishga yordam beradigan ochiq va bepul vositalar to'plami.
  * Computer Visionni to'liq qo'llab-quvvatlaydi
  * Deep Learning algoritmlarini qo'llashni soddalashtiradi
  * Bir nechta Intel platformalarida oson bajarish imkonini beradi.
    
- ```OpenVINO``` turli xil muammolarni, jumladan Face Detection, Automatic Object Recognition, Text and Speech Recognition, Image Processing va boshqalar bilan ishlashda qo'l keladi.

## Main
* Face Recognition - bu shaxslarni yuz xususiyatlariga qarab aniqlash yoki tekshirishni o'z ichiga olgan texnologiya. Bu biometrik identifikatsiyaning bir shakli bo'lib, unda shaxs yuzining o'ziga xos xususiyatlari tahlil qilinadi va autentifikatsiya yoki identifikatsiya qilish uchun foydalaniladi. Yuzni tanib olishdan asosiy maqsad - odamlarning yuz xususiyatlarini ma'lum yuzlar ma'lumotlar bazasi bilan solishtirish orqali aniqlashdir.

* ```Open Vino``` yordamida Face Recognition texnologiyasidan foydalanish mumkin. Bunda quyidagi texnologiyalar qo'llaniladi:
   - Face Detection
   - Face Landmarks Detection
   - Face Reidentificaton
![image](https://github.com/MisterFoziljon/OpenVino-Face-Recognition/blob/main/source/face.jpg)


## Requirements
* Microsoft Visual Studio 2022
* Python 3.7 - 3.11 (64-bit)
```cmd
pip install openvino
pip install opencv-python
pip install streamlit
pip install scipy
```

* OpenVino Core Components
```console
cd C:\Users\<YOUR_USERNAME>
mkdir "C:\Program Files (x86)\Intel"
cd Downloads
curl -L https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.1/windows/w_openvino_toolkit_windows_2023.1.0.12185.47b736f63ed_x86_64.zip --output openvino_2023.1.0.zip
tar -xf openvino_2023.1.0.zip
ren w_openvino_toolkit_windows_2023.1.0.10926.b4452d56304_x86_64 openvino_2023.1.0
move openvino_2023.1.0 "C:\Program Files (x86)\Intel"
cd "C:\Program Files (x86)\Intel\openvino_2023.1.0"
call setupvars.bat
```

## Data
  - yuzlarni tanib olish uchun ilova yuzlar bazasi va galereyadan foydalanadi. ```data``` - odamlar tasvirlari bo'lgan folder.
  - ```data``` nomli folder yarating. Ushbu folderdagi tasvirlar istalgan o'lchamda bo'lishi mumkin.
  - Tasvirlar bir yoki bir nechta old tomonga yo'naltirilgan sifatli yuzlarni o'z ichiga olgan bo'lishi kerak.
  - Tasvirlarni quyidagidek indexlash kerak: {Odam_ismi}-{id}.jpg
  - Bitta odamning bir nechta tasviri bo'lishi mumkin:
      - Ali-0.jpg
      - Ali-1.jpg
      - ...
      - Ali-n.jpg

## Usage
```python
streamlit run deploy.py
```

## Example
![image](https://github.com/MisterFoziljon/OpenVino-Face-Recognition/blob/main/source/example.gif)
