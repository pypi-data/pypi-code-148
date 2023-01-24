"""Functions to manipulate an Annotation Lab JSON export into an appropriate layout for training
assertion, relation extraction and NER models
"""
import requests
from typing import Optional, List, IO
import os
import random as rand
from io import BytesIO
import json
from zipfile import ZipFile
import itertools
import datetime

from sparknlp_jsl.utils.imports import is_module_importable

is_module_importable(lib='pandas',raise_exception=True,pip_name='pandas',message_type='module' )
import pandas as pd

from pyspark.sql import SparkSession
from sparknlp_jsl.training_log_parser import ner_log_parser
from IPython.display import display
from pyspark.sql import functions as F
from sparknlp.training import CoNLL
from sparknlp_jsl.eval import NerDLMetrics

from .utils.alab_utils import get_nlp_token_pipeline,get_rel_df, \
    get_ner_sentence_borders, get_single_task_conll, get_nlp_pos_pipeline, get_token_df



class AnnotationLab():
    """Class to interact with John Snow Labs's Annotation Lab
    """

    def __init__(self):
        """
        Class Constructor.
        """

        self.username = None
        self.password = None
        self.client_secret = None
        self.cookies = None
        self.base_url = None
        self.client_id = None
        self.http_success_codes = [200, 201, 203]

    def set_credentials(self, username, password, client_secret, annotationlab_url="https://annotationlab.johnsnowlabs.com"):
        """
        Set credentials to connect to your Annotation Lab instance.
        :param username: Username
        :type username: str
        :param password: Password
        :type password: str
        :param client_secret: Client Secret for your installation (Every installation of Annotation Lab has a secret code).
        :type client_secret: str
        :param annotationlab_url: URL of Annotation Lab. Default: JSL's Annotation Lab (https://annotationlab.johnsnowlabs.com).
        :type annotationlab_url: str
        """
        self.username = username
        self.password = password
        self.client_secret = client_secret
        self.cookies = None
        self.request_headers = {
            "Content-Type": "application/json",
            "accept": "*/*",
        }
        self.url_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "*/*",
        }
        self.base_url = annotationlab_url.strip('/')
        if self.base_url.startswith("https://annotationlab.johnsnowlabs.com"):
            self.client_id = "annotator"
        else:
            self.client_id = "annotationlab"


    def __create_url(self, path):
        """
        Generates a URL.
        """
        if self.base_url is None:
            raise Exception("Annotation Lab credentials not found.\nPlease set credentials (username, password, client_secret, annotationlab_url) using 'set_credentials' method.")
        return self.base_url+path

    def __make_post_request(self, url, jsn, data, with_cookies=True, show_message=True, header_type='json'):
        """
        Sends post request.
        """

        if header_type=='json':
            headers = self.request_headers
        else:
            headers = self.url_header

        if with_cookies:
            self.__authenticate()
            response = requests.post(url, headers=headers, cookies=self.cookies, json=jsn, data=data)
        else:
            response = requests.post(url, headers=headers, json=jsn, data=data)

        if response.status_code in self.http_success_codes:
            if show_message:
                print ("Operation completed successfully. Response code: {}".format(response.status_code))
        else:
            print ("Operation failed. Response code: {}\nDetails: {}".format(response.status_code, response.json()))

        if response.headers.get('content-type') in ['application/zip', 'application/octet-stream']:

            zipfile = ZipFile(BytesIO(response.content))
            with zipfile.open(zipfile.namelist()[0]) as f:
                data = f.read()
            project_json = json.loads(data)

            return response.status_code, project_json

        return response.status_code, response.json()

    def __make_get_request(self, url):
        """
        Sends a get request.
        """

        self.__authenticate()
        response = requests.get(url, headers=self.request_headers, cookies=self.cookies)

        if response.status_code in self.http_success_codes:
            print ("Operation completed successfully. Response code: {}".format(response.status_code))
        else:
            print ("Operation failed. Response code: {}\nDetails: {}".format(response.status_code, response.json()))

        return response.status_code, response.json()

    def __make_delete_request(self, url, jsn, data):
        """
        Sends a delete request.
        """

        self.__authenticate()
        response = requests.delete(url, headers=self.request_headers, cookies=self.cookies, json=jsn, data=data)

        if response.status_code in self.http_success_codes:
            print ("Operation completed successfully. Response code: {}".format(response.status_code))
        else:
            print ("Operation failed. Response code: {}\nDetails: {}".format(response.status_code, response.json()))

        return response.status_code, response.json()

    def __authenticate(self):
        """
        Authenticates Username and Password. Also, sets cookies.
        """

        if self.username == None or self.password == None or self.client_secret == None or self.client_id == None:
            raise Exception("Annotation Lab credentials not found.\nPlease set credentials (username, password, client_secret, annotationlab_url) using 'set_credentials' method.")

        ## cookie URL: "https://annotationlab.johnsnowlabs.com/openid-connect/token"
        url = self.__create_url("/openid-connect/token")

        jsn = {
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response_code, auth_info = self.__make_post_request(url, jsn=jsn, data={}, with_cookies=False, show_message=False)

        cookies = {
            'access_token': f"Bearer {auth_info['access_token']}",
            'refresh_token': auth_info['refresh_token']
        }
        self.cookies = cookies

    def __generate_random_color(self):
        """
        Generates random HEX color codes.
        :rtype str
        """

        r = lambda: rand.randint(0,200)
        return '#%02x%02x%02x' % (r(), r(), r())

    def get_all_projects(self):
        """
        Get a JSON object containing details of all visible projects in Annotation Lab.
        :rtype dict
        """

        url = self.__create_url("/api/projects")

        response_code, content = self.__make_get_request(url)

        return content

    def get_project_config(self, project_name):
        """
        Get configuration details of a project as JSON.
        :param project_name: Project Name
        :type project_name: str
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}".format(project_name))

        response_code, content = self.__make_get_request(url)

        return content

    def create_project(self, project_name, project_description='', project_sampling='', project_instruction=''):
        """
        Create a new project.
        :param project_name: Project Name
        :type project_name: str
        :param project_description: Project Description
        :type project_description: str
        :param project_sampling: Random or Sequential sampling while showing tasks to annotators
        :type project_sampling: str
        :param project_instruction: Annotation Guidelines
        :type project_instruction: str
        :rtype dict
        """

        jsn = {
            "project_name": project_name,
            "project_description": project_description,
            "project_sampling": project_sampling,
            "project_instruction": project_instruction
        }

        url = self.__create_url("/api/projects/create")

        response_code, content = self.__make_post_request(url, jsn=jsn, data={})

        return content

    def delete_project(self, project_name, confirm=False):
        """
        Delete an existing project.
        :param project_name: Project Name
        :type project_name: str
        :param confirm: If set to True, no input required for confirmation. Default: False.
        :type confirm: boolean
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}/delete".format(project_name))

        if not confirm:
            inp = input('Deleting Project. Press "Y" to confirm.').lower()
            if inp == 'y':
                response_code, content = self.__make_delete_request(url, jsn={}, data={})
                return content
            else:
                return {}
        else:
            response_code, content = self.__make_delete_request(url, jsn={}, data={})
            return content

    def set_project_config(self, project_name, classification_labels=[], ner_labels=[], assertion_labels=[], relations_labels=[]):
        """
        Set configuration of a project.
        :param project_name: Project Name
        :type project_name: str
        :param classification_labels: List of document classification classes. By default, it'd be multiclass classification.
        :type classification_labels: List
        :param ner_labels: List of NER classes
        :type ner_labels: List
        :param assertion_labels: List of assertion classes
        :type assertion_labels: List
        :param relations_labels: List of different types of relations.
        :type relations_labels: List
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}/save-config".format(project_name))

        if classification_labels == [] and ner_labels == [] and assertion_labels:
            raise Exception ('No configuration found. Please provide labels for Classification, NER or Assertion.')

        if relations_labels != [] and (ner_labels == [] and assertion_labels==[]):
            raise Exception ("NER/Assertion configuration not found, which is a prerequisite for setting Relation Extraction configuration.")

        base_layout = """<View>\n{}\n{}\n<View style="white-space: pre-wrap">\n<Text name="text" value="$text"/>\n</View>{}\n</View>"""


        ner_ass_conf = ""
        if ner_labels+assertion_labels != []:
            ner_config_template = """<View style="padding: 0 1em; margin: 1em 0; background: #f1f1f1; position: sticky; top: 0; border-radius: 1px; overflow: auto; z-index:101;">\n<Labels name="label" toName="text">\n{}\n</Labels>\n</View>"""
            ner_conf = ["""<Label value="{}" background="{}"/>""".format(lbl, self.__generate_random_color()) for lbl in ner_labels ]
            assertion_conf = ["""<Label value="{}" assertion="true" background="#f1c40f"/>""".format(lbl) for lbl in assertion_labels ]
            ner_ass_conf = ner_config_template.format("\n".join(ner_conf+assertion_conf))

        re_conf = ""
        if relations_labels != []:
            re_config_template = """<Relations>\n{}\n</Relations>"""
            re_conf = "\n".join(["""<Relation value="{}" background="yellowgreen"/>""".format(lbl) for lbl in relations_labels])
            re_conf = re_config_template.format(re_conf)

        classification_conf = ""
        if classification_labels != []:
            classification_config_template = """<Choices name="sentiment" toName="text" choice="multiple">\n<View>\n<Header value="Select Class" />{}\n</View>\n</Choices>"""
            classification_conf = "\n".join([ """<Choice value="{}"/>""".format(clss)  for clss in classification_labels])
            classification_conf = classification_config_template.format(classification_conf)

        data = {"label_config": base_layout.format(ner_ass_conf, re_conf, classification_conf)}

        response_code, content = self.__make_post_request(url, jsn={}, data=data, header_type='url')

        return content

    #def edit_project_config(self, project_name, ner_labels, assertion_labels, ):


    def upload_tasks(self, project_name, task_list, title_list = [], id_offset=0):
        """
        Upload tasks to a project in Annotation Lab.
        :param project_name: Project Name
        :type project_name: str
        :param task_list: List of documents (text).
        :type task_list: List
        :param title_list: Option for providing custom titles for each task. If defined, it's length should be equal to number of tasks
        :type title_list: List
        :param id_offset: Increment offset for document ID. Useful when uploading in batches. Default: 0.
        :type id_offset: int
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}/import".format(project_name))
        print ("Uploading {} task(s).".format(len(task_list)))

        if title_list != []:
            assert (len(title_list) == len(task_list))
            upload_jsn = [ {"text": zp[0], "title": zp[1], 'id': index+id_offset} for index, zp in enumerate(zip(task_list, title_list))]
        else:
            upload_jsn = [ {"text": zp, "title": "task_{}".format(index+id_offset), 'id': index+id_offset} for index, zp in enumerate(task_list)]

        response_code, content = self.__make_post_request(url, jsn=upload_jsn, data={})

        return content

    def delete_tasks(self, project_name, task_ids, confirm=False):
        """
        Delete tasks of a project in Annotation Lab.
        :param project_name: Project Name
        :type project_name: str
        :param task_id: List of tasks ids
        :type task_list: List
        :param confirm: If set to True, no input required for confirmation. Default: False.
        :type confirm: boolean
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}/tasks_delete".format(project_name))
        print ("Deleting {} task(s).".format(len(task_ids)))
        jsn = {"task_ids": task_ids}

        if not confirm:
            inp = input('Press "Y" to confirm.').lower()
            if inp == 'y':
                response_code, content = self.__make_delete_request(url, jsn=jsn, data={})
                return content
        else:
            response_code, content = self.__make_delete_request(url, jsn=jsn, data={})
            return content

    def get_annotations(self, project_name, output_name, save_dir="."):
        """
        Get / Export annotations of a project in Annotation Lab.
        :param project_name: Project Name
        :type project_name: str
        :param output_name: file name where to write the result as json.
        :type output_name: str
        :param save_dir: directory location where to save output json.
        :type save_dir: str
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}/export?format=JSON".format(project_name))

        response_code, content = self.__make_post_request(url, jsn={}, data={})

        print ('Exported {} Tasks'.format(len(content)))

        try:
            os.mkdir(save_dir)
        except:
            pass

        ex_pth = "{}/{}.json".format(save_dir, output_name)
        with open(ex_pth, 'w', encoding='utf-8') as f:
            f.write(json.dumps(content))

        print ('Annotations saved as {}.'.format(ex_pth))

        return content

    def get_conll_data(self, spark: SparkSession, input_json_path: str, output_name: str, save_dir: str = 'exported_conll',
                       ground_truth: bool = False, excluded_labels: List[str] = None,
                       excluded_task_ids: Optional[List[int]] = None, excluded_task_titles: Optional[List[str]] = None,
                       regex_pattern: str = None) -> IO:
        """Generates a CoNLL file from an Annotation Lab JSON export
        :param spark: Spark session with spark-nlp-jsl jar
        :type spark: SparkSession
        :param input_json_path: path to Annotation Lab JSON export
        :type input_json_path: str
        :param output_name: name of the CoNLL file to save
        :type output_name: str
        :param save_dir: path for CoNLL file saving directory, defaults to 'exported_conll'
        :type save_dir: str
        :param ground_truth: set to True to select ground truth completions, False to select latest completions,
        defaults to False
        :type ground_truth: bool
        :param excluded_labels: labels to exclude from CoNLL; these are all assertion labels and irrelevant NER labels,
        defaults to None
        :type excluded_labels: list
        :param excluded_task_ids: list of Annotation Lab task IDs to exclude from CoNLL, defaults to None
        :type excluded_task_ids: list
        :param excluded_task_titles: list of Annotation Lab task titles to exclude from CoNLL, defaults to None
        :type excluded_task_titles: list
        :param regex_pattern: set a pattern to use regex tokenizer, defaults to regular tokenizer if pattern not defined
        :type regex_pattern: str
        :return: CoNLL file
        :rtype: IO
        """
        with open(input_json_path, 'r', encoding='utf-8') as json_file:
            json_outputs = json.load(json_file)

        json_outputs = sorted(json_outputs, key=lambda d: d["id"])

        bulk_conll_lines = []


        lp_pipeline = get_nlp_pos_pipeline (spark=spark, regex_pattern=regex_pattern)
        token_lp_pipeline = get_nlp_token_pipeline(spark=spark, regex_pattern=regex_pattern)

        for _, output in enumerate(json_outputs):
            in_conll_lines = get_single_task_conll(output=output, pos_pipeline=lp_pipeline,
                                                   token_pipeline=token_lp_pipeline, ground_truth=ground_truth,
                                                   excluded_labels=excluded_labels, excluded_task_ids=excluded_task_ids,
                                                   excluded_task_titles=excluded_task_titles)
            bulk_conll_lines.extend(in_conll_lines)

        try:
            os.mkdir(save_dir)
        except:
            pass

        with open(f'{save_dir}/{output_name}.conll', 'w', encoding='utf-8') as f:
            for i in bulk_conll_lines:
                f.write(i)

        print(f'Saved in location: {save_dir}/{output_name}.conll')

        print('\nPrinting first 30 lines of CoNLL for inspection:\n')

        return bulk_conll_lines[:30]



    def get_assertion_data(self, spark: SparkSession, input_json_path: str, assertion_labels: List[str], relevant_ner_labels:
    List[str], ground_truth: bool = False, unannotated_label: Optional[str] = None,
                           regex_pattern: Optional[str] = None, unannotated_label_strategy: Optional[str] = None,
                           unannotated_label_strategy_dict: Optional[dict] = None,
                           included_task_ids: Optional[List[int]] = None,
                           excluded_task_ids: Optional[List[int]] = None,
                           excluded_task_titles: Optional[List[str]] = None, seed: int = None) -> pd.DataFrame:
        """Generate a dataframe to train assertion models in Spark NLP from an Annotation Lab JSON export
        :param spark: Spark session with spark-nlp-jsl jar
        :type spark: SparkSession
        :param input_json_path: path to Annotation Lab JSON export
        :type input_json_path: str
        :param assertion_labels: annotated assertion labels to train on
        :type assertion_labels: list[str]
        :param relevant_ner_labels: relevant NER labels that are assigned assertion labels
        :type relevant_ner_labels: list[str]
        :param ground_truth: set to True to select ground truth completions, False to select latest completions,
        defaults to False
        :type ground_truth: bool
        :param unannotated_label: assertion label to assign to entities that have no assertion, defaults to None
        :type unannotated_label: str
        :param regex_pattern: set a pattern to use regex tokenizer, defaults to regular tokenizer if pattern not defined
        :type regex_pattern: str
        :param unannotated_label_strategy: set the strategy to control the number of occurrences of the unannotated
        assertion label in the output dataframe, options are 'weighted' or 'counts', 'weighted' allows to sample using a
        fraction, 'counts' allows to sample using absolute counts, defaults to None
        :type unannotated_label_strategy: str
        :param unannotated_label_strategy_dict: dictionary in the format {'ENTITY_LABEL': sample_weight_or_counts} to
        control the number of occurrences of the unannotated assertion label in the output dataframe, where 'ENTITY_LABEL'
        are the NER labels that are assigned the unannotated assertion label, and sample_weight_or_counts should be between
        0 and 1 if `unannotated_label_strategy` is 'weighted' or between 0 and the max number of occurrences of that NER
        label if `unannotated_label_strategy` is 'counts'
        :type unannotated_label_strategy_dict: dict
        :param excluded_task_ids: list of Annotation Lab task IDs to exclude from output dataframe, defaults to None
        :type excluded_task_ids: list
        :param excluded_task_titles: list of Annotation Lab task titles to exclude from output dataframe, defaults to None
        :type excluded_task_titles: list
        :param seed: Makes sure we get the same data every time we execute the code. Defaults to None
        :type seed: int
        :return: dataframe in appropriate layout for training assertion models
        :rtype: pd.DataFrame
        """



        lp_pipeline = get_nlp_token_pipeline(spark=spark, regex_pattern=regex_pattern)

        with open(input_json_path, 'r', encoding='utf-8') as json_file:
            output_list = json.load(json_file)

        if excluded_task_ids is not None:
            output_list = [task for task in output_list if task['id'] not in excluded_task_ids]

        if included_task_ids is not None:
            output_list = [task for task in output_list if task['id'] in included_task_ids]

        ner_dicts = []
        id_title_map = {}
        for w, output in enumerate(output_list):

            map_id = str(output["id"])

            try:
                map_title = output['data']['title']
            except:
                map_title = "untitled"

            id_title_map[map_id] = map_title

            try:
                text = output['data']['text']
                if ground_truth:
                    for i in range(len(output['completions'])):
                        if output['completions'][i]['honeypot']:
                            gt_index = i

                elif ground_truth is False or ground_truth is None:
                    gt_index = -1

                doc_id = output['id']

            except:
                print('EXCEPTION:', input_json_path.split('/')[-1], 'Task ID#', doc_id)
                continue

            lines = [(line.result, line.begin, line.end) for line in lp_pipeline.fullAnnotate(text)[0]['sentence']]

            sent_df = pd.DataFrame(lines, columns=['sentence', 'begin', 'end'])


            try:
                for _, i in enumerate(output['completions'][gt_index]['result']):


                    if i['type'] == 'labels':
                        assertion_label = i['value']['labels'][0]

                        sentence = sent_df[(i['value']['start'] >= sent_df.begin) &
                                           (i['value']['start'] <= sent_df.end) &
                                           (i['value']['end'] - 1 >= sent_df.begin) &
                                           (i['value']['end'] - 1 <= sent_df.end)]

                        if len(sentence) == 0:
                            continue

                        sent = sentence['sentence'].values[0]

                        begin = i['value']['start'] - sentence['begin'].values[0]
                        end = i['value']['end'] - sentence['begin'].values[0]


                        token_df = get_token_df(sent)


                        ix = token_df[(token_df.begin >= begin) & (token_df.end < end)].index

                        if len(ix) == 0:
                            continue
                        left_ix = min(ix)
                        right_ix = max(ix)

                        ner_dicts.append((doc_id, sent, i['value']['text'], assertion_label, left_ix, right_ix,
                                          i['value']['start'], i['value']['end'], begin, end))

            except Exception as e:

                print(e)
                print('EXCEPTION:', input_json_path.split('/')[-1], 'Task ID#', doc_id)
                continue

            print('Processing Task ID#', doc_id)

        ass_df = pd.DataFrame(ner_dicts,
                              columns=['task_id', 'text', 'target', 'label', 'start', 'end', 'doc_start_index',
                                       'doc_end_index', 'char_begin', 'char_end'])
        ass_df["json_file_path"] = input_json_path

        relevant_ner_df = ass_df[ass_df['label'].isin(relevant_ner_labels)]
        relevant_ass_df = ass_df[ass_df['label'].isin(assertion_labels)]

        ass_inner_duplicates = relevant_ass_df.merge(relevant_ner_df,
                                                     on=['task_id', 'text', 'target', 'start', 'end', 'doc_start_index',
                                                         'doc_end_index', 'json_file_path','char_begin', 'char_end'], how='inner').rename(
            columns={'label_x': 'label', 'label_y': 'ner_label'})

        if unannotated_label is not None:
            ass_outer_duplicates = relevant_ass_df.merge(relevant_ner_df,
                                                         on=['task_id', 'text', 'target', 'start', 'end', 'doc_start_index',
                                                             'doc_end_index', 'json_file_path', 'char_begin', 'char_end'], how='right',
                                                         indicator=True).query('_merge == "right_only"').rename(
                columns={'label_x': 'label', 'label_y': 'ner_label', })

            ass_outer_duplicates['label'] = unannotated_label


            if unannotated_label_strategy == 'weighted':
                sample_data_dict = []
                for key in unannotated_label_strategy_dict:
                    if unannotated_label_strategy_dict[key] > 1:
                        print(f"ERROR: The sampling proportion set for '{key}' was greater than 1. Please choose a value "
                              f"between 0 and 1.")
                    if seed:
                        sample_data = ass_outer_duplicates[ass_outer_duplicates['ner_label'] == key].sample(
                            frac=unannotated_label_strategy_dict[key], random_state=seed)

                    else:
                        sample_data = ass_outer_duplicates[ass_outer_duplicates['ner_label'] == key].sample(
                            frac=unannotated_label_strategy_dict[key])

                    sample_data_dict.append(sample_data)

                ass_outer_duplicates_sampled = pd.concat(sample_data_dict)
                ass_outer_duplicates = ass_outer_duplicates_sampled.copy()

            elif unannotated_label_strategy == 'counts':
                sample_data_dict = []
                for key in unannotated_label_strategy_dict:
                    subset = ass_outer_duplicates[ass_outer_duplicates['ner_label'] == key]
                    subset_length = len(subset)
                    if unannotated_label_strategy_dict[key] > subset_length:
                        print(f"ERROR: The sampling counts set for '{key}' was greater than the maximum number of '{key}' "
                              f"entities in your data. Please choose a value lower than {subset_length}.")

                    if seed:
                        sample_data = subset.sample(n=unannotated_label_strategy_dict[key], random_state=seed)
                    else:
                        sample_data = subset.sample(n=unannotated_label_strategy_dict[key])

                    sample_data_dict.append(sample_data)

                ass_outer_duplicates_sampled = pd.concat(sample_data_dict)
                ass_outer_duplicates = ass_outer_duplicates_sampled.copy()
            ass_df = pd.concat([ass_inner_duplicates, ass_outer_duplicates]).reset_index(drop=True)

            ass_df = ass_df.sort_values(['task_id', 'doc_start_index', 'doc_end_index']).reset_index(drop=True)

        else:
            ass_df = ass_inner_duplicates.copy()
            ass_df = ass_df.sort_values(['task_id', 'doc_start_index', 'doc_end_index']).reset_index(drop=True)


        ass_df['title'] = ass_df['task_id'].astype(str).map(id_title_map)

        if excluded_task_titles is not None:
            ass_df = ass_df[~ass_df['title'].isin(excluded_task_titles)]


        ass_df = ass_df[['task_id', 'title', 'text', 'target', 'ner_label', 'label', 'start', 'end','char_begin', 'char_end']]

        return ass_df

    def get_relation_extraction_data(self, spark: SparkSession, input_json_path: str, ground_truth: bool = False,
                                     negative_relations: bool = False,
                                     assertion_labels: Optional[List[str]] = None,
                                     relations: Optional[List[str]] = None,
                                     relation_pairs: Optional[List[str]] = None,
                                     negative_relation_strategy: Optional[str] = None,
                                     negative_relation_strategy_dict: Optional[dict] = None,
                                     excluded_task_ids: Optional[int] = None,
                                     excluded_task_titles: Optional[List[str]] = None) -> pd.DataFrame:
        """Generate a dataframe to train relation extraction models in Spark NLP from an Annotation Lab JSON export
        :param spark: Spark session with spark-nlp-jsl jar
        :type spark: SparkSession
        :param input_json_path: path to Annotation Lab JSON export
        :type input_json_path: str
        :param ground_truth: set to True to select ground truth completions, False to select latest completions,
        defaults to False
        :type ground_truth: bool
        :param negative_relations: set to True to assign a relation label between entities where no relation was
        annotated, defaults to False
        :type negative_relations: bool
        :param assertion_labels: all assertion labels that were annotated, defaults to None
        :type assertion_labels: list
        :param relations: Name of the relations you want to include. It will discard the rest
        :type relations: list
        :param relation_pairs: plausible pairs of entities for relations, separated by a `-`, use the same casing as
        the annotations, include only one relation direction, defaults to all possible pairs of annotated entities
        :type relation_pairs: list
        :param negative_relation_strategy: set the strategy to control the number of occurrences of the negative relation
        label in the output dataframe, options are 'weighted' or 'counts', 'weighted' allows to sample using a
        fraction, 'counts' allows to sample using absolute counts, defaults to None
        :type negative_relation_strategy: str
        :param negative_relation_strategy_dict: dictionary in the format {'ENTITY1-ENTITY2': sample_weight_or_counts} to
        control the number of occurrences of negative relations in the output dataframe for each entity pair, where
        'ENTITY1-ENTITY2' represent the pairs of entities for relations separated by a `-` (include only one relation
        direction), and sample_weight_or_counts should be between 0 and 1 if `negative_relation_strategy` is 'weighted' or
        between 0 and the max number of occurrences of negative relations if `negative_relation_strategy` is 'counts',
        defaults to None
        :type negative_relation_strategy_dict: dict
        :param excluded_task_ids: list of Annotation Lab task IDs to exclude from output dataframe, defaults to None
        :type excluded_task_ids: list
        :param excluded_task_titles: list of Annotation Lab task titles to exclude from output dataframe, defaults to None
        :type excluded_task_titles: list
        :return: dataframe in appropriate layout for training relation extraction models
        :rtype: pd.DataFrame
        """

        rel_df = get_rel_df(input_json_path=input_json_path, ground_truth=ground_truth)
        if relations is not None:
            rel_df = rel_df[rel_df['relation'].isin(relations)]
        ner_borders_df = get_ner_sentence_borders(spark=spark, input_json_path=input_json_path, ground_truth=ground_truth,
                                                  assertion_labels=assertion_labels)

        official_rel_df_col_names = ["task_id", "sentence", "firstCharEnt1", "firstCharEnt2", "lastCharEnt1",
                                     "lastCharEnt2", "chunk1", "chunk2", "label1", "label2", "rel"]

        full_rel_df = rel_df.merge(ner_borders_df.add_prefix('from_'), left_on='from_id',
                                   right_on='from_chunk_id').merge(ner_borders_df.add_prefix('to_'), left_on='to_id',
                                                                   right_on='to_chunk_id')

        if negative_relations:
            group_df = ner_borders_df.groupby(['ner_sentence_id', 'ner_sentence'])

            new_relations_list = []
            text_list = []
            ner_label_list = []
            text_indexes_list = []
            sentence_list = []
            task_id_list = []

            ind = 0
            for key, group_row in group_df:
                ind += 1
                a_group = group_df.get_group(key)
                a_group = a_group.sort_values(by='sentence_begin')
                x = a_group['ner_label'].values
                y = a_group['text'].values
                ch = a_group['chunk_id'].values
                z = a_group['ner_sentence'].values
                s_e = a_group[['start', 'end']].values
                ner_se = a_group[['ner_sentence_start_border', 'ner_sentence_end_border']].values
                s_be = a_group[['sentence_begin', 'sentence_end']].values
                tides = a_group['task_id'].values

                text_indexes = list(zip(s_e, ner_se, s_be))
                id_w_indexes = list(zip(ch, text_indexes))

                new_relations_list.extend(list(itertools.combinations(ch, 2)))
                text_list.extend(list(itertools.combinations(y, 2)))
                ner_label_list.extend(list(itertools.combinations(x, 2)))
                text_indexes_list.extend(list(itertools.combinations(id_w_indexes, 2)))
                sentence_list.extend(itertools.repeat(z, len(list(itertools.combinations(y, 2)))))
                task_id_list.extend(list(itertools.combinations(tides, 2)))

            new_relations_df = pd.DataFrame(new_relations_list, columns=['from_id', 'to_id'])
            new_relations_df['id_pairs'] = new_relations_df.apply(lambda k: (k['from_id'], k['to_id']), axis=1)
            new_relations_df['sentence'] = sentence_list
            new_relations_df['sentence'] = new_relations_df['sentence'].apply(lambda t: t[0])
            new_relations_df['from_start'] = [i[0][1][2][0] for i in text_indexes_list]
            new_relations_df['to_start'] = [i[1][1][2][0] for i in text_indexes_list]
            new_relations_df['from_end'] = [i[0][1][2][1] for i in text_indexes_list]
            new_relations_df['to_end'] = [i[1][1][2][1] for i in text_indexes_list]
            new_relations_df['from_text'] = [i[0] for i in text_list]
            new_relations_df['to_text'] = [i[1] for i in text_list]
            new_relations_df['from_ner_label'] = [i[0] for i in ner_label_list]
            new_relations_df['to_ner_label'] = [i[1] for i in ner_label_list]
            new_relations_df['task_id'] = [i[0] for i in task_id_list]
            new_relations_df['relation'] = 'O'

            existing_rel_ids = list(zip(full_rel_df['from_id'], full_rel_df['to_id']))
            existing_rel_ids_reverse = [t[::-1] for t in existing_rel_ids]
            existing_rel_ids_all = existing_rel_ids + existing_rel_ids_reverse
            new_relations_df = new_relations_df[
                [x not in existing_rel_ids_all for x in zip(new_relations_df.from_id, new_relations_df.to_id)]]

            new_relations_df = new_relations_df[
                ['task_id', 'sentence', 'from_start', 'to_start', 'from_end', 'to_end', 'from_text', 'to_text',
                 'from_ner_label', 'to_ner_label', 'relation']]
            full_rel_df = full_rel_df[
                ['task_id', 'from_ner_sentence', 'from_sentence_begin', 'to_sentence_begin', 'from_sentence_end',
                 'to_sentence_end', 'from_text', 'to_text', 'from_ner_label', 'to_ner_label', 'relation']]

            new_relations_df.columns = official_rel_df_col_names
            full_rel_df.columns = official_rel_df_col_names
            final_rel_df = pd.concat([full_rel_df, new_relations_df]).reset_index(drop=True)

        else:
            full_rel_df = full_rel_df[
                ['task_id', 'from_ner_sentence', 'from_sentence_begin', 'to_sentence_begin', 'from_sentence_end',
                 'to_sentence_end', 'from_text', 'to_text', 'from_ner_label', 'to_ner_label', 'relation']]
            full_rel_df.columns = official_rel_df_col_names
            final_rel_df = full_rel_df.copy()

        if relation_pairs is not None:
            user_input_rel_pairs = [(i.split('-')[0], i.split('-')[1]) for i in relation_pairs]
            user_input_rel_pairs_reverse = [t[::-1] for t in user_input_rel_pairs]
            candidate_rel_pairs = user_input_rel_pairs + user_input_rel_pairs_reverse
            final_rel_df = final_rel_df[
                [x in candidate_rel_pairs for x in zip(final_rel_df.label1, final_rel_df.label2)]]

        reorder = final_rel_df['firstCharEnt1'] > final_rel_df['firstCharEnt2']

        final_rel_df.loc[reorder, ['firstCharEnt1', 'firstCharEnt2', 'lastCharEnt1', 'lastCharEnt2',
                                   'chunk1', 'chunk2', 'label1', 'label2']] = (
            final_rel_df.loc[reorder, ['firstCharEnt2', 'firstCharEnt1', 'lastCharEnt2', 'lastCharEnt1',
                                       'chunk2', 'chunk1', 'label2', 'label1']].values)

        final_rel_df = final_rel_df.sort_values(['task_id', 'firstCharEnt1']).reset_index(drop=True)

        if excluded_task_ids is not None:
            final_rel_df = final_rel_df[~final_rel_df['task_id'].isin(excluded_task_ids)]

        with open(input_json_path, 'r', encoding='utf-8') as json_file:
            output_list = json.load(json_file)

        id_title_map = {}
        for w, output in enumerate(output_list):

            map_id = str(output["id"])
            try:
                map_title = output["data"]["title"]
            except:
                map_title = "untitled"

            id_title_map[map_id] = map_title

        final_rel_df["title"] = final_rel_df["task_id"].astype(str).map(id_title_map)

        if excluded_task_titles is not None:
            final_rel_df = final_rel_df[~final_rel_df["title"].isin(excluded_task_titles)]

        final_rel_df = final_rel_df[["task_id", "title", "sentence", "firstCharEnt1", "firstCharEnt2", "lastCharEnt1",
                                     "lastCharEnt2", "chunk1", "chunk2", "label1", "label2", "rel"]]

        if negative_relation_strategy == 'weighted':
            sample_data_dict = []
            for key in negative_relation_strategy_dict:
                if negative_relation_strategy_dict[key] > 1:
                    print(f"ERROR: The sampling proportion set for '{key}' was greater than 1. Please choose a value "
                          f"between 0 and 1.")
                dict_input_rel_pairs = [(key.split('-')[0], key.split('-')[1])]
                dict_input_rel_pairs_reverse = [t[::-1] for t in dict_input_rel_pairs]
                dict_candidate_rel_pairs = dict_input_rel_pairs + dict_input_rel_pairs_reverse
                subset_final_rel_df = final_rel_df[final_rel_df['rel'] == 'O']
                sample_data = subset_final_rel_df[
                    [x in dict_candidate_rel_pairs for x in zip(subset_final_rel_df.label1, subset_final_rel_df.label2)]]. \
                    sample(frac=negative_relation_strategy_dict[key])
                sample_data_dict.append(sample_data)
            final_rel_df_sampled_down = pd.concat(sample_data_dict)
            final_rel_df_no_negatives = final_rel_df[final_rel_df['rel'] != 'O']
            final_rel_df = pd.concat([final_rel_df_sampled_down, final_rel_df_no_negatives]).sort_values(
                ['task_id', 'firstCharEnt1']).reset_index(drop=True)

        elif negative_relation_strategy == 'counts':
            sample_data_dict = []
            for key in negative_relation_strategy_dict:
                dict_input_rel_pairs = [(key.split('-')[0], key.split('-')[1])]
                dict_input_rel_pairs_reverse = [t[::-1] for t in dict_input_rel_pairs]
                dict_candidate_rel_pairs = dict_input_rel_pairs + dict_input_rel_pairs_reverse
                subset_final_rel_df = final_rel_df[final_rel_df['rel'] == 'O']
                subset = subset_final_rel_df[
                    [x in dict_candidate_rel_pairs for x in zip(subset_final_rel_df.label1, subset_final_rel_df.label2)]]
                subset_length = len(subset)
                if negative_relation_strategy_dict[key] > subset_length:
                    print(f"ERROR: The sampling counts set for '{key}' was greater than the maximum number of negative "
                          f"relations fpr the '{key}' pairs in your data. Please choose a value lower than "
                          f"{subset_length}.")
                sample_data = subset.sample(n=negative_relation_strategy_dict[key])
                sample_data_dict.append(sample_data)
            final_rel_df_sampled_down = pd.concat(sample_data_dict)
            final_rel_df_no_negatives = final_rel_df[final_rel_df['rel'] != 'O']
            final_rel_df = pd.concat([final_rel_df_sampled_down, final_rel_df_no_negatives]).sort_values(
                ['task_id', 'firstCharEnt1']).reset_index(drop=True)

        return final_rel_df

    def get_classification_data(self, input_json_path, ground_truth=False):
        """Generates a dataframe to train classification models.
        :param input_json_path: path of Annotation Lab exported JSON
        :type input_json_path: str
        :param ground_truth: set to True to select ground truth completions, False to select latest completions,
        defaults to False
        :type ground_truth: boolean
        """

        with open(input_json_path, 'r') as f:
            annotations = json.load(f)

        print ('Processing {} annotation(s).'.format(len(input_json_path)))

        res_df = []
        for ann in annotations:

            if len(ann['completions']) > 0:
                all_classes = []
                if ground_truth:
                    for i in range(len(ann['completions'])):
                        if ann['completions'][i]['honeypot']:
                            ann_results = ann['completions'][i]['result']

                elif ground_truth is False or ground_truth is None:
                    ann_results = ann['completions'][-1]['result']

                for ann_res in ann_results:
                    all_classes += ann_res.get('value', {}).get('choices', [])

                res_df.append({'task_id': ann['id'], 'task_title': ann['data']['title'], 'text': ann['data']['text'], 'class': all_classes})

            else:
                print ('EXCEPTION: No Completion found for TaskID: {}'.format(ann['data']['id']))

        if len(res_df) < 1:
            print ('No Completions Found. Data not generated.')

        return pd.DataFrame(res_df)

    def __generate_hash(self, length=10) -> str:
        """Generates a unique ID
        :param length: character length of ID
        :type length: int
        """
        nums = list(range(48,58))
        uppers = list(range(65,91))
        lowers = list(range(97,123))
        all_chars = nums+uppers+lowers
        return "".join([chr(all_chars[rand.randint(0, len(all_chars)-1)]) for x in range(length)])

    def __build_ner_label(self, chunk: str, start: int, end: int, label: str) -> dict:
        """Generates a Named Entity Annotation object.
        :param chunk: named entity string
        :type chunk: str
        :param start: starting string index of entity
        :type start: int
        :param end: ending string index of entity
        :type end: int
        :param label: entity type
        :type label: str
        """

        id_ = self.__generate_hash()
        ner_label = {
            "from_name": "label",
            "id": id_,
            "source": "$text",
            "to_name": "text",
            "type": "labels",
            "value": {
                "end": end,
                "labels": [label],
                "start": start,
                "text": chunk
            }
        }
        return ner_label

    def __build_re_label(self, from_id: str, to_id: str, direction : str = 'right', labels: List = []) -> dict:
        """Generates a Relation Annotation object.
        :param from_id: unique id of chunk1
        :type from_id: str
        :param tos_id: unique id of chunk2
        :type to_id: str
        :param direction: direction of relation
        :type direction: str
        :param labels: label of relation
        :type labels: list[str]
        """

        label_json = {
            "from_id":from_id,
            "to_id": to_id,
            "type": "relation",
            "direction": "right",
            "labels": labels
        }
        return label_json

    def generate_preannotations(self, all_results: List[dict], document_column: str, ner_columns : List[str], assertion_columns : List[str] = [], relations_columns : List[str] = [], user_name : str = 'model', titles_list : List[str] = [], id_offset : int = 0) -> List[dict]:
        """Generates a JSON that can be imported directly into Annotation Lab as pre-annotations.
        :param all_results: list of annotations on documents using light_pipeline.fullAnnotate or full_pipeline.transform(df).collect()
        :type all_results: list[objects]
        :param document_column: output column name of DocumentAssembler stage
        :type document_column: str
        :param ner_columns: list of column names of ner chunks
        :type ner_columns: list[str]
        :param assertion_columns: list of column names of ner chunks
        :type assertion_columns: list[str]
        :param assertion_columns: list of column names of assertion models
        :type assertion_columns: list[str]
        :param relations_columns: list of column names of relation models
        :type relations_columns: list[str]
        :param user_name: name of model(s). default: model
        :type user_name: str
        :param titles_list: custom list of titles of tasks in Annotation Lab. Default: task_ID
        :type titles_list: list[str]
        :param id_offset: When older tasks are already in Annotation Lab, define the ID offeset to avoid overriting existing tasks. Default: 0
        :type id_offset: int
        """

        print ("Processing {} Annotations.".format(len(all_results)))

        ids_list = list(map(lambda x: x+id_offset, range(len(all_results))))

        if titles_list != []:
            assert len(all_results) == len(titles_list)
        else:
            titles_list = list(map(lambda x: f"task_{x}", ids_list))

        export_anns = []
        summary = {'ner_labels' : set(), 'assertion_labels' : set(), 're_labels' : set()}

        for index, row in enumerate(all_results):

            this_ann = {'predictions': [{'created_username': user_name,
                                         'result': []}],
                        'data': {'title': titles_list[index],
                                 'text': row[document_column][0].result},
                        'id': ids_list[index]
                        }

            annotator_type = None
            if hasattr(row[document_column][0], 'annotator_type'):
                annotator_type = 'annotator_type'
            else:
                annotator_type = 'annotatorType'

            this_chunks = {}

            for ner_column in ner_columns:
                for x in row[ner_column]:
                    if getattr(x, annotator_type) == 'chunk':
                        this_lbl = self.__build_ner_label(x.result, x.begin, x.end+1, x.metadata["entity"])
                        this_ann['predictions'][0]['result'].append(this_lbl)
                        summary['ner_labels'].add(x.metadata["entity"])
                        if int(x.begin) not in this_chunks:
                            this_chunks[int(x.begin)] = this_lbl
                    else:
                        raise Exception("Column '{}' is not of 'chunk' type.".format(ner_column))

            for ner_column in assertion_columns:
                for x in row[ner_column]:
                    if getattr(x, annotator_type) == 'assertion':
                        if int(x.begin) in this_chunks:
                            this_lbl = self.__build_ner_label(this_chunks[int(x.begin)]['value']['labels'][0], x.begin, x.end+1, x.result)
                            this_ann['predictions'][0]['result'].append(this_lbl)
                            summary['assertion_labels'].add(x.result)
                        else:
                            print ("Warning: Skipping assertion for entity at index {}.".format(x.begin))
                    else:
                        raise Exception("Column '{}' is not of 'assertion' type. If using AssertionFilterer, please pass the AssertionFilterer column as ner_columns, and AssertionDLModel column as assertion_columns.".format(ner_column))

            for rel_c in relations_columns:
                for rel in row[rel_c]:
                    et_1 = this_chunks[int(rel.metadata['entity1_begin'])]
                    et_2 = this_chunks[int(rel.metadata['entity2_begin'])]
                    summary['ner_labels'].add(rel.metadata['entity1'])
                    summary['ner_labels'].add(rel.metadata['entity2'])
                    if et_1 not in this_ann['predictions'][0]['result']:
                        this_ann['predictions'][0]['result'].append(et_1)
                    if et_2 not in this_ann['predictions'][0]['result']:
                        this_ann['predictions'][0]['result'].append(et_2)


                    this_ann['predictions'][0]['result'].append(self.__build_re_label(et_1['id'],
                                                                                      et_2['id'], labels=[rel.result]))

                    summary['re_labels'].add(rel.result)

            export_anns.append(this_ann)

        for k, v in summary.items(): summary[k] = list(v)

        return export_anns, summary

    def upload_preannotations(self, project_name, preannotations):
        """
        Uploads preannotations to a project in Annotation Lab.
        :param project_name: Project Name
        :type project_name: str
        :param preannotations: preannotation JSON generated by 'generate_preannotations' function
        :type preannotations: List
        :rtype dict
        """

        url = self.__create_url("/api/projects/{}/import".format(project_name))
        print ("Uploading {} preannotation(s).".format(len(preannotations)))

        response_code, content = self.__make_post_request(url, jsn=preannotations, data={})

        return content

    def get_IAA_metrics(self, spark: SparkSession, conll_dir: str, annotator_names: List[str], set_ref_annotator: str = None, return_NerDLMetrics: bool = False,
                        save_dir: str = "results_token_based"):
        """
        Gets IAA metrics for the annotator annotations

        :param spark: Spark session
        :param conll_dir:path to the conll files
        :param annotator_names: list of annotator names
        :param set_ref_annotator: reference annotator name, Default is None. If present, all comparisons made with respect to it.
        :param return_NerDLMetrics: By default return_NerDLMetrics = False. If True, we get the full chunk and partial chunk per token IAA dataframes by using NerDLMetrics. If False, we get the evaluate method for chunk based and classification reports for token based comparisons.
        :param save_dir: path to save token based results, default = "results_token_based"
        """
        global display
        is_module_importable(lib='sklearn',raise_exception=True,pip_name='scikit-learn',message_type='function' )
        from sklearn.metrics import classification_report
        if return_NerDLMetrics:
            if set_ref_annotator is not None:
                ConllDataDict = {}
                iaa_data = {}
                for annotator_name in annotator_names:
                    conllDataRead = CoNLL().readDataset(spark, conll_dir + "/" + annotator_name + ".conll")
                    ConllDataDict[annotator_name] = {"conllData": conllDataRead}

                full_data = ConllDataDict[set_ref_annotator]["conllData"].withColumnRenamed('label',
                                                                                            set_ref_annotator + '_extractions')

                for annotator_name in annotator_names:
                    if annotator_name != set_ref_annotator:
                        full_data = full_data.join(ConllDataDict[annotator_name]["conllData"].withColumnRenamed('label',
                                                                                                                annotator_name + '_extractions'),
                                                ConllDataDict[annotator_name]["conllData"].text ==
                                                ConllDataDict[set_ref_annotator]["conllData"].text)

                evaluation_types = ["partial_chunk_per_token", "full_chunk"]

                for evaluation_mode in evaluation_types:
                    evaler = NerDLMetrics(mode=evaluation_mode)

                    for annotator_name in annotator_names:
                        if annotator_name != set_ref_annotator:
                            iaa_data[annotator_name] = evaler.computeMetricsFromDF(
                                full_data.select(annotator_name + "_extractions", set_ref_annotator + "_extractions"),
                                prediction_col=annotator_name + "_extractions",
                                label_col=set_ref_annotator + "_extractions").cache().toPandas()

                    df_list = []
                    for key, value in iaa_data.items():
                        df = value.set_index('entity')[['total', 'f1']]
                        df.columns = pd.MultiIndex.from_product([[key + " vs " + set_ref_annotator], ['total', 'f1']])
                        df_list.append(df)

                    full_iaa = pd.concat(df_list, axis=1)

                    if evaluation_mode == "full_chunk":

                        full_iaa.to_csv("IAA_" + evaluation_mode + ".csv")
                        print(f"Dataframes written as : IAA_{evaluation_mode}.csv")
                        print("Full_Chunk_iaa_df.head()\n")
                        display(full_iaa.head())
                        print('\n')

                    elif evaluation_mode == "partial_chunk_per_token":
                        full_iaa.to_csv("IAA_" + evaluation_mode + ".csv")
                        print(f"Dataframes written as :  IAA_{evaluation_mode}.csv")
                        print("Partial_Chunk_per_token_iaa_df.head()\n")
                        display(full_iaa.head())
                        print('\n')

            else:
                ConllDataDict = {}
                for annotator_name in annotator_names:
                    conllDataRead = CoNLL().readDataset(spark, conll_dir + "/" + annotator_name + ".conll")
                    ConllDataDict[annotator_name] = {"conllData": conllDataRead}

                evaluation_types = ["partial_chunk_per_token", "full_chunk"]
                for evaluation_mode in evaluation_types:
                    final_processed_df = pd.DataFrame()
                    for i in range(len(annotator_names)):
                        for j in range(i + 1, len(annotator_names)):
                            anno1 = ConllDataDict[annotator_names[i]]["conllData"].withColumnRenamed('label',
                                                                                                    annotator_names[
                                                                                                        i] + '_extractions')
                            anno2 = ConllDataDict[annotator_names[j]]["conllData"].withColumnRenamed('label',
                                                                                                    annotator_names[
                                                                                                        j] + '_extractions')
                            full_data = anno1.join(anno2, anno1.text == anno2.text)
                            evaler = NerDLMetrics(mode=evaluation_mode)
                            annotator_combination_metrics = evaler.computeMetricsFromDF(
                                full_data.select(annotator_names[j] + "_extractions", annotator_names[i] + "_extractions"),
                                prediction_col=annotator_names[j] + "_extractions",
                                label_col=annotator_names[i] + "_extractions").cache().toPandas()
                            annotator_combination_metrics = annotator_combination_metrics.set_index('entity')[
                                ['total', 'f1']]
                            annotator_combination_metrics.columns = pd.MultiIndex.from_product(
                                [[annotator_names[j] + " vs " + annotator_names[i]], ['total', 'f1']])
                            if final_processed_df.empty:
                                final_processed_df = annotator_combination_metrics
                            else:
                                final_processed_df = final_processed_df.join(annotator_combination_metrics, how="outer")
                    final_processed_df.to_csv("Combined_IAA_" + evaluation_mode + ".csv")
                    print(f"Dataframes written as :  Combined_IAA_{evaluation_mode}.csv")
                    print(f"Combined_IAA_{evaluation_mode}.head()\n")
                    display(final_processed_df.head())
                    print('\n')

        else:
            if set_ref_annotator is not None:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                annotator = annotator_names

                for _file_ in os.listdir(conll_dir):
                    conll_path = conll_dir + "/" + _file_
                    for anno_name in annotator:
                        if anno_name in conll_path:
                            conll_df = pd.read_csv(conll_path, sep=" ", engine="python", index_col=0,
                                                skip_blank_lines=False, quoting=3)

                            tmp_df = pd.DataFrame([conll_df.columns.to_list()], columns=['token', 'pos1', 'pos2', 'label'])
                            conll_df.columns = tmp_df.columns
                            conll_df = pd.concat([tmp_df, conll_df]).reset_index(drop=True)
                            conll_df = conll_df.fillna("")

                            ids = []
                            for i, j in conll_df.iterrows():

                                if "-" in j.pos2:
                                    task_id = j.pos2.strip("-")
                                ids.append(task_id)

                            conll_df["task_id"] = ids
                            conll_df.to_csv("tmp.conll", sep=' ', index=False, header=False,
                                            columns=['token', 'pos1', 'pos2', 'label'])

                            conll_df_to_map = conll_df[~conll_df['token'].isin(['', "-DOCSTART-"])][
                                ['task_id']].reset_index()

                            tmp_data = CoNLL().readDataset(spark, "tmp.conll")

                            preds_df = tmp_data.select("sentence", F.explode(
                                F.arrays_zip('token.result', 'token.begin', 'token.end', 'label.result')).alias("cols")) \
                                .select("sentence",
                                        F.expr("cols['0']").alias("token"),
                                        F.expr("cols['1']").alias("begin"),
                                        F.expr("cols['2']").alias("end"),
                                        F.expr("cols['3']").alias(f'{anno_name}_label')).withColumn("sentence", F.explode(
                                tmp_data.sentence.result)).toPandas()

                            assert (preds_df.shape[0] == conll_df_to_map.shape[0])

                            preds_df['task_id'] = conll_df_to_map['task_id']
                            os.remove("tmp.conll")
                            preds_df.to_csv(save_dir + "/" + anno_name + "_token_based_comparison.csv")
                            print(f"Token Comparison File saved as {save_dir}/{anno_name}_token_based_comparison.csv")

                task_dict = {}
                for name in annotator_names:
                    path = f"{save_dir}/{name}_token_based_comparison.csv"
                    df = pd.read_csv(path)
                    task_dict[name] = (set(df['task_id'].values))

                final_tasks = []
                for i in task_dict.values():
                    if len(final_tasks) == 0:

                        final_tasks = list(i)
                    else:
                        final_tasks.extend(list(i))

                final_tasks = (set(final_tasks))

                final_task_info_dict = {}
                for k, v in task_dict.items():
                    diff = final_tasks.difference(v)
                    final_task_info_dict[k] = diff

                base_df = pd.read_csv(save_dir + "/" + set_ref_annotator + '_token_based_comparison.csv')
                a1_a2_df = base_df.copy()
                base_label = set_ref_annotator + "_label"
                comparison_df_dir = save_dir + "/comparison_df/"
                if not os.path.exists(comparison_df_dir):
                    os.mkdir(comparison_df_dir)
                annotator_names.remove(set_ref_annotator)
                for name in annotator_names:
                    df = pd.read_csv(save_dir + "/" + name + '_token_based_comparison.csv')
                    col_name = name + "_label"
                    a1_a2_df[col_name] = df[col_name]
                    a1_a2_df = a1_a2_df[["task_id", "sentence", "token", "begin", "end", base_label, col_name]]

                    a1_a2_df[set_ref_annotator + "_vs_" + name] = a1_a2_df[base_label] == a1_a2_df[col_name]
                    a1_a2_df.to_csv(comparison_df_dir + name + "_" + set_ref_annotator + "__token_df_comparison.csv")

                initialized = False
                for file_ in os.listdir(comparison_df_dir):
                    df = pd.read_csv(comparison_df_dir + file_)

                    name = df.columns[7]
                    if not initialized:
                        result_df = df
                        initialized = True
                    else:

                        result_df[name] = df[name]
                        name = name.split('_')[0]
                        result_df[set_ref_annotator + "_vs_" + name] = df[set_ref_annotator + "_vs_" + name]

                result_df.drop(result_df.filter(regex="Unnamed"), axis=1, inplace=True)

                result_df = result_df.dropna()
                print(f"Final Combined Token comparison result written as csv to {comparison_df_dir}")
                result_df.to_csv(comparison_df_dir + "Final_Combined_Token_Comparison.csv")
                eval_result_df = pd.DataFrame()
                for name in annotator_names:
                    if name != set_ref_annotator:
                        print(f"Conll Evaluate Results for {set_ref_annotator} vs {name}")
                        print("\n")
                        eval_res = ner_log_parser().evaluate(result_df[set_ref_annotator + "_label"].values,
                                                            result_df[name + "_label"].values)
                        print("\n")
                        if not os.path.exists('eval_metric_files'):
                            os.makedirs('eval_metric_files/with_set_ref_annotator/')

                        with open(f'eval_metric_files/with_set_ref_annotator/{name}_vs_{set_ref_annotator}.txt', 'w') as f:
                            for t in eval_res:
                                line = ' '.join(str(x) for x in t)
                                f.write(line + '\n')
                            f.close()

                        entity = []
                        f1 = []

                        with open(f'eval_metric_files/with_set_ref_annotator/{name}_vs_{set_ref_annotator}.txt', 'r') as f:
                            name = f"{name}_vs_{set_ref_annotator}"
                            for line in f.readlines():
                                line = line.replace(") (", ",")
                                line = line.replace("(", "").replace(")", "")
                                line = line.split(",")
                                for i in range(len(line)):
                                    if i == 0 or i % 5 == 0:
                                        if not any(map(str.isdigit, line[i])):
                                            entity.append(line[i])

                                    elif i == 3 or (i % 5) - 3 == 0:

                                        f1.append(line[i])

                        df = pd.DataFrame()
                        df['entity'] = entity
                        df[name + '-F1'] = f1
                        df = df.set_index('entity')

                        if eval_result_df.empty:
                            eval_result_df = df
                        else:

                            eval_result_df = eval_result_df.join(df, how="outer")

                eval_result_df = eval_result_df.T.drop_duplicates().T
                display(eval_result_df)
                print(
                    "Dataframe written as : eval_metric_files/with_set_ref_annotator/Combined_Evaluation_Metrics.csv \n\n")
                eval_result_df.to_csv("eval_metric_files/with_set_ref_annotator/Combined_Evaluation_Metrics.csv")
                token_df = pd.read_csv(comparison_df_dir + "Final_Combined_Token_Comparison.csv")
                final_classification_df = pd.DataFrame()
                for name in annotator_names:
                    if name != set_ref_annotator:
                        classification_res = classification_report(token_df[set_ref_annotator + "_label"].values,
                                                                token_df[name + "_label"].values, output_dict=True)
                        df = pd.DataFrame(classification_res).transpose()
                        df = df[['f1-score']]
                        df = df.rename(columns={"f1-score": set_ref_annotator + "-" + name + "-f1"})
                        if final_classification_df.empty:
                            final_classification_df = df
                        else:
                            final_classification_df = final_classification_df.join(df, how="outer")

                final_classification_df.to_csv(f"classification_report_with_{set_ref_annotator}.csv")
                print(f"Combined Classification Report with ref annotator : {set_ref_annotator} \n")
                display(final_classification_df)
                print(f"DataFrame written as csv: classification_report_with_{set_ref_annotator}.csv\n")
                print("Tasks Not Done by Annotators", final_task_info_dict)

            else:
                if not os.path.exists(save_dir + "/without_set_ref_annotator/"):
                    os.makedirs(save_dir + "/without_set_ref_annotator/")
                save_path = save_dir + "/without_set_ref_annotator/"
                annotator = annotator_names

                for _file_ in os.listdir(conll_dir):
                    conll_path = conll_dir + "/" + _file_
                    for anno_name in annotator:
                        if anno_name in conll_path:
                            conll_df = pd.read_csv(conll_path, sep=" ", engine="python", index_col=0,
                                                skip_blank_lines=False, quoting=3)

                            tmp_df = pd.DataFrame([conll_df.columns.to_list()], columns=['token', 'pos1', 'pos2', 'label'])
                            conll_df.columns = tmp_df.columns
                            conll_df = pd.concat([tmp_df, conll_df]).reset_index(drop=True)
                            conll_df = conll_df.fillna("")

                            ids = []
                            for i, j in conll_df.iterrows():

                                if "-" in j.pos2:
                                    task_id = j.pos2.strip("-")
                                ids.append(task_id)

                            conll_df["task_id"] = ids
                            conll_df.to_csv("tmp.conll", sep=' ', index=False, header=False,
                                            columns=['token', 'pos1', 'pos2', 'label'])

                            conll_df_to_map = conll_df[~conll_df['token'].isin(['', "-DOCSTART-"])][
                                ['task_id']].reset_index()

                            tmp_data = CoNLL().readDataset(spark, "tmp.conll")

                            preds_df = tmp_data.select("sentence", F.explode(
                                F.arrays_zip('token.result', 'token.begin', 'token.end', 'label.result')).alias("cols")) \
                                .select("sentence",
                                        F.expr("cols['0']").alias("token"),
                                        F.expr("cols['1']").alias("begin"),
                                        F.expr("cols['2']").alias("end"),
                                        F.expr("cols['3']").alias(f'{anno_name}_label')).withColumn("sentence", F.explode(
                                tmp_data.sentence.result)).toPandas()

                            assert (preds_df.shape[0] == conll_df_to_map.shape[0])

                            preds_df['task_id'] = conll_df_to_map['task_id']
                            os.remove("tmp.conll")
                            preds_df.to_csv(save_path + anno_name + "_token_based_comparison.csv")
                            print(f"Token Comparison File saved as {save_path}{anno_name}_token_based_comparison.csv")

                task_dict = {}
                for name in annotator_names:
                    path = f"{save_path}{name}_token_based_comparison.csv"
                    df = pd.read_csv(path)
                    task_dict[name] = (set(df['task_id'].values))

                final_tasks = []
                for i in task_dict.values():
                    if len(final_tasks) == 0:

                        final_tasks = list(i)
                    else:
                        final_tasks.extend(list(i))

                final_tasks = (set(final_tasks))

                final_task_info_dict = {}
                for k, v in task_dict.items():
                    diff = final_tasks.difference(v)
                    final_task_info_dict[k] = diff

                for i in range(len(annotator_names)):
                    for j in range(i + 1, len(annotator_names)):
                        anno1 = annotator_names[i]
                        anno2 = annotator_names[j]
                        base_df = pd.read_csv(save_path + anno1 + '_token_based_comparison.csv')
                        a1_a2_df = base_df.copy()
                        base_label = anno1 + "_label"
                        comparison_df_dir = save_path + "/comparison_df/"
                        if not os.path.exists(comparison_df_dir):
                            os.mkdir(comparison_df_dir)
                        df = pd.read_csv(save_path + anno2 + '_token_based_comparison.csv')
                        col_name = anno2 + "_label"
                        a1_a2_df[col_name] = df[col_name]
                        a1_a2_df = a1_a2_df[["task_id", "sentence", "token", "begin", "end", base_label, col_name]]
                        a1_a2_df[anno1 + "_vs_" + anno2] = a1_a2_df[base_label] == a1_a2_df[col_name]
                        a1_a2_df.to_csv(comparison_df_dir + anno2 + "_" + anno1 + "__token_df_comparison.csv")

                result_df = pd.DataFrame()
                for i in range(len(annotator_names)):
                    for j in range(i + 1, len(annotator_names)):
                        anno1 = annotator_names[i]
                        anno2 = annotator_names[j]
                        for file_ in os.listdir(comparison_df_dir):
                            if anno1 in file_ and anno2 in file_:
                                df = pd.read_csv(comparison_df_dir + file_)

                                if result_df.empty:
                                    result_df = df
                                else:
                                    result_df[anno1 + "_label"] = df[anno1 + "_label"]
                                    result_df[anno2 + "_label"] = df[anno2 + "_label"]
                                    result_df[anno1 + "_vs_" + anno2] = df[anno1 + "_vs_" + anno2]

                result_df.drop(result_df.filter(regex="Unnamed"), axis=1, inplace=True)

                result_df = result_df.dropna()
                print(f"Final Combined Token comparison result written as csv to {comparison_df_dir}")
                from IPython.display import display
                display(result_df)
                result_df.to_csv(comparison_df_dir + "Final_Combined_Token_Comparison.csv")
                for i in range(len(annotator_names)):
                    for j in range(i + 1, len(annotator_names)):
                        anno1 = annotator_names[i]
                        anno2 = annotator_names[j]
                        if not os.path.exists('eval_metric_files/without_set_ref_annotator/'):
                            os.makedirs('eval_metric_files/without_set_ref_annotator/')

                        print(f"Conll Evaluate Results for {anno1} vs {anno2}")
                        print("\n")

                        eval_res = ner_log_parser().evaluate(result_df[anno1 + "_label"].values,
                                                            result_df[anno2 + "_label"].values)
                        print("\n")
                        with open(f'eval_metric_files/without_set_ref_annotator/{anno1}_vs_{anno2}.txt', 'w') as f:
                            for t in eval_res:
                                line = ' '.join(str(x) for x in t)
                                f.write(line + '\n')
                            f.close()
                eval_result_df = pd.DataFrame()
                for file_ in os.listdir("eval_metric_files/without_set_ref_annotator/"):
                    if file_.endswith('.txt'):
                        entity = []
                        f1 = []
                        with open("/content/eval_metric_files/without_set_ref_annotator/" + file_, 'r') as f:
                            name = file_.split('.')[0]
                            for line in f.readlines():
                                line = line.replace(") (", ",")
                                line = line.replace("(", "").replace(")", "")
                                line = line.split(",")
                                for i in range(len(line)):
                                    if i == 0 or i % 5 == 0:
                                        if not any(map(str.isdigit, line[i])):
                                            entity.append(line[i])

                                    elif i == 3 or (i % 5) - 3 == 0:
                                        f1.append(line[i])

                        df = pd.DataFrame()
                        df['entity'] = entity
                        df[name + '-F1'] = f1
                        df = df.set_index('entity')

                        if eval_result_df.empty:
                            eval_result_df = df
                        else:
                            eval_result_df = eval_result_df.join(df, how="outer")

                print("Dataframe written as : eval_metric_files/without_set_ref_annotator/Combined_Evaluation_Metrics.csv")
                eval_result_df.to_csv("eval_metric_files/without_set_ref_annotator/Combined_Evaluation_Metrics.csv")
                display(eval_result_df.head())
                print("\n\n")

                token_df = pd.read_csv(comparison_df_dir + "Final_Combined_Token_Comparison.csv")
                final_classification_df = pd.DataFrame()
                for i in range(len(annotator_names)):
                    for j in range(i + 1, len(annotator_names)):
                        anno1 = annotator_names[i]
                        anno2 = annotator_names[j]
                        classification_res = classification_report(token_df[anno1 + "_label"].values,
                                                                token_df[anno2 + "_label"].values, output_dict=True)
                        df = pd.DataFrame(classification_res).transpose()
                        df = df[['f1-score']]
                        df = df.rename(columns={"f1-score": anno1 + "-" + anno2 + "-f1"})
                        if final_classification_df.empty:
                            final_classification_df = df
                        else:
                            final_classification_df = final_classification_df.join(df, how="outer")

                final_classification_df.to_csv("classification_report.csv")
                print(f"Combined Classification Report with no ref annotator : \n")
                display(final_classification_df)
                print(f"DataFrame written as csv: classification_report.csv \n")
                print("Tasks Not Done by Annotators", final_task_info_dict)



