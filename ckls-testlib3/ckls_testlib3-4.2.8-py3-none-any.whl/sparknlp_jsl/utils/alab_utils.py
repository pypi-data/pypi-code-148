"""Util functions for alab module
"""
import json
import re
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from sparknlp.annotator import Tokenizer, RegexTokenizer, SentenceDetectorDLModel, PerceptronModel
from sparknlp.base import Pipeline, DocumentAssembler, LightPipeline
from pyspark.sql import DataFrame as SparkDataFrame
from sparknlp_jsl.utils.imports import is_module_importable

nlp_token_pipeline: LightPipeline = None
nlp_pos_pipeline: LightPipeline = None
token_pipeline_initialized = False
pos_pipeline_initialized = False

document_assembler: DocumentAssembler = None
sentence_detector: SentenceDetectorDLModel = None
regular_tokenizer: Tokenizer = None
regex_tokenizer: RegexTokenizer = None
empty_df: SparkDataFrame = None
pos: PerceptronModel = None


def get_doc_assembler() -> DocumentAssembler:
    global document_assembler
    if not document_assembler:
        document_assembler = DocumentAssembler().setInputCol("text").setOutputCol("document")
    return document_assembler


def get_sent_detector() -> SentenceDetectorDLModel:
    global sentence_detector
    if not sentence_detector:
        sentence_detector = SentenceDetectorDLModel.pretrained("sentence_detector_dl_healthcare", "en",
                                                               "clinical/models") \
            .setInputCols(["document"]) \
            .setOutputCol("sentence")
    return sentence_detector


def get_regular_tokenizer() -> Tokenizer:
    global regular_tokenizer
    if not regular_tokenizer:
        regular_tokenizer = Tokenizer().setInputCols(["sentence"]).setOutputCol("token")
    return regular_tokenizer


def get_regex_tokenizer(regex_pattern) -> RegexTokenizer:
    global regex_tokenizer
    if not regex_tokenizer:
        regex_tokenizer = RegexTokenizer() \
            .setInputCols(["sentence"]) \
            .setOutputCol("token") \
            .setPositionalMask(True) \
            .setPattern(regex_pattern)
    return regex_tokenizer


def get_pos() -> PerceptronModel:
    global pos
    if not pos:
        pos = PerceptronModel.pretrained("pos_clinical", "en", "clinical/models") \
            .setInputCols(["sentence", "token"]) \
            .setOutputCol("pos")
    return pos


def get_empty_df(spark) -> SparkDataFrame:
    global empty_df
    if not empty_df:
        empty_df = spark.createDataFrame([[""]]).toDF("text")
    return empty_df


def get_nlp_token_pipeline(spark, regex_pattern):
    """Generates a LightPipeline with a document assembler, sentence detector and regular tokenizer
    :param spark: Spark session with spark-nlp-jsl jar
    :type spark: SparkSession
    :param regex_pattern: set a pattern to use regex tokenizer, defaults to regular tokenizer if pattern not defined
    :type regex_pattern: str
    :return: LightPipeline with a document assembler, sentence detector and a regular or regex tokenizer depending on regex_pattern
    :rtype: LightPipeline
    """
    global token_pipeline_initialized
    global nlp_token_pipeline

    if not token_pipeline_initialized:

        if regex_pattern is None:
            tokenizer = get_regular_tokenizer()

        else:
            tokenizer = get_regex_tokenizer(regex_pattern)

        pipeline = Pipeline(
            stages=[
                get_doc_assembler(),
                get_sent_detector(),
                tokenizer]
        )

        empty_data = get_empty_df(spark)

        pipeline_fit = pipeline.fit(empty_data)

        nlp_token_pipeline = LightPipeline(pipeline_fit)

        print("Spark NLP Token LightPipeline is created")

        token_pipeline_initialized = True

        return nlp_token_pipeline

    else:
        return nlp_token_pipeline


def get_sentence_pipeline(spark):
    """Generates a LightPipeline with a document assembler and sentence detector
        :param spark: Spark session with spark-nlp-jsl jar
        :type spark: SparkSession
        :return: LightPipeline with a document assembler and sentence detector
        :rtype: LightPipeline
        """

    pipeline = Pipeline(
        stages=[
            get_doc_assembler(),
            get_sent_detector()]
    )

    empty_data = get_empty_df(spark)

    pipeline_fit = pipeline.fit(empty_data)

    return pipeline_fit


def get_rel_df(input_json_path, ground_truth=False):
    """Generate dataframe for all annotated relations from an Annotation Lab JSON export
    :param input_json_path: path to Annotation Lab JSON export
    :type input_json_path: str
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :return: dataframe with all annotated relations
    :rtype: pd.DataFrame
    """
    is_module_importable('pandas',True,'pandas' )
    import pandas as pd
    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        ann_results = json.load(json_file)

    rels = []
    for _, ann_result in enumerate(ann_results):
        task_id = ann_result["id"]
        try:
            task_title = ann_result['data']['title']
        except:
            task_title = f"Task ID# {task_id}"
        task_title_print = f"Task ID# {task_id}"
        try:
            if ground_truth:
                for ind in range(len(ann_result['completions'])):
                    if ann_result['completions'][ind]['honeypot']:
                        ground_truth_index = ind
                rels.extend([(d['from_id'], d['to_id'], d.get('labels', []), task_id) for d in
                             ann_result['completions'][ground_truth_index]['result'] if d['type']
                             not in ['labels', 'choices', 'textarea']])
                print('Successfully processed relations for task:', task_title_print)

            elif ground_truth is False or ground_truth is None:
                rels.extend([(d['from_id'], d['to_id'], d.get('labels', []), task_id) for d in
                             ann_result['completions'][-1]['result'] if
                             d['type'] not in ['labels', 'choices', 'textarea']])
                print('Successfully processed relations for task:', task_title_print)

        except:
            print('EXCEPTION: could not process relations for', task_title_print)

    print('Total tasks processed:', len(ann_results), '\nTotal annotated relations processed:', len(rels))

    rel_df = pd.DataFrame(rels, columns=['from_id', 'to_id', 'relation', 'task_id'])
    rel_df['relation'] = rel_df['relation'].apply(lambda x: x[0] if len(x) > 0 else 'relation')
    rel_df['json'] = input_json_path
    rel_df = rel_df.reset_index(drop=True)
    return rel_df


def get_ner_df(input_json_path, ground_truth=False, assertion_labels=None):
    """Generates dataframe for all annotated entities from an Annotation Lab JSON export
    :param input_json_path: path to Annotation Lab JSON export
    :type input_json_path: str
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :param assertion_labels: all assertion labels that were annotated, defaults to None
    :type assertion_labels: list
    :return: dataframe with all annotated entities
    :rtype: pd.DataFrame
    """
    is_module_importable('pandas',True,'pandas' )
    import pandas as pd

    if assertion_labels is None:
        assertion_labels = []

    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        ann_results = json.load(json_file)

    ner_list = []
    for _, ann_result in enumerate(ann_results):
        task_id = ann_result["id"]
        try:
            task_title = ann_result['data']['title']
        except:
            task_title = f"Task ID# {task_id}"
        task_title_print = f"Task ID# {task_id}"
        try:
            if ground_truth:
                for x in range(len(ann_result['completions'])):
                    if ann_result['completions'][x]['honeypot']:
                        ground_truth_index = x
                for ner in ann_result['completions'][ground_truth_index]['result']:
                    if ner["type"] == "labels" and ner["value"]['labels'][0] not in assertion_labels:
                        ner_tuples = ((ner['id'], ner["value"]['start'], ner["value"]['end'],
                                       ner["value"]['text'], ner["value"]['labels'][0],
                                       task_id, task_title))
                        ner_list.append(ner_tuples)
                print('Successfully processed NER labels for:', task_title_print)

            elif ground_truth is False or ground_truth is None:
                for ner in ann_result['completions'][-1]['result']:
                    if ner["type"] == "labels" and ner["value"]['labels'][0] not in assertion_labels:
                        ner_tuples = ((ner['id'], ner["value"]['start'], ner["value"]['end'],
                                       ner["value"]['text'], ner["value"]['labels'][0],
                                       task_id, task_title))
                        ner_list.append(ner_tuples)
                print('Successfully processed NER labels for:', task_title_print)

        except:
            print('EXCEPTION: could not process NER labels for', task_title)

    ner_df = pd.DataFrame(ner_list, columns=['chunk_id', "start", "end", 'text', 'ner_label', "task_id", 'title'])
    if len(ner_list) > 0:
        print('Total tasks processed:', len(ann_results), '\nTotal annotated NER labels processed:', len(ner_list))

    ner_df['json'] = input_json_path
    ner_df = ner_df.reset_index(drop=True)
    return ner_df


def get_ner_sentence_borders(spark, input_json_path, ground_truth=False, assertion_labels=None):
    """Get sentence borders for each task
    :param spark: Spark session with spark-nlp-jsl jar
    :type spark: SparkSession
    :param input_json_path: path to Annotation Lab JSON export
    :type input_json_path: str
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :param assertion_labels: all assertion labels that were annotated, defaults to None
    :type assertion_labels: list
    :return: dataframe with tasks split into sentences including start and end indexes
    :rtype: pd.DataFrame
    """
    is_module_importable('pandas',True,'pandas' )
    import pandas as pd

    if assertion_labels is None:
        assertion_labels = []

    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        ann_results = json.load(json_file)

    task_sent_df = []
    for _, ann_result in enumerate(ann_results):
        task_sent_df.append([ann_result["id"], ann_result['data']['text']])

    c_schema = StructType([StructField("task_id", IntegerType()), StructField("text", StringType())])

    task_sent_spark_df = spark.createDataFrame(task_sent_df, schema=c_schema)

    df = get_sentence_pipeline(spark=spark).transform(task_sent_spark_df)

    sentence_df = df.select("task_id", F.explode(
        F.arrays_zip(df.sentence.begin, df.sentence.end, df.sentence.result, df.sentence.metadata)).alias("cols")) \
        .select("task_id",
                F.expr("cols['0']").alias("start"),
                F.expr("cols['1']").alias("end"),
                F.expr("cols['2']").alias("sentence"),
                F.expr("cols['3']['sentence']").alias("sentence_id")).toPandas()
    sentence_df = sentence_df.sort_values('task_id')

    ner_borders_dicts = []
    project_df = get_ner_df(input_json_path=input_json_path, ground_truth=ground_truth,
                            assertion_labels=assertion_labels)
    for _, task in enumerate(project_df.task_id.unique()):
        task_df = project_df[project_df.task_id == task].reset_index(drop=True)
        task_start = task_df.start.min()
        task_end = task_df.end.max()
        task_sentences_df = sentence_df[(sentence_df.task_id == task) &
                                        (sentence_df.end >= task_start) &
                                        (sentence_df.start <= task_end)]

        for _, row in task_df.iterrows():
            try:
                ner_sentence_borders = task_sentences_df[(task_sentences_df.start <= row['start']) &
                                                         (task_sentences_df.end >= row['end'] - 1)]
                ner_sentence_start = ner_sentence_borders['start'].values[0]
                ner_sentence_end = ner_sentence_borders['end'].values[0]
                ner_sentence_id = ner_sentence_borders['sentence_id'].values[0]
                ner_sentence_text = ner_sentence_borders['sentence'].values[0]
                ner_sentence_task_id = ner_sentence_borders['task_id'].values[0]

                ner_dict = dict(row)
                ner_dict['ner_sentence_start_border'] = ner_sentence_start
                ner_dict['ner_sentence_end_border'] = ner_sentence_end
                ner_dict['ner_sentence_id'] = ner_sentence_id
                ner_dict['ner_sentence'] = ner_sentence_text
                ner_dict['task_id'] = ner_sentence_task_id
                ner_borders_dicts.append(ner_dict)
            except:
                ner_sentence_borders = task_sentences_df[((task_sentences_df.start <= row['start']) &
                                                          (task_sentences_df.end >= row['start'])) |
                                                         ((task_sentences_df.start <= row['end']) &
                                                          (task_sentences_df.end >= row['end']))]
                ner_sentence_start = ner_sentence_borders['start'].min()
                ner_sentence_end = ner_sentence_borders['end'].max()
                ner_sentence_id = '_'.join(ner_sentence_borders['sentence_id'].values)
                ner_sentence_text = ' '.join(ner_sentence_borders['sentence'].values)
                ner_sentence_task_id = ner_sentence_borders['task_id'].values[0]

                ner_dict = dict(row)
                ner_dict['ner_sentence_start_border'] = ner_sentence_start
                ner_dict['ner_sentence_end_border'] = ner_sentence_end
                ner_dict['ner_sentence_id'] = ner_sentence_id
                ner_dict['ner_sentence'] = ner_sentence_text
                ner_dict['task_id'] = ner_sentence_task_id
                ner_borders_dicts.append(ner_dict)
                print('EXCEPTION:\n\n', ner_dict)
                continue

    ner_borders_df = pd.DataFrame(ner_borders_dicts)
    ner_borders_df['sentence_begin'] = ner_borders_df.apply(
        lambda begin_row: begin_row['start'] - begin_row['ner_sentence_start_border'], axis=1)
    ner_borders_df['sentence_end'] = ner_borders_df.apply(lambda end_row: end_row['sentence_begin'] +
                                                                          len(end_row['text']), axis=1)
    return ner_borders_df


def get_nlp_pos_pipeline(spark, regex_pattern):
    """Generates a LightPipeline with a document assembler, sentence detector, regular tokenizer and POS-tagger
    :param spark: Spark session with spark-nlp-jsl jar
    :type spark: SparkSession
    :param regex_pattern: set a pattern to use regex tokenizer, defaults to regular tokenizer if pattern not defined
    :type regex_pattern: str
    :return: LightPipeline with a document assembler, sentence detector, regular or regex tokenizer depending on regex_pattern and POS-tagger
    :rtype: LightPipeline
    """
    global pos_pipeline_initialized
    global nlp_pos_pipeline

    if not pos_pipeline_initialized:
        if regex_pattern is None:
            tokenizer = get_regular_tokenizer()

        else:
            tokenizer = get_regex_tokenizer(regex_pattern)

        pipeline = Pipeline(
            stages=[
                get_doc_assembler(),
                get_sent_detector(),
                tokenizer,
                get_pos()]
        )

        empty_data = get_empty_df(spark)

        pipeline_fit = pipeline.fit(empty_data)

        nlp_pos_pipeline = LightPipeline(pipeline_fit)

        pos_pipeline_initialized = True

        print("Spark NLP POS LightPipeline is created")

        return nlp_pos_pipeline

    else:
        return nlp_pos_pipeline


def get_single_task_conll(output, pos_pipeline, token_pipeline, ground_truth=False, excluded_labels=None,
                          excluded_task_ids=None, excluded_task_titles=None):
    """Generates CoNLL-style outputs from a single task in an Annotation Lab JSON export
    :param output: enumerated items from an Annotation Lab JSON export
    :type output: dict
    :param pos_pipeline: LightPipeline with a document assembler, sentence detector, tokenizer and POS-tagger
    :type pos_pipeline: LightPipeline
    :param token_pipeline: LightPipeline with a document assembler, sentence detector and tokenizer
    :type token_pipeline: LightPipeline
    :param ground_truth: set to True to select ground truth completions, False to select latest completions,
    defaults to False
    :type ground_truth: bool
    :param excluded_labels: labels to exclude from CoNLL; these are all assertion labels and irrelevant NER labels,
    defaults to None
    :type excluded_labels: list
    :param excluded_task_ids: list of Annotation Lab task IDs to exclude from CoNLL, defaults to None
    :type excluded_task_ids: list
    :param excluded_task_titles: Annotation Lab task titles to exclude from CoNLL, defaults to None
    :type excluded_task_titles: list
    :return: CoNLL lines
    :rtype: list
    """
    is_module_importable('pandas',True,'pandas' )
    import pandas as pd

    if excluded_labels is None:
        excluded_labels = []
    else:
        excluded_labels = ["B-" + i for i in excluded_labels] + ["I-" + i for i in excluded_labels] + excluded_labels

    if excluded_task_titles is None:
        excluded_task_titles = []

    if excluded_task_ids is None:
        excluded_task_ids = []

    conll_lines = [f"-DOCSTART- -X- -{output['id']}- O\n\n"]

    lp_pipeline = pos_pipeline
    token_lp_pipeline = token_pipeline

    try:
        new_content = output['data']['text']
    except:
        new_content = output['data']['longText']

    try:
        title = output['data']['title']
    except:
        title = "untitled"

    print_title = "Task ID# " + str(output['id'])

    print(f'Attempting to process: {print_title}')

    n = lp_pipeline.fullAnnotate(new_content)

    sent_tuples = {str(x.metadata['sentence']): (x.begin, x.end) for x in n[0]['sentence']}
    parsed = [(int(x.metadata['sentence']), x.result, x.begin, x.end, y.result, sent_tuples[x.metadata['sentence']][0])
              for x, y in zip(n[0]["token"], n[0]["pos"])]

    entities = []
    if len(output['completions']) > 0 and title.strip() not in excluded_task_titles \
            and output['id'] not in excluded_task_ids:
        print(f'{print_title} is included')

        honeypot = False       
        if ground_truth:
            for completion in output['completions']:          
                if completion['honeypot']:
                    ann_results = completion['result']
                    honeypot=True
                    
                elif honeypot==False:
                    ann_results = output['completions'][-1]['result']             

        elif ground_truth is False or ground_truth is None:
            ann_results = output['completions'][-1]['result']

        for d in ann_results:
            if d['type'] == 'labels' and d['value']['labels'][0].replace(' ', '') not in excluded_labels:
                temp_text = d['value']['text']
                start = d['value']['start']
                end = d['value']['end']

                if len(temp_text) != len(temp_text.rstrip()):
                    end = end - (len(temp_text) - len(temp_text.rstrip()))
                    temp_text = temp_text.rstrip()

                if len(temp_text) != len(temp_text.lstrip()):
                    start = start + (len(temp_text) - len(temp_text.lstrip()))
                    temp_text = temp_text.lstrip()

                entities.append((temp_text, d['value']['labels'][0].replace(' ', ''), start, end))

        text_df = pd.DataFrame(entities, columns=['chunk', 'label', 'start', 'end'])

        text_df['label'] = text_df['label'].apply(lambda x: x.replace(' ', ''))

        text_df.sort_values(by=['start', 'end'], inplace=True)
        text_df.reset_index(drop=True, inplace=True)

        df = text_df.copy()

        tag_dict = {}

        for _, row in df.iterrows():
            base_ix = row["start"]
            chunk_tokens = token_lp_pipeline.fullAnnotate(row['chunk'])[0]['token']

            for c, token in enumerate(chunk_tokens):
                if c == 0:
                    iob = 'B-'
                else:
                    iob = 'I-'
                tag_dict[(base_ix + token.begin, token.result)] = iob + row['label'].replace(' ', '')

        s = 0
        for _, p in enumerate(parsed):
            if p[0] != s:
                conll_lines.append("\n")
                s += 1
            conll_lines.append("{} {} {} {}\n".format(p[1], p[4], p[4], tag_dict.get((p[2] + p[-1], p[1]), "O")))

        conll_lines.append("\n")

        return conll_lines

    else:
        print(f'{print_title} is excluded')
        return ''

def get_token_df(text):
    """
    Args:
        text (str): input text

    Returns:
        _type_: Pandas DataFrame with columns ('token', 'begin', 'end')
    """
    is_module_importable('pandas',True,'pandas' )
    import pandas as pd

    try:
        tokens, borders = zip(*[(m.group(0), (m.start(), m.end()-1)) for m in re.finditer(r'\S+', text)])
        tuples = [(x, y[0], y[1]) for x,y in zip(tokens, borders)]
    except:
        tuples = [('-',0,0)]
    df = pd.DataFrame(tuples, columns=['token','begin','end'])
    return df