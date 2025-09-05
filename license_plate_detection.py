import cv2
import numpy as np
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import pytesseract
from _datetime import datetime

# set the path to the Tesseract-OCR executable file
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

global cancel_frame_created
cancel_frame_created = False

TBC_created = False

random_string = ''


# the Tkinter GUI application begins here
def tkinter_application(theNumber):
    root = Tk()
    root.title("Number Plate Checker")
    myList = []

    # Load the background image
    bg_image = tk.PhotoImage(file="images/ukapartment.png")

    # Create a label with the background image
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Adjust size
    height = 600
    width = 900
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # these are frames that were used for displaying the various interfaces in tkinter
    register_frame = Frame(root)
    cancel_frame = Frame(root)
    authorizedCars_frame = Frame(root)

    status_list = ['New Resident', 'Visitor']

    # This function is to check if a vehicle is authorized or not to enter the community,
    # and display the vehicle details.
    def authorizedCars():
        global TBC_created
        cancel_frame.pack_forget()
        # vehicleID = res_entry.get()
        if not TBC_created:
            TBC_created = True
            authorizedCars_frame.pack()
            try:
                with open('Registered_Vehicles_V2.csv', newline='') as csvfile:
                    for row in csv.reader(csvfile):
                        if row[3] == theNumber and row[8] == 'R':
                            vehicleNum = row[3]
                            owner = row[4]
                            model = row[5]
                            address = row[6]
                            contact = row[7]
                            display_label0 = tk.Label(authorizedCars_frame,
                                                      text='--------- Vehicle Number : ' + vehicleNum + ' ---------')
                            display_label0.pack(padx=40, pady=5)
                            name_label = tk.Label(authorizedCars_frame, text='Owner : ' + owner)
                            name_label.pack(padx=40, pady=5)
                            model_label = tk.Label(authorizedCars_frame, text='Vehicle Model : ' + model)
                            model_label.pack(padx=40, pady=5)
                            address_label = tk.Label(authorizedCars_frame, text='Owner Address : ' + address)
                            address_label.pack(padx=40, pady=5)
                            contact_label = tk.Label(authorizedCars_frame, text='Owner Contact : ' + contact)
                            contact_label.pack(padx=40, pady=5)
                            submit_button = tkinter.Button(authorizedCars_frame, text='Entry Approved',
                                                           state=tk.DISABLED, font='Helvetica 18 bold')
                            submit_button.pack()
                            break
                        elif row[3] == theNumber and row[8] == 'V':
                            vehicleNum = row[3]
                            owner = row[4]
                            model = row[5]
                            contact = row[7]
                            theTime = row[2]
                            TimeIn = datetime.strptime(theTime, '%H:%M:%S')
                            exitTime = datetime.now().time()
                            duration = datetime.combine(datetime.today(), exitTime) - datetime.combine(datetime.today(),
                                                                                                       TimeIn.time())
                            hours_spent = duration.total_seconds() / 3600  # 3600 seconds in an hour
                            minutes = int(duration.total_seconds()) / 60
                            label_minutes_var = tk.StringVar()
                            label_toPay_var = tk.StringVar()
                            label_minutes_var.set('Parking Duration: ' "{:.2f}".format(minutes) + ' minutes')
                            if hours_spent < 1:
                                hours_spent = 1
                            toPay = hours_spent * 2
                            label_toPay_var.set('Amount Paid: £ ' "{:.2f}".format(toPay))
                            display_label0 = tk.Label(authorizedCars_frame,
                                                      text='--------- Vehicle Number : ' + vehicleNum + ' ---------')
                            display_label0.pack(padx=40, pady=5)
                            name_label = tk.Label(authorizedCars_frame, text='Owner : ' + owner)
                            name_label.pack(padx=40, pady=5)
                            model_label = tk.Label(authorizedCars_frame, text='Vehicle Model : ' + model)
                            model_label.pack(padx=40, pady=5)
                            owner_label = tk.Label(authorizedCars_frame, text='Owner Contact : ' + contact)
                            owner_label.pack(padx=40, pady=5)
                            duration_label = tk.Label(authorizedCars_frame, textvariable=label_minutes_var)
                            duration_label.pack(padx=40, pady=5)
                            contact_label = tk.Label(authorizedCars_frame, textvariable=label_toPay_var)
                            contact_label.pack(padx=40, pady=5)

                            submit_button = tkinter.Button(authorizedCars_frame, text='Exit Approved',
                                                           state=tk.DISABLED, font='Helvetica 18 bold')
                            submit_button.pack()
                            break
                    else:
                        authorizedCars_frame.pack_forget()
                        messagebox.showerror("Error", "Unauthorized Vehicle. Please Register")
                        for i in authorizedCars_frame.winfo_children():
                            i.destroy()
                        authorizedCars_frame.pack_forget()
                        register()
            except FileNotFoundError:
                print("File not found. Check the path variable and filename")

    # This function is a form that gathers new vehicle registration information (either resident or visitor)
    def register():
        cancel_frame.forget()
        authorizedCars_frame.forget()
        register_frame.pack()

        global v_number_entry, owner_entry, model_entry, address_entry, contact_entry, status_dropdown

        v_number_label = tk.Label(register_frame, text="Enter Vehicle Number: ")
        v_number_label.pack(padx=40, pady=5)
        v_number_entry = tk.Entry(register_frame)
        v_number_entry.pack(padx=40, pady=5)

        owner_label = tk.Label(register_frame, text="Enter Owner Name: ")
        owner_label.pack(padx=40, pady=5)
        owner_entry = tk.Entry(register_frame)
        owner_entry.pack(padx=40, pady=5)

        model_label = tk.Label(register_frame, text="Enter Vehicle Model: ")
        model_label.pack(padx=40, pady=5)
        model_entry = tk.Entry(register_frame)
        model_entry.pack(padx=40, pady=5)

        address_label = tk.Label(register_frame, text="Enter Owner Address: ")
        address_label.pack(padx=40, pady=5)
        address_entry = tk.Entry(register_frame)
        address_entry.pack(padx=40, pady=5)

        contact_label = tk.Label(register_frame, text="Owner Contact Number: ")
        contact_label.pack(padx=40, pady=5)
        contact_entry = tk.Entry(register_frame)
        contact_entry.pack(padx=40, pady=5)

        status_label = tk.Label(register_frame, text="Select Status : ")
        status_label.pack(padx=40, pady=5)
        status_dropdown = ttk.Combobox(register_frame, values=status_list, state="readonly")
        status_dropdown.pack(padx=40, pady=5)
        status_dropdown.set('New Resident')

        submit_button = tkinter.Button(register_frame, text='Register and Allow Entry', bg="#127ba7",
                                       command=submit_form)
        submit_button.pack()

    # This function prepares the registration information to be saved into a csv file.
    def submit_form():
        with open('Registered_Vehicles_V2.csv', 'r') as file:
            myFile = csv.reader(file)
            for row in myFile:
                myList.append(row)
        Date = datetime.now().date()
        Month = 'June'
        VehicleNumber = v_number_entry.get()
        OwnerName = owner_entry.get()
        VehicleModel = model_entry.get()
        OwnerAddress = address_entry.get()
        Ownercontact = contact_entry.get()
        if status_dropdown.get() == 'New Resident':
            Status = 'R'
            TimeIn = 'NULL'
        elif status_dropdown.get() == 'Visitor':
            Status = 'V'
            TimeIn = datetime.now().strftime('%H:%M:%S')

        if VehicleNumber and OwnerName and VehicleModel and OwnerAddress and Ownercontact and Status and TimeIn:
            save_to_csv(Date, Month, TimeIn, VehicleNumber, OwnerName, VehicleModel, OwnerAddress, Ownercontact, Status)
        else:
            messagebox.showerror('Error', 'All fields must be filled')

    # This function saves the registration information into the csv file.
    def save_to_csv(Date, Month, TimeIn, VehicleNumber, OwnerName, VehicleModel, OwnerAddress, Ownercontact, Status):
        with open('Registered_Vehicles_V2.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Check if the file is empty and write the header if needed
            if csvfile.tell() == 0:
                writer.writerow(
                    ['Date', 'Month', 'TimeIn', 'VehicleNumber', 'OwnerName', 'VehicleModel', 'OwnerAddress',
                     'Ownercontact', 'Status',
                     ])

            # Write the form data to the CSV file and clear the form entries.
            writer.writerow(
                [Date, Month, TimeIn, VehicleNumber, OwnerName, VehicleModel, OwnerAddress, Ownercontact, Status, ])
            v_number_entry.delete(0, 'end')
            owner_entry.delete(0, 'end')
            model_entry.delete(0, 'end')
            address_entry.delete(0, 'end')
            contact_entry.delete(0, 'end')
            contact_entry.delete(0, 'end')
            status_dropdown.delete(0, 'end')
            messagebox.showinfo('SUCCESS', 'Registration Successful')
            root.quit()

    # This function exits the program when quit button is clicked.
    def quit_application():
        root.quit()

    # This is the top header part of the window
    frame = tk.Frame()
    Intro_label = tk.Label(frame, text='Welcome to the Community Gatekeeper', font=('Algerian', 20))
    Intro_label.pack(padx=20, pady=20)

    frame.pack()
    cancel_frame.pack()

    # These are the 2 menu buttons on the page (register and quit).
    Book_Button = tk.Button(frame, text="Register Vehicle", command=register)
    Quit_Button = tk.Button(frame, text="Quit", command=quit_application)

    Book_Button.pack(side="left", expand=True, fill="both")
    Quit_Button.pack(side="right", expand=True, fill="both")
    authorizedCars()

    root.mainloop()


# This is where the OpenCV code begins
def main():
    global cancel_frame_created

    # Define an image preprocessing code
    def preprocess(gray):
        """
        Transform the shape of grayscale objects (pre-processing)
        :param gray:
        :return:
        """
        # Gaussian smoothing
        gaussian = cv2.GaussianBlur(gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)

        # Median filter
        median = cv2.medianBlur(gaussian, 5)

        # Sobel operator，process the edges which is a convolution
        sobel = cv2.Sobel(median, cv2.CV_64F, dx=1, dy=0, ksize=3)
        # The type is converted to unit8
        sobel = np.uint8(np.absolute(sobel))

        # Binaryzation
        ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)

        # dilation and erosion
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
        # Expand once so the outline stands out
        dilation = cv2.dilate(binary, element2, iterations=1)
        # Corrode once, remove details
        erosion = cv2.erode(dilation, element1, iterations=2)
        # Expand it again to make it more visible
        dilation2 = cv2.dilate(erosion, element2, iterations=5)
        # Corrode once, remove details
        erosion2 = cv2.erode(dilation2, element1, iterations=4)

        return erosion2

    img = cv2.imread("images/car1.jpg", 0)

    # Resizing the image for better scanning
    img = cv2.resize(img, (1220, 950))
    preprocess(img)

    # Do a license plate area search
    def find_plate_number_region(img):
        """
        Look for the outline of a possible license plate area
        :param img:
        :return:
        """
        # Find contours (img: original image, contours: rectangular coordinate points, hierarchy: image hierarchy)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find rectangle
        max_ratio = -1
        max_box = None
        ratios = []
        number = 0
        for i in range(len(contours)):
            cnt = contours[i]  # Coordinates of the current profile

            # Calculated contour area
            area = cv2.contourArea(cnt)
            # Filter out areas that are too small
            if area < 10000:
                continue

            # Find the smallest rectangle
            rect = cv2.minAreaRect(cnt)

            # The four coordinates of the rectangle (the order varies, but it must be a circular order of bottom left, top left, top right, bottom right (unknown starting point))
            box = cv2.boxPoints(rect)
            # Convert to the long type
            box = np.int64(box)

            # Calculate length, width and height
            # Calculate the length of the first edge
            a = abs(box[0][0] - box[1][0])
            b = abs(box[0][1] - box[1][1])
            d1 = np.sqrt(a ** 2 + b ** 2)
            # Calculate the length of the second side
            c = abs(box[1][0] - box[2][0])
            d = abs(box[1][1] - box[2][1])
            d2 = np.sqrt(c ** 2 + d ** 2)
            # Let the minimum be the height and the maximum the width
            height = int(min(d1, d2))
            weight = int(max(d1, d2))

            # calculate area
            area2 = height * weight

            # The difference between the two areas must be within a certain range
            r = np.absolute((area2 - area) / area)
            if r > 0.6:
                continue

            ratio = float(weight) / float(height)
            print((box, height, weight, area, area2, r, ratio, rect[-1]))
            cv2.drawContours(img, [box], 0, 255, 2)
            cv2.imshow('contours in image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # In practice, the ratio should be about 3, but our photos are not standard
            # the measured width to height should be between 2 and 5.5
            if ratio > max_ratio:
                max_box = box
                max_ratio = ratio

            if ratio > 5.5 or ratio < 2:
                continue

            number += 1
            ratios.append((box, ratio))

        # Output data based on the number of image matrices found
        print("Total found :{} possible regions!!".format(number))
        if number == 1:
            # Direct return
            return ratios[0][0]
        elif number > 1:
            # Take the median value without thinking too much (and filter it)
            # The actual requirements are more stringent
            filter_ratios = list(filter(lambda t: 2.7 <= t[1] <= 5.0, ratios))
            size_filter_ratios = len(filter_ratios)

            if size_filter_ratios == 1:
                return filter_ratios[0][0]
            elif size_filter_ratios > 1:
                # Get the median
                ratios1 = [filter_ratios[i][1] for i in range(size_filter_ratios)]
                ratios1 = list(zip(range(size_filter_ratios), ratios1))
                # Sorting data
                ratios1 = sorted(ratios1, key=lambda t: t[1])
                # Get data for the median value
                idx = ratios1[size_filter_ratios // 2][0]
                return filter_ratios[idx][0]
            else:
                # Get the maximum
                ratios1 = [ratios[i][1] for i in range(number)]
                ratios1 = list(zip(range(number), ratios1))
                # Sorting data
                ratios1 = sorted(ratios1, key=lambda t: t[1])
                # Get the maximum value
                idx = ratios1[-1][0]
                return filter_ratios[idx][0]
        else:
            # Direct return to maximum
            print("Return directly to the region closest to the scale...")
            return max_box

    # For license plate interception
    def cut(img_or_img_path):
        """
        Intercept the license plate area
        :param img_or_img_path:
        :return:
        """
        if isinstance(img_or_img_path, str):
            img = cv2.imread(img_or_img_path)
        else:
            img = img_or_img_path

        # Gets the height and width of the image
        rows, cols, _ = img.shape

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Image preprocessing --> The license plate area is clearly displayed
        dilation = preprocess(gray)

        # Find the license plate area (assuming there will only be one)
        box = find_plate_number_region(dilation)

        # Returns the image corresponding to the region
        # Due to we do not know the order of the points, so I sort the coordinates of the points on the left
        ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
        xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
        ys_sorted_index = np.argsort(ys)
        xs_sorted_index = np.argsort(xs)

        # Gets the coordinates on x
        x1 = box[xs_sorted_index[0], 0]
        x1 = x1 if x1 > 0 else 0
        x2 = box[xs_sorted_index[3], 0]
        x2 = cols if x2 > cols else x2

        # Get the coordinates on y
        y1 = box[ys_sorted_index[0], 1]
        y1 = y1 if y1 > 0 else 0
        y2 = box[ys_sorted_index[3], 1]
        y2 = rows if y2 > rows else y2

        # Intercept image
        img_plate = img[y1:y2, x1:x2]

        return img_plate

    def extract_letters(image):
        """
        Function to extract letters from the number plate image using Tesseract OCR
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use pytesseract to perform OCR on the image
        letters = pytesseract.image_to_string(gray, config='--psm 7')
        # Extract the last 7 characters from the OCR result and remove spaces
        letters = ''.join(letters.split())[-7:]

        return letters

    # This path is where the images are loaded. You can test several images by replacing car222.jpg with another car.
    path = 'images/car222.jpg'
    cut_img = cut(path)
    print(cut_img.shape)
    cv2.imwrite(f'plat_{path}', cut_img)

    # visualization
    cv2.imshow('original image', cv2.imread(path))
    cv2.imshow('plate', cut_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Call the function to extract letters from the number plate image
    number_plate_letters = extract_letters(cut_img)

    # Call the function to print the extracted number plate to console
    print("Number Plate Letters:", number_plate_letters)

    # tkinter GUI application receives the extracted number plate for access control
    tkinter_application(number_plate_letters)


if __name__ == "__main__":
    main()
