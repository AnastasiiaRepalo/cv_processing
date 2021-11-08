# Get faces coordinates from CV

This project was created for faces detection on photos from resumes. On localhost:5000 you could choose file (pdf or docx) and get result in json format. File would be saved into `input_files/` folder.
All photos would be extracted and saved into proper directory `photos/<INPUT_FILE_NAME>`. 

### To run project you have to clone it first of all:

``` python
git clone https://github.com/AnastasiiaRepalo/cv_processing.git
```

### And for docker build and run:

``` python
docker build -t cv-face-detector .
docker run -dp 5000:5000 cv-face-detector
```





