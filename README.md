# catGenerator
A variational autoencoder that generates images of cats.

The cat model was trained on cropped versions of the data from the [Kaggle cat dataset](https://www.kaggle.com/crawford/cat-dataset) obtained from this [git repository](https://github.com/YutingZhang/lmdis-rep). The training data consistes of 9997 `100 * 100` pixel images of cat faces.

## Training

The model can be trained by running `trainModel.ipynb` with appropriate parameters set (path to the image data). The weights that result from training the model with default parameters are available in the `./weights/` directory.

## Testing

The model may be tested by running `testModel.ipynb`.

## Generating Images

Individual cat images can be generated using the provied script `genCats.py`. The script can be run using

```   python3 genCats.py <desired number of cats>```

