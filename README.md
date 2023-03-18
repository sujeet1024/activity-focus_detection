# Activity and Focus Detection using OpenCV
This assignment was submitted to Kino AI Challenge: Metadata Engine Hackathon

### Problem statement:
- Moments of significant visual activity, inactivity detection per video frame
- Out-of-focus frame detection (categorizing video frame as blur or focussed)

Classical Computer Vision approches were used for both the problems,
- Successive frames were compared using Optical Flow methods for the activity recognition
- Blur detection was done by computing and comparing the Variance of Laplacian of each frames

### Requirements
`ffmpeg` package for converting video files
```
numpy                        1.24.2
```
```
opencv-python                4.7.0.72
```
```
subprocess.run               0.0.8
```


### I/O 
- The `eninge = Engine(Inp)` in line 97 takes filename or list of filenames as input
- The `engine.process(idx)` in line 98 takes the index of the list of filenames to process the video file
- The methods used are robust and runs a real time, in video output
- The threholds can be customized accordingly for better categorization in line the 14
