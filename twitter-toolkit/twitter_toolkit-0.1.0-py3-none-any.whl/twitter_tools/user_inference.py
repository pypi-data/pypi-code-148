from m3inference import M3Twitter
import progressbar
import os

class TwitterUserInference:
    
    def __init__(self, cache_dir = 'twitter_cache') -> None:
        self.m3twitter = M3Twitter(cache_dir=cache_dir)
    
    def infer_users(self,users, lang, postprocess_threshold=None):
        """
        Infers age, gender and if it is an organization for twitter users.  
        There is no guarantee of infering all the users (like users who have been deleted from Twitter).
        
        Parameters
        ----------
        users : list of users(dict or json)
            Each user most at least have the following keys: `id`, `name`,
            `screen_name`, `description`, `profile_image_url`
            from a twitter object
        lang : str, or list str
            A string representing the languages for the users if the language is
            the same for all, or a list of languages, one for each user.
            Supported languages are `['en', 'cs', 'fr', 'nl', 'ar', 'ro', 'bs', 
            'da', 'it', 'pt', 'no', 'es', 'hr', 'tr', 'de', 'fi', 'el', 'ru',
            'bg', 'hu', 'sk', 'et', 'pl', 'lv', 'sl', 'lt', 'ga', 'eu', 'mt', 
            'cy', 'rm', 'is', 'un']`
        postprocess_threshold: float between 0 and 1 or None
            If different than `None`, the threshold of confidence 
            to be considered an organization and remove the inference of 
            sex and age from the result. This would be done to have coherence
            in the results
        """

        if isinstance(lang, str):
            lang_arr = [lang for i in range(len(users))]
        elif isinstance(lang, list):
            if len(lang) != len(users):
                raise Exception("language list provided has a different length than users")
            lang_arr = lang
        else:
            raise Exception("lang type not supported")
        
        print("Retrieving profile images")

        # retrieve profile image
        transformed_users = []
        for i,u in enumerate(progressbar.progressbar(users, max_value=len(users))):
            u['lang'] = lang_arr[i]
            u['id_str'] = u['id']
            u['screen_name'] = u['username']
            try:
                out = self.m3twitter.transform_jsonl_object(u,img_path_key='profile_image_url', lang_key='lang')
                transformed_users.append(out)
            except:
                print('error')
                continue
        
        # Check that images are dowloaded
        valid_users = []
        for u in transformed_users:
            if os.path.isfile(u['img_path']):
                valid_users.append(u)
        
        print("Infering...")

        inferences = self.m3twitter.infer(valid_users)

        if postprocess_threshold:
            inferences = self.postprocess_results(inferences, postprocess_threshold)
        
        return inferences

    def postprocess_results(self, inferences, threshold=0.5):
        """
        Post process the inference results for have some coherence.
        It is done by remove the sex and age inference in inference organizations.

        Parameters
        ----------
        inference: Dict result of M3Twitter inference
        """

        for _, inf in inferences.items():
            if inf['org']['is-org']>= threshold:
                del inf['gender']
                del inf['age']
        
        return inferences