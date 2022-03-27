# ORBID: Refugee Boat Image Dataset

## Download the data

Download the data here: [https://drive.google.com/drive/folders/1MguQ-PfyjSpRsNgypgS9hbrOSCDGMz7B?usp=sharing](https://drive.google.com/drive/folders/1MguQ-PfyjSpRsNgypgS9hbrOSCDGMz7B?usp=sharing)

## Structure

```
-- toar                        top-of-athmosphere reflectance (TOAR)
 |- img001.npy                 numpy format
 |- img002.npy                 data type: uint16
 |- img003.npy                 Actual values are scaled from 0-10000
 |- ...
-- true_color                  color corrected images
 |- img001.png                 png
 |- img002.png                 data type: uint8
 |- img003.png
 |- ...
-- publishing_instances.json    COCO-style annotations

```

## Annotation Format

Analogue to the [COCO-format](https://cocodataset.org/#format-data)

```
{
    "images": [
        {
            "id": 1, 
            "width": 800, 
            "height": 800, 
            "file_name": "img001.png", 
            "swh": 0.45356306433677673
        },
        {...}
    ],
    "annotations": [
        {
            "id": 1, 
            "image_id": 1, 
            "category_id": 0, 
            "segmentation": [[
                85.67000000000007, 63.22000000000003, 
                83.86999999999989, 56.620000000000005, 
                80.76999999999998, 52.72000000000003, 
                73.17000000000007, 45.41999999999996, 
                64.86999999999989, 53.32000000000005, 
                71.97000000000003, 62.620000000000005, 
                78.06999999999994, 66.72000000000003, 
                83.36999999999989, 66.01999999999998, 
                85.67000000000007, 63.22000000000003]], 
            "area": 245.0, 
            "bbox": [64.86999999999989, 45.41999999999996, 20.8, 21.3], 
            "iscrowd": 0, 
            "attributes": {
                "has_wake": true, 
                "refugee": false, 
                "white_waves": false, 
                "occluded": false
            }
        },
        {...}
    ],
    "categories": [
        {
            "id": 0, 
            "name": "boat", 
            "supercategory": ""
        }
    ]
}
```

Details about the **polygon format**: It is a series of (x, y) points that mark the bounds of the polygon.

Details about the channel order in the Numpy containers: shape is (c, w, h).

The **special attributes** only in ORBID are *swh* (significant wave height) in the image objects and *has_wake*, *refugee* and *white_waves* in the annotation objects.

Note: Image and annotation ids start at 1.

## Dataset Info

* 264 images
* 548 objects

## Apply the color conversion

```
cd color_conversion
pip install -r requirements.txt
python convert_toar_to_true_color.py ../toar ../processed toar_to_truecolor.npy
```

## Satellite Data Licensing

Copyright Planet Labs PBC.