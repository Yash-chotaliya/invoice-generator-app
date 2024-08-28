# Invoice Generator App

The Invoice Generator App allows users to upload an image of an old invoice and generate a new invoice based on the uploaded content. This application utilizes Streamlit for the user interface, Google Generative AI for processing the invoice, and a custom API for generating the new invoice.

## Features

- Upload Invoice: Users can upload an image of their old invoice.
- Generate New Invoice: The app extracts information from the uploaded invoice and generates a new invoice.
- Download New Invoice: Users can download the newly generated invoice directly from the app.

## Technologies Used

- Python: Programming language used for the application.
- Streamlit: Framework for building the web interface.
- Google Generative AI: For understanding and extracting data from the invoice image.
- Requests: For making HTTP requests to the invoice generation API.
- Pillow: For image processing.

## Setup and Installation

1. Clone the Repository
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create a Virtual Environment
   ```bash
   conda create -p venv
   ```

3. Activate the Environment
   ```bash
   conda activate venv
   ```

4. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Set Up Environment Variables
   Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key
   ```

6. Run the Application
   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the application in your browser.
2. Upload an image of the invoice using the file uploader.
3. Click the "Submit" button to process the invoice.
4. If successful, a download button will appear allowing you to download the generated invoice.

## Notes

- Ensure the uploaded image is clear for accurate extraction of data.
- The app uses the Google Generative AI model to interpret the invoice image and extract necessary details.

## Troubleshooting

- File Not Uploaded: Make sure you upload an image file in JPG, JPEG, or PNG format.
- Error Generating Invoice: Verify that the image is clear and readable.