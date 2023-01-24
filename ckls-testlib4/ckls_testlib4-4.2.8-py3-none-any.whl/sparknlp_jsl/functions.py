from pyspark import SparkContext
from pyspark.sql.column import Column, _to_java_column


def profile(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApply(_to_java_column(code_array), _to_java_column(age),
                                                           _to_java_column(sex), _to_java_column(elig),
                                                           _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV24Y17(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV24Y17(_to_java_column(code_array), _to_java_column(age),
                                                              _to_java_column(sex), _to_java_column(elig),
                                                              _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV24Y18(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV24Y18(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV24Y19(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV24Y19(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV24Y20(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV24Y20(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV24Y21(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV24Y21(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV24Y22(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV24Y22(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV23Y18(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV23Y18(_to_java_column(code_array), _to_java_column(age),
                                                              _to_java_column(sex), _to_java_column(elig),
                                                              _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV23Y19(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV23Y19(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV23(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV23(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22Y17(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22Y17(_to_java_column(code_array), _to_java_column(age),
                                                              _to_java_column(sex), _to_java_column(elig),
                                                              _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22Y18(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22Y18(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22Y19(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22Y19(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22Y20(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22Y20(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22Y21(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22Y21(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22Y22(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22Y22(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)

def profileV22(code_array, age, sex, elig="CNA", orec="0", medicaid=False):
    sc = SparkContext._active_spark_context
    jc = sc._jvm.com.johnsnowlabs.nlp.jsl.HCC.profileApplyV22(_to_java_column(code_array), _to_java_column(age),
                                                                 _to_java_column(sex), _to_java_column(elig),
                                                                 _to_java_column(orec), _to_java_column(medicaid))
    return Column(jc)
