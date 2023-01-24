from debater_python_api.api.clients.key_point_analysis.KpAnalysisUtils import KpAnalysisUtils
from debater_python_api.api.clients.key_point_analysis.KpaResult import KpaResult

if __name__ == '__main__':
    file = '/Users/yoavkantor/Downloads/2022_11 (Nov) Survey - New hierarchy-selected/06-ISC_NPS_Survey_4Q22_NewHierarchy_kpa_result_all_columns.csv'
    kpa_result = KpaResult.create_from_result_csv(file)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result, result_filename=file.replace('.csv', '_0_4.csv'), filter_min_relations_for_text=0.4)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result, result_filename=file.replace('.csv', '_0_45.csv'), filter_min_relations_for_text=0.45)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result, result_filename=file.replace('.csv', '_0_5.csv'), filter_min_relations_for_text=0.5)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result, result_filename=file.replace('.csv', '_0_55.csv'), filter_min_relations_for_text=0.55)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result, result_filename=file.replace('.csv', '_0_60.csv'), filter_min_relations_for_text=0.6)



    file = '/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/final/v0_multi_kps_sbert_stage2_15/test/eng_kp_input_2022_simplified_multi_kps_con_kpa_results.csv'
    kpa_result = KpaResult.create_from_result_csv(file)

    result_file = file.replace('.csv', '_new1.csv')
    kpa_result.write_to_file(result_file)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result, result_filename=result_file)

    kpa_result2 = KpaResult.create_from_result_json(kpa_result.result_json)
    result_file = file.replace('.csv', '_new2.csv')
    kpa_result2.write_to_file(result_file)
    KpAnalysisUtils.generate_graphs_and_textual_summary_kpa_result(kpa_result2, result_filename=result_file)

    file = file.replace('.csv', '_new3.csv')
    kpa_result.write_to_file(file)
    KpAnalysisUtils.generate_graphs_and_textual_summary(file)