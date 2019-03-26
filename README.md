# Python EXIF Matching
This script basically compares two(2) identically named images in different folders. One folder named reference_images and another test image folder (Lightroom, Photoshop, Facebook, etc.). The script displays the differences via the terminal if the two images have different EXIF data.

## Folder Structre
Project Folder\
├── reference_images/ <-- Reference Folder\
│ ├── img1.jpg\
│ ├── img2.png\
├── Lightroom/ <-- Test Folder\
│ ├── img1.jpg\
│ ├── img2.png\
├── stored_exif.json<-- This is where we store previous exif data so we dont have to re-read the exif data\
├── script.py\

## How to use?
```bash
python script.py
```

## Sample Output
![Sample](https://i.imgur.com/BqpBlB4.png)