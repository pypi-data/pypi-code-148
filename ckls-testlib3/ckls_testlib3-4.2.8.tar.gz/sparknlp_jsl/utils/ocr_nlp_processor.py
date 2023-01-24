from sparknlp_jsl.utils.ocr_utils import __ocr_pipeline, __colored_box, __highlighted_box, __black_box
from pyspark.sql import SparkSession
from typing import Optional, List, IO
from pyspark.ml import PipelineModel

colors = ['aqua', 'aquamarine', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
          'chartreuse', 'chocolate', 'cornflowerblue', 'crimson', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray',
          'darkgreen', 'darkkhaki', 'darkmagenta',
          'darkolivegreen', 'darkorange', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray',
          'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'fuchsia', 'firebrick',
          'gold', 'goldenrod', 'green', 'greenyellow', 'hotpink',
          'indianred', 'indigo', 'indianred', 'khaki', 'lightblue', 'lightcoral', 'lightgoldenrodyellow', 'lightgreen',
          'lightgray', 'lightgrey', 'lightpink', 'limegreen', 'lightsalmon', 'magenta', 'mediumblue', 'mediumorchid',
          'mediumpurple', 'mediumspringgreen', 'mediumseagreen', 'mediumvioletred',
          'midnightblue', 'navy', 'olive', 'orange', 'orangered', 'peru', 'pink', 'purple', 'rebeccapurple', 'red',
          'rosybrown', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'sienna', 'violet', 'tan', 'tomato',
          'thistle',
          'yellow', 'yellowgreen']


def ocr_entity_processor(spark: SparkSession, file_path: str, ner_pipeline: PipelineModel, style: str = "bounding_box",
                         save_dir: str = "save_folder", label: bool = False,
                         label_color: str = "red", color_chart_path: str = "color_chart.png",
                         chunk_col: str = "ner_chunk",
                         black_list: Optional[List[str]] = [], display_result: bool = False) -> IO:

    """Generates an annotated PDF file using input PDF files
        :param spark: Spark session with spark-nlp-jsl and spark-ocr jar
        :type spark: SparkSession

        :param file_path: Path to PDF files
        :type file_path: str

        :param ner_pipeline: Fitted NER pipeline
        :type ner_pipeline: PipelineModel

        :param chunk_col: OutputCol name of the chunk in ner pipeline that will be annotated, default 'ner_chunk'
        :type chunk_col: str

        :param black_list: List of NER labels that will be painted over in 'highlight' and 'bounding_box' styles
        :type black_list: list

        :param style:  PDF file process style that has 3 options; 'black_band': Black bands over the chunks detected
        by NER pipeline. 'bounding_box': Colorful bounding boxes around the chunks detected by NER pipeline. Each
        color represents a different NER label. 'highlight': Colorful highlights over the chunks detected by NER
        pipeline. Each color represents a different NER label. :type style: str

        :param save_dir: Path for saving folder of processed PDF files, defaults to 'save_folder'
        :type save_dir: str

        :param label: Set to True to write NER labels over the chunks, defaults to False
        :type label: bool

        :param label_color: Color of NER labels if 'label=True' , defaults to "red"
        :type label_color: str

        :param color_chart_path: File name of color chart in PNG format that shows the colors of NER labels in the
        processed file, defaults to "color_chart.png" :type color_chart_path: str

        :param display_result: Set to True to see the output of processed file, defaults to False
        :type display_result: bool

        :return: PDF file
        :rtype: IO
    """

    global colors

    results = __ocr_pipeline(spark, file_path, ner_pipeline)

    for i in results.select('path').distinct().collect():
        result = results[results.path == i.path]
        file_name = i.path.split("/")[-1].split(".")[0]

        if style == "bounding_box":
            if label and label_color not in colors:
                raise Exception(f"{label_color} is not a valid color. Please pick one:{colors}")
            else:
                __colored_box(result, file_name, style, chunk_col, black_list, save_dir, label, label_color,
                              color_chart_path, display_result)

        elif style == "highlight":
            if label and label_color not in colors:
                raise Exception(f"{label_color} is not a valid color. Please pick one:{colors}")
            else:
                __highlighted_box(result, file_name, style, chunk_col, black_list, save_dir, label,
                                  label_color,
                                  color_chart_path, display_result)

        elif style == "black_band":
            if label and label_color not in colors:
                raise Exception(f"{label_color} is not a valid color. Please pick one:{colors}")
            else:
                __black_box(result, file_name, style, chunk_col, save_dir, label, label_color, display_result)

        else:
            raise Exception(style,
                            "is not a valid option. Please try one: ['bounding_box', 'highlight', 'black_band']")
