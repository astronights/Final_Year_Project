import os
import json
from os import listdir
from os.path import isfile, join
import ast
import shutil

BERT_DIR = "/home/fyp19020/BERT-fine-tuning-for-twitter-sentiment-analysis"
BERT_DATA_DIR = f'{BERT_DIR}/data'
BERT_MODEL = "MODEL NAME"

csvPath = '/data/csv/'
allFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f))]

file_name = ""
# get first item that isn't processed
for file in allFiles:
    file = file.replace(".csv", "")
    if not os.path.exists(f'data/results/{file}.json'):
        file_name = file + ".csv"
        break

print(file_name)


src_dir = os.curdir
dst_dir = BERT_DATA_DIR
src_file = os.path.join(src_dir, file_name)
shutil.copy(src_file, dst_dir)

dst_file = os.path.join(dst_dir, file_name)
new_dst_file_name = os.path.join(dst_dir, "get_test.csv")
os.rename(dst_file, new_dst_file_name)

# #get data
# print("reading file\n")
# with open(csvPath + file_name, 'r') as f:
#     raw_input = f.readlines()
# print("file read\n")
#
#
# # Convert data to input file
# lst = [x.replace('\n', '') for x in raw_input]
# df = pd.DataFrame(lst)
# df.to_csv(BERT_DIR + '/data/get_test.csv', sep='\t', index=False, header=False)
# print("input ready...running bert\n")
# print(df.shape)


# Run Command
if os.path.exists(f'{BERT_DATA_DIR}/bert_result/test_results.tsv'):
    os.remove(f'{BERT_DATA_DIR}/bert_result/test_results.tsv')

COMMAND = f'python3 {BERT_DIR}/test_bert/run_classifier.py \
     --task_name=twitter \
     --do_predict=true \
     --data_dir={BERT_DIR}/data \
     --vocab_file={BERT_DIR}/Bert_base_dir/vocab.txt\
     --bert_config_file={BERT_DIR}/Bert_base_dir/bert_config.json\
     --init_checkpoint={BERT_DIR}/model \
     --max_seq_length=64 \
     --output_dir={BERT_DIR}/data/bert_result'
os.system(COMMAND)

with open(f'{BERT_DATA_DIR}/bert_result/test_results.tsv', 'r') as f:
    test_results = f.readlines()

print("BERT successful\n")
# Append data to input
jsonPath = "/data/json"

json_file_name = file_name.replace(".csv", ".json")

obj = []
i = 0
with open(jsonPath + "/" + json_file_name, 'rb') as f:
    line = f.readline().decode()
    while line:
        data = ast.literal_eval(line)
        test_results[i] = test_results[i][:-1]
        data['test_score'] = test_results[i].split('\t')
        obj.append(data)
        line = f.readline().decode()
        i += 1

print("saving results")
# saving data
resultsPath = "/data/results"

if os.path.exists(resultsPath + "/" + json_file_name):
    os.remove(resultsPath + "/" + json_file_name)

with open(resultsPath + "/" + json_file_name, 'w+') as f:
    for item in obj:
        f.write(json.dumps(item))
        f.write("\n")

