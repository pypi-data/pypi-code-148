from keras.models import load_model
from proquo.model.relation.RelationVectorizerLstm import RelationVectorizerLstm


def test(test_file_path, vocab_file_path, model_file_path):
    examples = []
    gold_preds = []

    with open(test_file_path, 'r', encoding='utf-8') as input_file:
        for line in input_file:

            if not line.strip():
                continue

            parts = line.split('\t')

            if len(parts) == 2:
                examples.append(parts[0])
                gold_preds.append(int(parts[1]))

    vectorizer = RelationVectorizerLstm.from_vocab_file(vocab_file_path, 300, True)
    test_data = vectorizer.vectorize(examples)
    # TODO: fix loading
    model = load_model(model_file_path)
    preds = list(model.predict(test_data, verbose=1).ravel())

    tp_cnt = 0
    fp_cnt = 0
    tn_cnt = 0
    fn_cnt = 0

    for example, pred, gold_pred in zip(examples, preds, gold_preds):

        if pred >= 0.3:
            if gold_pred == 1:
                tp_cnt += 1
            else:
                fp_cnt += 1
                print(f'FP: {example}, {pred}')
        else:
            if gold_pred == 0:
                tn_cnt += 1
            else:
                fn_cnt += 1
                print(f'FN: {example}, {pred}')

    precision = tp_cnt / (tp_cnt + fp_cnt)
    recall = tp_cnt / (tp_cnt + fn_cnt)

    f_score = 0
    if precision + recall > 0:
        f_score = (2 * precision * recall) / (precision + recall)

    print(f'TP: {tp_cnt}, FP: {fp_cnt}, TN: {tn_cnt}, FN: {fn_cnt}, Precision: {precision}, Recall: {recall},'
          f' F-Score: {f_score}')
