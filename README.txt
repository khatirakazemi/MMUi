## ui_frog libary ##
This is a free open-source pygame UI libary, so that you can make UI using pygame - for menus and whatever
Im making this open source so that you dont have to do it yourself when you make UI in pygame, works like any other module. If you run into any issues or need extra functionallity talk to me and write a post on the issues thread. If you make improvements please show me so i can incorporate it in the base module.

## pre-requisites ## 

> pygame
  |> https://www.pygame.org/wiki/GettingStarted

## upcoming ##
> track every instance of a class and output in an error log.txt, make a function for this and implement every crash - raise Exception clause
> pairent class called entity where each type would be a child this class would include the getfontsize and getinactivecolor functions so we dont have to rewrite them
> complete revamp of the Button class, to instead of creating a sepreate rect, to cteate a rect arround given text

## setup ## 
download the apropriate version of the module, place it in your directory under your_driectory\bin\ui_frog

## changelogs ##
> version 0.1 ## known issues ## inactive colors work the opposite way when pressed they get darker in function get_inactiveColor in InputBox obj
  |>TextBox takes A LOT of args
  	NEEDED
	-x, y, w, h (self explanitory)
	-text = str of text 
	NOT NEEDED
	-limit-vertically = True/False : weather the limiting factor of the text is the height (True) or the width (False)
	-font_name = '' : name of the font not using this variable 
	TO DRAW TO SCREEN CALL:
	-box.draw(screen)
  |>InputBox args
	NEEDED
	-x, y, w, h
	NOT NEEDED
	-text = string of text
	-color = tuple :takes rgb color code up to (255, 255, 255)
	-colorDiff = float : percentage of difference between the color of active and inactive - the ammount it dims and grays out this defaults to 50% 
	-font_name = string of font name in the pygame libary : defaults to None which is the default pygame font
	TO DRAW TO SCREEN CALL:
	-for each event
		-box.handle_event(event)
	-then update 
		-box.update()
	-then draw after filling screen
		-box.draw(screen)
  |>Button args
	NEEDED
	-x, y, w, h
	-result = [prosedure] : e.g prosedures(ONLY) is written def quit() you would put it in results like quit
	NOT NEEDED
	-color = tuple :takes rgb color code up to (255, 255, 255)
	-colorDiff = float : percentage of difference between the color of active and inactive - the ammount it dims and grays out this defaults to 50% 
	-font_name = string of font name in the pygame libary : defaults to None which is the default pygame font
	-font_override = int : overrides font size function and sets fontsize as given.
