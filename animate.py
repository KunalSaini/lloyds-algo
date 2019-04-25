import imageio
import glob

images = []
pngList = glob.glob("images/*.png")

for filename in pngList:
    images.append(imageio.imread(filename))

kargs = { 'duration': 2 }
imageio.mimsave('images/movie.gif', images, **kargs)
