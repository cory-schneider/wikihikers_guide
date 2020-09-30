from PIL import Image


def monochrome(imgname, extension):  # Function to make Images Monochrome
    photo = Image.open(imgname+extension)  # Open Original Image
    photo = photo.convert('1')  # Converts Image to Monochrome
    return photo  # Returns the New Image


def readpixels(img, x, y):  # Function to Read RGB Value of Image Pixels
    pixel = img.load()  # Stores Image in Memory as Pixel Access Object
    return pixel[x,y]  # Displays RGB Value


def makeascii(img, imgname):  # Function to Convert Image to Ascii
    width, height = img.size  # Get Width and Height
    x = 0  # X Position on Image
    y = 0  # Y Position on Image

    chars = {0: '%', 255: ' '}

    text_file = open(imgname+'.txt', 'w')  # Opens a Text File

    while y <= height - 1:
        rgb = readpixels(img, x, y)  # Reads Pixel at position X, Y
        text_file.write(chars[rgb])  # Writes Pixel as Relevant Character In Text File

        x += 1  # Increases X position by 1

        if x == width - 1:
            text_file.write('\n')  # Takes X to Next Line
            x = 0
            y += 1  # Takes Y to next line

    text_file.close()


print("Welcome to the ASCII Art Generator!")
print("All files must be located in this folder")
imgname = input("Enter Image Name (without its file extension): ")  # Get User Chosen Image
extension = input("Enter its file extension (EX: .jpg}")

makeascii(monochrome(imgname, extension), imgname)

print("Done!")
