MedWise is a comprehensive mobile application designed to enhance the well-being and safety of the elderly. The app offers a range of intuitive features tailored to make medication management and emergency response easier and more efficient:
1. Medicine recognition by utilising pytesseract, an Optical Character Recognition (OCR), to read the packaging information of medication. The app will then feed the read information to Gemini, thus providing a brief explanation of what the medication is used for and how much would be a correct dosage.
2. Integrated TTS that supports 2 languages, English and Chinese for those elderly who suffer from reading issues.
3. Emergency location services which would show you the nearest hospitals and health services and rank them by distance.

It uses pytesseract which is a wrapper for google's OCR software tesseract to function, which can be downloaded here
https://github.com/UB-Mannheim/tesseract/wiki

To launch the app just download the dependencies and run app.py
