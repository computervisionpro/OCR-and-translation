import pytesseract
from pytesseract import Output
import argparse
import cv2
import re
from language_convertor import Tr
import imutils

# python 1.loc_text_translate.py --image gmn.jpg -l de -c 50

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, 
                    help = 'path to input image')
ap.add_argument("-c", "--confidence", type=int, default=0,
                    help='minimum confidence value')
ap.add_argument('-l','--lang', type=str, default='eng', help='Language to read')

#we’ve set the threshold to 0 so that all detections are returned
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
image = imutils.resize(image, width=500)
image2 = image.copy()
image3 = image.copy()

img_shape = image.shape
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)
#rgb = cv2.threshold(gray, 0,255, cv2.THRESH_OTSU)[1]
rgb = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY_INV, 15,3)


#detect and localize text using image_to_data function
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

# detecting text with only spaces
def blanks(pattern, string):
    s = re.compile(pattern).search(string)
    return s
# translation object
conv = Tr(args['lang'][:2])
sentence = []

#looping over the detections
for i in range(0, len(results["text"])):
    #extract the bounding boxes
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]

    #extract text and confidence
    text = results["text"][i]
    conf = int(results["conf"][i])

    check_empty = blanks("^\s+$", text)

    # filter out weak confidences
    if not check_empty and conf > args["confidence"]:
        
        #print("Text: {}".format(text))            

        ## strip out non-ASCII letters and draw boxes
        # cv2.putText function doesn’t support non-ASCII characters
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(image, text, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0,20,255), 3)

        # Translation
        # if language isn't english then translate
        sentence.append(text)
print("")
        
if args["lang"] != "eng":
    s = " ".join(sentence)
    print(s)
    translated = conv.trans(s)
    print("Translation: ",translated)
    cv2.putText(image3, translated, (10, img_shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (250,97,87), 3)  
else:
    s = " ".join(sentence)
    print(s)


# show the output image

cv2.imshow("OCR", image)
cv2.imshow("Input Image", image2)
cv2.imshow("Translated", image3)
cv2.waitKey(0)


