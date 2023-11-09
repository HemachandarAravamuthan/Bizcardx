
# Bizcardx

Extracting business card data with OCR and enable the user to store the data into SQL database.

## Goal

This project is commited to extract the text from the uploaded business card using easyOCR and storing it to the SQL databse.
## Installation

Installing the required packages

```bash
  pip install mysql.connector
```
```bash
  pip install streamlit
```
```bash
  pip install easyocr
```
## Roadmap

- Business card text is extracted using easyocr

- The extracted data is stored in SQL database


## Explanation

- Installed the required packages: I installed Python, Streamlit, easyOCR, and a database management MySQL.

- Designed the user interface: I created a simple and intuitive user interface using Streamlit that guided users through the process of uploading the business card image and extracting its information. I used widgets like file uploader, buttons, and text boxes to make the interface more interactive.

- Implemented the image processing and OCR: I used easyOCR to extract the relevant information from the uploaded business card image. I used image processing techniques like resizing, cropping, and thresholding to enhance the image quality before passing it to the OCR engine.

- Displayed the extracted information: Once the information was extracted,I displayed it in a clean and organized manner in the Streamlit GUI. I used widgets like tables, text boxes, and labels to present the information.

- Implemented database integration: I used a database management MySQL to store the extracted information along with the uploaded business card image. I used SQL queries to create tables, insert data,and retrieve data from the database, Updated the data and Allowed the user to delete the data through the streamlit UI.
## Screenshots

Web page to upload the business card
![bizcardx app layout](https://github.com/HemachandarAravamuthan/Bizcardx/assets/141393571/41455c2f-6f1d-4a93-8c18-3403c2c5b3ed)


The display area where the extracted data and other operations are available 
![operations](https://github.com/HemachandarAravamuthan/Bizcardx/assets/141393571/8e11904b-6076-4282-a875-5ddd56564c80)


## Appendix

The accuracy of the image text extraction can be improved by pre processing the images.


## Contact


email : hemachandar11@gmail.com

Linkedin : https://www.linkedin.com/in/hemachandar-aravamuthan-1594b1194/
