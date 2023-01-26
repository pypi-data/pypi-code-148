from PIL import Image, ImageFont
import numpy as np
import cv2
from pilmoji import Pilmoji
import random
from keras.datasets import cifar100
import imgaug.augmenters as iaa
import time
import pkgutil
import urllib.request

class EmojiHunt():
    def __init__(self, config):
        self.emojis_master_list = ['😫','😩','🥺','😢','😭','😮‍💨','😤','😠','😡','🤬','🤯','😳','🥵',
                      '🥶','😱','😨','😰',
                      '😵‍💫','🤐','🥴','🤢','🤮','🤧','😷','🤒','🤕','🤑','🤠','😈','👿',
                      '👹','👺','🤡','💩','👻','💀','☠️','👽','👾','🤖','🎃','😺','😸','😹',
                      '😻','😼','😽','🙀','😿','😾','🏳️','🏴','🏁','🚩','🏳️‍🌈','🏳️','🏴‍☠️',
                      '🇦🇫','🇦🇽','🇦🇱','🇩🇿','🇦🇸','🇦🇩','🇦🇴','🇦🇮','🇦🇶','🇦🇬','🇦🇷','🇦🇲','🇦🇼','🇦🇺',
                      '🇦🇹','🇦🇿','🇧🇸','🇧🇭','🇧🇩','🇧🇧','🇧🇾','🇧🇪','🇧🇿','🇧🇯','🇧🇲','🇧🇹','🇧🇴','🇧🇦',
                      '🇧🇼','🇧🇷','🇮🇴','🇻🇬','🇧🇳','🇧🇬','🇧🇫','🇧🇮','🇰🇭','🇨🇲','🇨🇦','🇮🇨','🇨🇻','🇧🇶',
                      '🇰🇾','🇨🇫','🇹🇩','🇨🇱','🇨🇳','🇨🇽','🇨🇨','🇨🇴','🇰🇲','🇨🇬','🇨🇩','🇨🇰','🇨🇷','🇨🇮',
                      '🇭🇷','🇨🇺','🇨🇼','🇨🇾','🇨🇿','🇩🇰','🇩🇯','🇩🇲','🇩🇴','🇪🇨','🇪🇬','🇸🇻','🇬🇶','🇪🇷',
                      '🇪🇪','🇪🇹','🇪🇺','🇫🇰','🇫🇴','🇫🇯','🇫🇮','🇫🇷','🇬🇫','🇵🇫','🇹🇫','🇬🇦','🇬🇲','🇬🇪',
                      '🇩🇪','🇬🇭','🇬🇮','🇬🇷','🇬🇱','🇬🇩','🇬🇵','🇬🇺','🇬🇹','🇬🇬','🇬🇳','🇬🇼','🇬🇾','🇭🇹',
                      '🇭🇳','🇭🇰','🇭🇺','🇮🇸','🇮🇳','🇮🇩','🇮🇷','🇮🇶','🇮🇪','🇮🇲','🇮🇱','🇮🇹','🇯🇲','🇯🇵',
                      '🎌','🇯🇪','🇯🇴','🇰🇿','🇰🇪','🇰🇮','🇽🇰','🇰🇼','🇰🇬','🇱🇦','🇱🇻','🇱🇧','🇱🇸','🇱🇷',
                      '🇱🇾','🇱🇮','🇱🇹','🇱🇺','🇲🇴','🇲🇰','🇲🇬','🇲🇼','🇲🇾','🇲🇻','🇲🇱','🇲🇹','🇲🇭','🇲🇶',
                      '🇲🇷','🇲🇺','🇾🇹','🇲🇽','🇫🇲','🇲🇩','🇲🇨','🇲🇳','🇲🇪','🇲🇸','🇲🇦','🇲🇿','🇲🇲','🇳🇦',
                      '🇳🇷','🇳🇵','🇳🇱','🇳🇨','🇳🇿','🇳🇮','🇳🇪','🇳🇬','🇳🇺','🇳🇫','🇰🇵','🇲🇵','🇳🇴','🇴🇲',
                      '🇵🇰','🇵🇼','🇵🇸','🇵🇦','🇵🇬','🇵🇾','🇵🇪','🇵🇭','🇵🇳','🇵🇱','🇵🇹','🇵🇷','🇶🇦','🇷🇪',
                      '🇷🇴','🇷🇺','🇷🇼','🇼🇸','🇸🇲','🇸🇦','🇸🇳','🇷🇸','🇸🇨','🇸🇱','🇸🇬','🇸🇽','🇸🇰','🇸🇮',
                      '🇬🇸','🇸🇧','🇸🇴','🇿🇦','🇰🇷','🇸🇸','🇪🇸','🇱🇰','🇧🇱','🇸🇭','🇰🇳','🇱🇨','🇵🇲','🇻🇨',
                      '🇸🇩','🇸🇷','🇸🇿','🇸🇪','🇨🇭','🇸🇾','🇹🇼','🇹🇯','🇹🇿','🇹🇭','🇹🇱','🇹🇬','🇹🇰','🇹🇴',
                      '🇹🇹','🇹🇳','🇹🇷','🇹🇲','🇹🇨','🇹🇻','🇻🇮','🇺🇬','🇺🇦','🇦🇪','🇬🇧','🏴󠁧󠁢󠁥󠁮󠁧󠁿','🏴󠁧󠁢󠁳󠁣󠁴󠁿','🏴󠁧󠁢󠁷󠁬󠁳󠁿',
                      '🇺🇳','🇺🇸','🇺🇾','🇺🇿','🇻🇺','🇻🇦','🇻🇪','🇻🇳','🇼🇫','🇪🇭','🇾🇪','🇿🇲','🇿🇼','⌚️',
                      '📱','📲','💻','⌨️','🖥','🖨','🖱','🖲','🕹','🗜','💽','💾','💿','📀',
                      '📼','📷','📸','📹','🎥','📽','🎞','📞','☎️','📟','📠','📺','📻','🎙',
                      '🎚','🎛','🧭','⏱','⏲','⏰','🕰','⌛️','⏳','📡','🔋','🔌','💡','🔦',
                      '🕯','🧯','🛢','💸','💵','💴','💶','💷','💰','💳','💎','⚖️','🧰','🔧',
                      '🔨','⚒','🛠','⛏','🔩','⚙️','🧱','⛓','🧲','🔫','💣','🧨','🔪','🗡','⚔️',
                      '🛡','🚬','⚰️','⚱️','🏺','🔮','📿','🧿','💈','⚗️','🔭','🔬','🕳','💊','💉',
                      '🧬','🦠','🧫','🧪','🌡','🧹','🧺','🧻','🚽','🚰','🚿','🛁','🛀','🧼',
                      '🧽','🧴','🛎','🔑','🗝','🚪','🛋','🛏','🛌','🧸','🖼','🛍','🛒','🎁',
                      '🎈','🎏','🎀','🎊','🎉','🎎','🏮','🎐','🧧','✉️','📩','📨','📧','💌',
                      '📥','📤','📦','🏷','📪','📫','📬','📭','📮','📯','📜','📃','📄','📑',
                      '🧾','📊','📈','📉','🗒','🗓','📆','📅','🗑','📇','🗃','🗳','🗄','📋',
                      '📁','📂','🗂','🗞','📰','📓','📔','📒','📕','📗','📘','📙','📚','📖',
                      '🔖','🧷','🔗','📎','🖇','📐','📏','🧮','📌','📍','✂️','🖊','🖋','✒️','🖌',
                      '🖍','📝','✏️','🔍','🔎','🔏','🔐','🔒','🔓']
        self.update_config(config)
        self.emoji_size = 128
        print('Downloading assets...')
        urllib.request.urlretrieve("https://github.com/dash-uvic/ece471_536-S2022/raw/main/duck-hunt/NotoSansSC-Regular.otf", "NotoSansSC-Regular.otf")
        urllib.request.urlretrieve("https://github.com/dash-uvic/ece471_536-S2022/raw/main/duck-hunt/emojis.npy", "emojis.npy")
        self.emojies_master = np.load('emojis.npy')
        (_, __), (imgs, ___) = cifar100.load_data()
        self.background_parts = imgs.copy()
        self.background_parts[:,:,:,0] = imgs[:,:,:,2] 
        self.background_parts[:,:,:,2] = imgs[:,:,:,0]

    def update_config(self, config):
        self.config = config
        self.emoji_augs = []
        # Emoji Augs
        if self.config['emoji_transforms']['Add']:
            self.emoji_augs.append(iaa.Add((-40, 40), per_channel=0.5))
        if self.config['emoji_transforms']['Multiply']:
            self.emoji_augs.append(iaa.Multiply((0.5, 1.5), per_channel=0.5))
        if self.config['emoji_transforms']['Cutout']:
            self.emoji_augs.append(iaa.Cutout(nb_iterations=2))
        if self.config['emoji_transforms']['CoarseDropout']:
            self.emoji_augs.append(iaa.CoarseDropout((0.0, 0.05), size_percent=(0.02, 0.25)))
        if self.config['emoji_transforms']['CoarseSaltAndPepper']:
            self.emoji_augs.append(iaa.CoarseSaltAndPepper(0.05, size_px=(4, 16)))
        if self.config['emoji_transforms']['JpegCompression']:
            self.emoji_augs.append(iaa.JpegCompression(compression=(70, 99)))
        if self.config['emoji_transforms']['BlendAlpha']:
            self.emoji_augs.append(iaa.BlendAlpha((0.0, 1.0), iaa.Grayscale(1.0)))
        if self.config['emoji_transforms']['BlendAlphaRegularGrid']:
            self.emoji_augs.append(iaa.BlendAlphaRegularGrid(nb_rows=(1, 8), nb_cols=(1, 8),foreground=iaa.Multiply(0.0)))
        if self.config['emoji_transforms']['GaussianBlur']:
            self.emoji_augs.append(iaa.GaussianBlur(sigma=(0.0, 1.0)))
        if self.config['emoji_transforms']['MotionBlur']:
            self.emoji_augs.append(iaa.MotionBlur(k=5, angle=[-45, 45]))
        if self.config['emoji_transforms']['MultiplyHueAndSaturation']:
            self.emoji_augs.append(iaa.MultiplyHueAndSaturation(mul_hue=(0.75, 1.25)))
        if self.config['emoji_transforms']['Grayscale']:
            self.emoji_augs.append(iaa.Grayscale(alpha=(0.0, 1.0)))
        if self.config['emoji_transforms']['ChangeColorTemperature']:
            self.emoji_augs.append(iaa.ChangeColorTemperature((1100, 10000)))
        if self.config['emoji_transforms']['SigmoidContrast']:
            self.emoji_augs.append(iaa.SigmoidContrast(gain=(3, 10), cutoff=(0.4, 0.6), per_channel=True))
        if self.config['emoji_transforms']['CLAHE']:
            self.emoji_augs.append(iaa.CLAHE(clip_limit=(1, 5)))
        if self.config['emoji_transforms']['Emboss']:
            self.emoji_augs.append(iaa.Emboss(alpha=(0.0, 0.5), strength=(0.5, 1.5)))
        if self.config['emoji_transforms']['DirectedEdgeDetect']:
            self.emoji_augs.append(iaa.DirectedEdgeDetect(alpha=(0.0, 0.5), direction=(0.0, 1.0)))
        if self.config['emoji_transforms']['Fliplr']:
            self.emoji_augs.append(iaa.Fliplr(0.5))
        if self.config['emoji_transforms']['PiecewiseAffine']:
            self.emoji_augs.append(iaa.PiecewiseAffine(scale=(0.03, 0.15)))
        if self.config['emoji_transforms']['PerspectiveTransform']:
            self.emoji_augs.append(iaa.PerspectiveTransform(scale=(0.01, 0.25)))
        if self.config['emoji_transforms']['WithPolarWarping']:
            self.emoji_augs.append(iaa.WithPolarWarping(iaa.CropAndPad(percent=(-0.15, 0.15))))
        if self.config['emoji_transforms']['Rot90']:
            self.emoji_augs.append(iaa.Rot90([1, 3]))
        if self.config['emoji_transforms']['ElasticTransformation']:
            self.emoji_augs.append(iaa.ElasticTransformation(alpha=(0, 2.0), sigma=0.15))
        if self.config['emoji_transforms']['Jigsaw']:
            self.emoji_augs.append(iaa.Jigsaw(nb_rows=4, nb_cols=4))

    def get_random_emoji_img(self):
            
        return cv2.resize(self.emojies_master[random.randint(0,self.emojies_master.shape[0]-1)],(self.emoji_size,self.emoji_size))

    def get_background(self):
        background = np.zeros((512,512,3), np.uint8)
        for x in range(512//self.emoji_size):
            for y in range(512//self.emoji_size):
                background[x*self.emoji_size:(x+1)*self.emoji_size,y*self.emoji_size:(y+1)*self.emoji_size] = cv2.resize(
                                        self.background_parts[random.randint(0,self.background_parts.shape[0]-1)], (self.emoji_size,self.emoji_size))
        return background

    def augment_emoji(self, emoji):
        transformation_aug = iaa.Sequential([iaa.Rotate((-180, 180)),iaa.SomeOf((0, 5), self.emoji_augs)],random_order=True)
        images_aug = transformation_aug(image=emoji)
        return images_aug

    def generate_image_and_points(self):
        '''
        Returns a target image, emoji example (uncorrupted), and ground truth gt_points. For your testing and development
        '''
        emoji_target = self.get_random_emoji_img()
        test_image   = self.get_background()

        gt_points = []

        for _ in range(random.randint(1,10)):
            x = random.randint(0,512-self.emoji_size-1)
            y = random.randint(0,512-self.emoji_size-1)
            gt_points.append((x+self.emoji_size//2,y+self.emoji_size//2))
            augmented_emoji = self.augment_emoji(emoji_target)
            test_image[x:x+self.emoji_size,y:y+self.emoji_size] = np.where(
                np.expand_dims(np.sum(augmented_emoji,axis=-1) > 25,-1), augmented_emoji, test_image[x:x+self.emoji_size,y:y+self.emoji_size])
        
        test_image_agus = [iaa.AdditiveGaussianNoise(scale=(0, 0.1*255)),
                            iaa.GaussianBlur(sigma=(0.0, 0.25))]

        test_image = iaa.Sequential(test_image_agus)(image=test_image)

        return test_image, emoji_target, gt_points

    def score_function(self, ground_truth, predicted):
        '''
        Pass this function your predictions and ground truth to get your scores. 
        '''
        distances = np.zeros((len(ground_truth),len(predicted)))
        for x in range(len(ground_truth)):
            for y in range(len(predicted)):
                distances[x,y] = (ground_truth[x][0]-predicted[y][0])**2+(ground_truth[x][1]-predicted[y][1])**2

        distances = np.sqrt(distances)
        scores = []
        for x in range(len(predicted)):
            min_index = np.argmin(distances)
            scores.append(np.min(distances))
            distances[min_index//len(predicted),:] = 1e10
            if np.mean(distances) == 1e10:
                break

        while len(scores) < max([len(ground_truth),len(predicted)]):
            scores.append(512)

        return np.mean(scores)
        
    def offical_test(self, function, config):
        '''
        Runs an official test of 10 runs of your function! 
        Pass a function which takes in the inputs [image, emoji] and returns a lists of poits [(x,y),(x_2,y_2)] for the guesses of each emoji location.
        This function will use a randomized seed every time not your pre-set seed used for debugging.
        '''
        self.update_config(config)
        scores = []
        for x in range(10):
            test_image, emoji_target, gt_points = self.generate_image_and_points()
            scores.append(self.score_function(gt_points, function(test_image, emoji_target)))
        
        print("~~~~~STARTING TEST~~~~~~")
        print("Enabled Augmentations....")
        for aug in config['emoji_transforms'].keys():
            if config['emoji_transforms'][aug]:
                print('    ', aug)
        print("Scores (lower is better)....")
        for x, score in enumerate(scores):
            print('    Run',x,'->',score)

        print('Final Score is:', np.mean(scores))


if __name__ == '__main__':                

    config = {
        'emoji_transforms':
        {
            "Add" : True,
            "Multiply" : True,
            "Cutout" : True,
            "CoarseDropout" : True,
            "CoarseSaltAndPepper" : True,
            "JpegCompression" : True,
            "BlendAlpha" : True,
            "BlendAlphaRegularGrid" : True,
            "GaussianBlur" : True,
            "MotionBlur" : True,
            "MultiplyHueAndSaturation" : True,
            "Grayscale" : True,
            "ChangeColorTemperature" : True,
            "SigmoidContrast" : True,
            "CLAHE" : True,
            "Emboss" : True,
            "DirectedEdgeDetect" : True,
            "Fliplr" : True,
            "PiecewiseAffine" : True,
            "PerspectiveTransform" : True,
            "WithPolarWarping" : True,
            "Rot90" : True,
            "ElasticTransformation" : True,
            "Jigsaw" : True,
        }
    }

    test = EmojiHunt(config)

    a = [(0,1),(15,15), (600,600), (0,0)]
    b = [(5,1),(15,20), (600,605)]
    print(test.score_function(a,b))

    def test_bad_function(image, emoji):
        return [(random.randint(0,512),random.randint(0,512))]

    test.offical_test(test_bad_function,config)

    while True:
        image, emoji, points = test.generate_image_and_points()
        cv2.imshow('', image)
        cv2.waitKey(-1)