# This project is used to block bullet screen which masks the faces that apear in the video.
## Video2Masks.py
This is the first script you need to run. It's a preproccess to do before the formal job starts. It will transfer every frame of video into gray pictures which I use ``instance segementation`` to sperate people and backgroud.

![](Markdown_imgs%5C2022-05-08-17-28-34.png)

## CommentsTrackLayer.py
This is a package for you to manage bullet comments,like:
- how many tracks you wanna have
- the font of the comments
- the color of the comments
- the size of the commnets
- the speed of the commnets travel through the screen
  
  
## main.py
It will composite the video layer and bullet comments layer into integer

![](Markdown_imgs%5C2022-05-08-17-33-47.png)