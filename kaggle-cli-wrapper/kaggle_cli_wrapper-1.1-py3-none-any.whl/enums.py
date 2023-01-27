from dataclasses import dataclass


@dataclass
class KaggleCompetitionDatasets:
    """
    Kaggle competition datasets
    For getting other datasets, please use the list 
    function to get correct dataset name
    """
    bike_sharing: str = "bike-sharing-demand"
    breat_cancer_dtection_rsna: str = "rsna-breast-cancer-detection"
    facial_keypoints_detection: str = "facial-keypoints-detection"
    getting_starting_with_gans: str = "gan-getting-started"
    icecube_detector_neutrinos: str = "icecube-neutrinos-in-deep-ice"
    list_all_competitions: str = "kaggle competitions list"
    survey_studies: str = "kaggle-survey-2022"
    transfer_learning_food_recognition: str = "transfer-learning-on-food-recognition"
    

@dataclass
class KaggleGeneralDatasets:
    """
    Datasets listed here are sorted by maximum votes.
    For getting other datasets, please use the list 
    function to get correct dataset name
    """
    covid_dataset: str = "allen-institute-for-ai/CORD-19-research-challenge"
    nfl_dataset: str = "maxhorowitz/nflplaybyplay2009to2016"
    cityscapes_train_val_test: str = "chrisviviers/cityscapes-leftimg8bit-trainvaltest"