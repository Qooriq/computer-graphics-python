import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer-Graphics")
        self.root.geometry("1200x720")

        self.frame = Frame(self.root)
        self.frame.pack(pady=20)

        self.load_btn = Button(self.frame, text="Load Image", command=self.load_image, width=20)
        self.load_btn.grid(row=0, column=0, padx=10, pady=10)

        self.otsu_btn = Button(self.frame, text="Otsu Thresholding", command=self.apply_otsu_threshold, state=DISABLED,
                               width=20)
        self.otsu_btn.grid(row=0, column=1, padx=10, pady=10)

        self.sobel_operator_btn = Button(self.frame, text="Sobel operator", command=self.apply_sobel_operator,
                                         state=DISABLED, width=20)
        self.sobel_operator_btn.grid(row=0, column=2, padx=10, pady=10)

        self.display_panel = Label(self.root)
        self.display_panel.pack(pady=20)

        self.image = None
        self.processed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.image)
            self.otsu_btn.config(state=NORMAL)
            self.sobel_operator_btn.config(state=NORMAL)

    def display_image(self, img):
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.display_panel.config(image=imgtk)
        self.display_panel.image = imgtk

    def apply_sobel_operator(self):
        sobel_x = cv2.Sobel(self.image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(self.image, cv2.CV_64F, 0, 1, ksize=3)

        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
        self.processed_image = sobel_combined
        self.display_image(sobel_combined)

    def apply_otsu_threshold(self):
        _, thresh_otsu = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.processed_image = thresh_otsu
        self.display_image(thresh_otsu)


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
