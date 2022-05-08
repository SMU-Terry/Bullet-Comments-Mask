# This project is used to block bullet screen which masks the faces that apear in the video.

![image](https://user-images.githubusercontent.com/64240681/167291172-aff15823-c607-4fe0-b892-e017961fa83a.png)


## Video2Masks.py
This is the first script you need to run. It's a preproccess to do before the formal job starts. It will transfer every frame of video into gray pictures which I use ``instance segementation`` to sperate people and backgroud.

![](Markdown_imgs%5C2022-05-08-17-28-34.png)
![image](https://user-images.githubusercontent.com/64240681/167291122-ae44f179-3c3d-4733-9e04-dce39c32184e.png)


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
![image](https://user-images.githubusercontent.com/64240681/167291186-4da7dbe8-e69b-43b8-b88b-a7f5a151bfae.png)
