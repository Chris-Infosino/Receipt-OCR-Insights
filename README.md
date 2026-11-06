<a href="https://receipt-ocr-insights.streamlit.app"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"><a/>

# Use OCR to read and process data from receipts
This repository focuses on using python's easyocr package to read text from receipts and identify key information of interest.  
A JSON file is created to store important information alongside each receipt image.  
Annotations are then made on the image directly to highlight the date and total on each receipt. 

Access the [demo on Streamlit](https://receipt-ocr-insights.streamlit.app/) or follow the installation steps below.   
> [!NOTE]  
> Streamlit puts apps to sleep after 12 hours of inactivity. It may take up to a minute for the app to wake up.

## Installation
1. Clone this repository or download the source code.  
2. Install the required Python packages using the requirements.txt file:  
```
pip install -r requirements.txt
```

## Usage
To run the Streamlit application, execute the following command in your terminal from the project's root directory:
```
streamlit run src/app.py
```
This will start the local Streamlit server and open the application in your default web browser.

## Features
First, the OCR reads all text from the provided image, alongside corresponding confidence scores and bounding boxes.  

Text is then compared to predetermined positive or negative indicators of notable information. For example, the words `date` or `time` are strong positive indicators that the string is a Date or Time, `am` or `pm` are weak positive indicators that the string is a Time, and `account number` is a negative indicator that the string would be a Date. Similar indicators exist for Total and Amount text strings.  

Next the important text, labels, and coordinates for each image are stored in a JSON file under the same base name as the provided image to store and reference when creating annotations. 

Finally, annotations are drawn onto the image with unique colors and text labels for each identified data type. See the below example: 

<div align="center">
<img width="350" height="750" alt="Example receipt pre-processing" src="assets\093_asset.png" />
<img width="350" height="750" alt="Example receipt with date, totals, and amounts annotated to indicate important information" src="assets\annotated_093_asset.png" />  
</div>

Dates and times are indicated by red boxes, totals by blue boxes, and amounts by green boxes.  
Annotations are drawn directly onto the provided image, meaning image preferences (such as size or color filter) will persist in the output.

**What if positive indicators for a specific field are not present on the receipt?**  
Alternatively, when not indicated by surrounding text, information such as date-qualifying strings are passed through multiple checks and date parsers to identify potential dates that may be less-clearly indicated on the receipt.  Potential dates are indicated by orange boxes in the annotation.  

<div align="center">
<img width="350" height="750" alt="Example receipt pre-processing where potential date needs to be identified by procedural checks" src="assets\003_asset.jpg" /> 
<img width="350" height="750" alt="Example receipt where a potential date is indicated based on procedural checks rather than the presence of date-indicating text" src="assets\annotated_003_asset.png" />  
</div>
This helps to further collect useful information from a variety of receipt layouts, but does have some drawbacks as indicated in the [Areas for Improvement](#areas-for-improvement) section of the README.  

## Purpose
The OCR Receipt Reader utilizes a diverse set of features and functions to extract, process, store, and deliver insights from what would otherwise be a timely and manual review of physical or digital records.  

As it stands, this project has utility for both individuals and organizations:  
- For an individual, the ability to script receipt processing can be used for regular budget tracking or identifying trends in their spending. Additionally, individuals could use the extracted information to visualize their spend or perform statistical analyses on their habits to better understand how, when, and how much they are spending. Extracting information such as store names would allow for further analysis across shopping areas. This is further explored in the [Alternative Functionality](#alternative-functionality) section of the README.  
- For an organization, there is even more potential. Organizations can track trends by date, time, or total earnings across all sales from a given time period; not just on typical receipts, but also invoices or credit statements. This would allow them to perform more robust sales assessments, visualize spend over time trends, build shopper profiles if account numbers were extracted, track ROI across business locations if store information was collected, cash versus credit spend, and much more. This is further explored in the [Alternative Functionality](#alternative-functionality) section of the README.  

## Opportunity Areas

### Alternative Functionality
As highlighted above, capturing additional information from the receipt would enable further analysis across stores, locations, or mechanisms. Receipts are a wealth of information, not just for the purpose of having a record of what was bought but also as a primary source for information. Businesses are built and grown on the ability to learn from the data and use it to drive decision making. There are corporations today that make their money collecting receipts from customers, processing the information in them, and using this to better business practices, marketing, and sales. The more information that can be processed and linked together, the stronger and more useful the insights will be.  
This script can also be used or modified to enable more than just receipt processing. For example, processing an image to identify the cost of an item could be useful for creating and updating online menus for a small-business or processing tax documents across a variety of institutions. Such alternatives can and should be explored to expand upon this project in the future; it would be best to fork from this project to create a specialized version tailored to each purpose, though additional feature checks could be built in to classify an image by type and purpose if desired.

### Areas for Improvement
There are three primary areas of improvement that future enhancements to this project could focus on.  

**1. Additional information from the receipt can be captured and processed as part of a larger dataset**  
Currently this script extracts and highlights dates, totals, and amounts from the provided images. Additional information that could be useful to collect for further analysis could include what stores are represented, store locations, payments collected via cash versus card, discounts applied via sales or coupons, and much more. The ability to collect this information will vary by receipt type and format, as not all of the proposed information is consistently provided or formatted.  
That being said, the insights to be gained from this information and the enabled statistical analyses would be otherwise impossible from such a dataset. The ability to identify and model trends across and between these factors is a worthwhile effort to expand this project going forwards. 

**2. Numbers that look like dates, but are not, continue to be flagged.**  
In the below image, you will see that a date, total, and amount have correctly been identified. However, there is an additional text block saying `1.06` that is also highlighted as a potential date.  

<div align="center">
<img width="350" height="750" alt="Example receipt pre-processing where a tax amount will incorrectly be identified as a potential date" src="assets\085_asset.jpg" />  
<img width="350" height="750" alt="Screenshot of annotated image containing correctly tagged date, total, and amounts with an additional potential date incorrectly highlighted" src="assets\annotated_085_asset.png" />   
</div>

While `1.06` could mean `January 6th`, in this case it is a dollar amount indicating taxes paid on the purchased items. Additional checks could be made to exclude this if a date and time are already identified with a higher confidence level elsewhere in the receipt, or if additional contextual information could be used to further check if this string is or is not a date.  

**3. The OCR model is not trained specially for receipt data.**  
This is perhaps one of the most difficult hurdles to overcome for this project, as the ability to analyze the data is fully reliant on the ability of the OCR to accurately reflect the provided text. Due to the inconsistent formatting and quality of provided images, an OCR model that is trained on a large dataset of receipts would enable more accurate results, avoiding false positives or negatives where indicators are missed or text is misread.  
As easyocr does allow for model selection, a future project could focus on performing unsupervised learning of a large sample of receipts for the sole purpose of improving the character recognition capabilities on this type of image. An improved model would not only allow for the current script to perform at a higher level of accuracy, but it would also allow for additional insights to be extracted and processed.  
Until a better model is available, the current confidence scores of extracted text from the easyocr model are not significantly significant enough to use for the purpose of confirming or eliminating read text from processing. A stronger model would allow for more accurate reading and a significant difference between scores which could be used to identify a threshold to include or exclude extracted text based on the confidence score and how many standard deviations from the mean that value lies.  
Especially when using this for decision-making and as part of a business process, there is a real cost to inaccuracy and it is essential that the model has a high confidence in the extracted values. 
