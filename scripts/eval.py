import sys
import re
import numpy as np

label_dict = {'audit': 0, 'authenticate': 1, 'heartbeat': 2,
              'pooling': 3, 'scheduler': 4, 'unrelated': 5}

confusion_matrix = np.zeros(shape=(len(label_dict), len(label_dict)))


def calculate_precisions(confusion_matrix):
    column_val = np.sum(confusion_matrix, axis=0)
    for i in range(len(confusion_matrix)):
        if not column_val[i] == 0:
            column_val[i] = confusion_matrix[i, i] / column_val[i]
    return column_val


def calculate_recalls(confusion_matrix):
    row_val = np.sum(confusion_matrix, axis=1)
    for i in range(len(confusion_matrix)):
        if not row_val[i] == 0:
            row_val[i] = confusion_matrix[i, i] / row_val[i]
    return row_val


def calculate_accuracy(confusion_matrix):
    matrix_sum = confusion_matrix.sum()
    true_sum = confusion_matrix.diagonal().sum()
    accuracy = true_sum / matrix_sum
    return accuracy


def process(line, answers):
    if re.match('(^\d{4}-|^#).*', line):
        return
    file, prediction = line.split(' -> ')
    file = file.strip()
    prediction = prediction.strip()
    idx_prediction = label_dict[prediction]

    gold_answers = get_gold_answers(file, answers)
    if prediction in gold_answers:
        confusion_matrix[idx_prediction][idx_prediction] += 1
    else:
        for gold_answer in gold_answers:
            idx_gold = label_dict[gold_answer]
            confusion_matrix[idx_gold][idx_prediction] += 1


def get_gold_answers(filename, answers):
    gold_answers = list()
    for tactic in answers.keys():
        if check_list_for_name(filename, answers[tactic]):
            gold_answers.append(tactic)
    if not gold_answers:
        gold_answers = ['unrelated']
    return gold_answers


def check_list_for_name(filename, tactic_list):
    for name in tactic_list:
        if name == filename:
            return True
    return False


def process_file(infile, answers):
    with open(infile, 'r') as inp:
        for line in inp.readlines():
            res = process(line, answers)

    printResults(confusion_matrix)


def printResults(confusion_matrix):
    precisions = calculate_precisions(confusion_matrix)
    recalls = calculate_recalls(confusion_matrix)
    avg_precision = np.average(precisions[:-1])
    avg_recall = np.average(recalls[:-1])
    accuracy = calculate_accuracy(confusion_matrix)
    log_txt = 'Precision: Average (w/o U) {0:.2%} -> {1}\nRecall: Average (w/o U) {2:.2%} -> {3}\nAccuracy: {4:.2%}\n'.format(
        avg_precision, precisions, avg_recall, recalls, accuracy)
    log_txt += '{}'.format(confusion_matrix)
    print("{}\n".format(log_txt))


def readAnswerSet(answerSetFile):
    tactics_dict = createTacticsDict(answerSetFile)
    with open(answerSetFile, 'r') as file:
        curr_tactic = ''
        for line in file.readlines():
            if line.startswith('# '):
                curr_tactic = line.strip(' #\n')
                continue
            line = line.strip()
            if not line:
                continue
            tactics_dict[curr_tactic].append(line)
    return tactics_dict


def createTacticsDict(answerSetFile):
    tactics = []
    with open(answerSetFile, 'r') as file:
        for line in file.readlines():
            if line.startswith('# '):
                tactic = line.strip(' #\n')
                tactics.append(tactic)
    return dict((k, []) for k in tactics)


if __name__ == "__main__":
    answerSetFile = sys.argv[1]
    infile = sys.argv[2]

    answers = readAnswerSet(answerSetFile)
    process_file(infile, answers)
