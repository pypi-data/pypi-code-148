import random

config = {
    'emoji_transforms':
    {
        "Add" : False,
        "Multiply" : False,
        "Cutout" : False,
        "CoarseDropout" : False,
        "CoarseSaltAndPepper" : False,
        "JpegCompression" : False,
        "BlendAlpha" : False,
        "BlendAlphaRegularGrid" : False,
        "GaussianBlur" : False,
        "MotionBlur" : False,
        "MultiplyHueAndSaturation" : False,
        "Grayscale" : False,
        "ChangeColorTemperature" : False,
        "SigmoidContrast" : False,
        "CLAHE" : False,
        "Emboss" : False,
        "DirectedEdgeDetect" : False,
        "Fliplr" : False,
        "PiecewiseAffine" : False,
        "PerspectiveTransform" : False,
        "WithPolarWarping" : False,
        "Rot90" : False,
        "ElasticTransformation" : False,
        "Jigsaw" : False,
    }
}

def Example_Bad_Function(image, emoji):
    return [(random.randint(0,512),random.randint(0,512))]


