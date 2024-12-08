import torch
from tkinter import Tk, Button, Label, filedialog, OptionMenu, StringVar
from PIL import Image, ImageTk
import cv2
import numpy as np

# تحميل نموذج YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)


# إعداد الواجهة
window = Tk()
window.title("كاشف الأشياء")
window.geometry("800x600")

# اللغة الافتراضية
language_var = StringVar(window)
language_var.set("English")  # اللغة الافتراضية

# نصوص الواجهة بناءً على اللغة
texts = {
    "English": {
        "choose_image": "Choose Image",
        "language": "Language",
        "title": "Object Detector"
    },
    "Arabic": {
        "choose_image": "اختيار صورة",
        "language": "اللغة",
        "title": "كاشف الأشياء"
    },
    "French": {
        "choose_image": "Choisir une image",
        "language": "Langue",
        "title": "Détecteur d'objets"
    }
}

# دالة لتحديث الواجهة بناءً على اللغة المختارة
def change_language(*args):
    selected_language = language_var.get()
    button_choose.config(text=texts[selected_language]["choose_image"])
    language_options.config(text=texts[selected_language]["language"])
    window.title(texts[selected_language]["title"])

# تحميل صورة وتحليلها
def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        detect_objects(file_path)

# كشف الكائنات ووضع مربعات التحديد
def detect_objects(img_path):
    img = Image.open(img_path)
    img_np = np.array(img)

    # تطبيق النموذج
    results = model(img_np)

    # إضافة مربعات التحديد حول العناصر المكتشفة بدون تغيير الألوان
    for box in results.xyxy[0]:  # استخدام صيغة xyxy
        x1, y1, x2, y2 = map(int, box[:4])
        label = results.names[int(box[5])]
        # رسم مربع التحديد والنص فقط
        cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # تحويل الصورة المعدلة لعرضها في tkinter
    img_with_boxes = Image.fromarray(img_np)
    img_tk = ImageTk.PhotoImage(img_with_boxes)
    label_img.config(image=img_tk)
    label_img.image = img_tk

# عناصر واجهة المستخدم
button_choose = Button(window, text=texts["English"]["choose_image"], command=load_image)
button_choose.pack()

language_options = OptionMenu(window, language_var, "English", "Arabic", "French", command=change_language)
language_options.config(text=texts["English"]["language"])
language_options.pack()

label_img = Label(window)
label_img.pack()

# استدعاء تحديث اللغة عند اختيار لغة جديدة
language_var.trace("w", change_language)

window.mainloop()
