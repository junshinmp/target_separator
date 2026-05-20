# Target Separator

Aim Training analysis requires information that aim trainers simply do not provide, coming in the formats of comma separated value (CSV files). Simple log files from applications such as Kovaaks or AimLabs prevent further analysis from machine learning models, necessitating the usage of video analysis to provide the most useful insight.

This set of files aims to achieve finding a way to make the video useful to be feeded into a analysis model.

Such problems arise in this task:

    Differentiating target
    Differentiating crosshair
    Removing frames that indicate end of task (menus and other screens)

## Step 1 — Frame extraction

First, the video is spliced into several different images every 60 frames, resulting in the simple raw images without any post-processing such as removing menus and other elements. The reason for this is because the video needs to be made into a consumable format where a You-Only-Look-Once (YOLO) model can be used. By only taking images from every 60 frames (notably, training data videos are taken at 60 frames per second), significant images are saved while useless images are not.
## Step 2 — Labeling & augmentation

Second, the video is labeled using an external tool: Roboflex, applicable either through it's website or an implemented label file as provided in this program. With this, a labeling of each target and crosshair object found in the picture can be made, allowing the next step to make progress. Roboflex allows for the limited set of images provided to also be altered in another way: Augmentation. By augmenting the limited training data, the data can now cover a wide range of target sizes and colors, minus the time needed to apply new settings for an aim trainer. This solves another problem of Generalization vs. Overfitting, with a great bias in overfitting with the limited amount of data present within the training data.
## Step 3 — YOLO inference

Third, as mentioned previously, YOLO will be applied over the images for the following reasons:

    Speed: Outperforming other methods such as DPM and R-CNN, YOLO provides an insanely fast image processing speed that can quickly find answers for our task.
    Bounding-Box usage: Using coordinates, finding the bounding boxes of each target is very useful for this problem.
    Accuracy: At its speeds, YOLO still provides great mean Average Precision in comparision to other real time systems.
    Generalization: Color in aim trainers ranges greatly from user to user, requiring a model that can generalize users with other target colors from one another, and crosshair colors from one another.
