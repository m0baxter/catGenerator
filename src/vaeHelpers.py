
import matplotlib
import matplotlib.pyplot as plt
import src.imageTrans as it
import numpy as np
from glob import glob
import keras.backend as kb
from keras.preprocessing import image


def readSavedFiles( path ):

    files = []

    with open( path, "r" ) as readFile:
        for line in readFile:
            files.append( line.strip() )

    return np.array( files )

def writeFilesList( path, files ):
    
    with open( path, "w") as outFile:
        for f in files:
            outFile.write( f + "\n" )

def sampling( args ):
    """Samples from a normal distribution with mean args[0] and log-variance args[1]."""

    mean, logSigma = args
    batch = kb.shape( mean )[0]
    dim   = kb.int_shape( mean )[1]

    epsilon = kb.random_normal( shape = (batch, dim) )

    return mean + kb.exp(0.5 * logSigma ) * epsilon

def genData( files, size = 200 ):
    """Generates a set of training data and its associated labels."""

    X = np.zeros( (len(files), size, size, 3) )

    i = 0

    for f in files:
        img  = image.load_img( f, target_size = (size, size) )
        img  = image.img_to_array(img)/255
        X[i] = img

        i += 1

    return X, None

def genBatch( files, batchSize, imgSize = 200, rnd = False ):
    """Generator of mini batches for training."""

    while (True):
        inds = np.random.permutation( len(files) )

        for start in range(0, len(files) - 1, batchSize):

            X, _ = genData( files[ inds[start : start + batchSize] ], size = imgSize )

            if (rnd):
                #Choose transformations
                #brightness:
                if ( np.random.rand() < 0.5 ):
                    X = it.adjustBrightness( X, np.random.uniform(-0.3, 0.3) )

                #mirror flip:
                if ( np.random.rand() < 0.5 ):
                    #X = it.mirrorImages( X, np.random.randint(0,2) )
                    X = it.mirrorImages( X, 0 )

                #other transforms:
                #if ( np.random.rand() < 0.5 ):
                #    imageTransformers = [ lambda x : it.scaleImages( x, np.random.uniform(0.77, 1.43) ),
                #                          lambda x : it.translateImages( x, np.random.randint(0,5),
                #                                                            np.random.uniform(0, 0.3) ),
                #                          #lambda x : it.rotateK90Degs( x, np.random.randint(0,4) ),
                #                          lambda x : it.rotateImages( x, np.random.uniform(-np.pi/2, np.pi/2) ) ]

                #    transform = np.random.choice( imageTransformers )
                #    X = transform(X)

            yield X, None

def plotLosses( losses ):
    """Plots training loss as a fucntion of epoch."""

    fig = plt.figure(1, figsize = (18,10))
    plt.plot( range(1, len(losses["loss"]) + 1), losses["loss"], "b-",
              linewidth = 3, label = "$\mathrm{training}$")
    plt.plot( range(1, len(losses["val_loss"]) + 1), losses["val_loss"], "g-",
              linewidth = 3, label = "$\mathrm{validation}$")
    plt.ylabel("$\mathrm{Loss}$")
    plt.xlabel("$\mathrm{Epoch}$")
    plt.legend( loc = "best" )

    plt.show()
    #fig.savefig( "lossPlot.eps", format = 'eps', dpi = 20000, bbox_inches = "tight" )

    return

def plotGrid( data, title ):
    """Plots a grid of images. Assumes that len(data) is a perfect square."""

    m = int(np.sqrt( len(data)) )
    f, axarr = plt.subplots(m, m)
    k = 0

    f.suptitle( title )

    for i in range(m):
        for j in range(m):

            axarr[i,j].imshow( data[k,:,:,:], vmin = 0, vmax = 1  )
            axarr[i,j].get_xaxis().set_ticks([])
            axarr[i,j].get_yaxis().set_ticks([])

            k += 1

    plt.show()

