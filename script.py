import exifread
from imutils import paths
import json
import zlib
import jsonpickle
import re
from difflib import SequenceMatcher
import time
test_folders = ["Photoshop", "Facebook", "Lightroom"]


def getImages(folder):
    return(paths.list_images(folder))

def getCRC32(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def saveMetadata(tag):
    with open('stored_exif.json', 'w') as output_file:
        json.dump(tag, output_file)
        print("Successfully saved metadata to stored_exif.json")
    return(1)

def getEXIF(image):
    crc = getCRC32(image)
    f = re.match("(.*)/((.*).jpg)", image)
    filename = f.group(2)
    with open(image, 'rb') as f:
        tags = exifread.process_file(f)
        tags = jsonpickle.encode(tags)
        serial = {
            "_FILENAME": filename,
            "_CRC": crc,
            "EXIFDATA": tags,
        }
        return(serial)

def compareEXIFData(reference, test):
    reference = jsonpickle.decode(reference["EXIFDATA"])
    test = jsonpickle.decode(test["EXIFDATA"])
    differences = []
    for i, (reference_key,reference_value) in enumerate(reference.items()):
        if reference_key == "JPEGThumbnail":
            break
        if(reference_key in test):
            s = SequenceMatcher(None, str(reference_value), str(test[reference_key]))
            if s.ratio() < 1:
                differences.append({
                    "key": reference_key,
                    "ref_value": reference_value,
                    "test_value": test[reference_key],
                })
        else: # Key not present in test image
            differences.append({
                "key": reference_key,
                "ref_value": reference_value,
                "test_value": "N/A",
            })
    return(differences)

def compareMetadata(image):
    f = re.match("(.*)/((.*).(jpg|tiff|png))", image)
    filename = f.group(2)
    #try:
    with open('stored_exif.json') as exif_table:
        data = json.load(exif_table)
        if len(data) > 0:               
            for reference in data:
                if reference["_FILENAME"] != filename:
                    break
                else:
                    print("Reference image match found at {}!".format(filename))
                    test = getEXIF(image)
                    return compareEXIFData(reference,test) # Compare the two files
        else:
            print("No reference images detected!")
    return ["Cannot find reference image for: {}".format(filename)]

    #except:
    #    print('Error in finding reference images...')

def scanReferenceImages():
    print("Scanning reference images...")
    reference = []
    for image in getImages("reference_images/"):
        reference.append(getEXIF(image))
    with open('stored_exif.json', 'w+') as exif_table:
        json.dump(reference, exif_table)
    print("Done scanning reference images...")


def main():
    t_started = time.time()
    scanReferenceImages()
    for folder in test_folders:
        testImages = getImages(folder+"/")
        for i in testImages:
            print("----- Testing File: {} -----".format(i))
            diff = compareMetadata(i)
            if len(diff) == 0:
                print("No difference in Metadata found!")
            else:
                print("Difference in Metadata found!")
                for differences in diff:
                    print(differences)
            print("--------------------------")
    print("Script completed in {} seconds".format(time.time() - t_started))


if __name__ == "__main__":
    main()