# -*- coding: utf-8 -*-

import pickle
import tensorflow as tf
import json
import jieba

from extraction_model import Model
from extraction_utils import get_logger, create_model, load_config
from extraction_data_utils import load_word2vec, input_from_line

flags = tf.app.flags
flags.DEFINE_string("ckpt_path",    "ckpt",      "Path to save model")
flags.DEFINE_string("log_file",     "train.log",    "File for log")
flags.DEFINE_string("map_file",     "maps.pkl",     "file for maps")
flags.DEFINE_string("config_file",  "config_file",  "File for config")

FLAGS = tf.app.flags.FLAGS

class crf_entities_extraction():
    def __init__(self, jieba_flag=True):
        self.config = load_config(FLAGS.config_file)
        self.logger = get_logger(FLAGS.log_file)
        # limit GPU memory
        self.tf_config = tf.ConfigProto()
        self.tf_config.gpu_options.allow_growth = True
        self.jieba_flag = jieba_flag
        with open(FLAGS.map_file, "rb") as f:
            self.char_to_id, self.id_to_char, self.tag_to_id, self.id_to_tag = pickle.load(f)
    
    '''
    def api(self, str):
        tf.reset_default_graph()
        with tf.Session(config=self.tf_config) as sess:
            model = create_model(sess, Model, FLAGS.ckpt_path, load_word2vec, self.config,
                                 self.id_to_char, self.logger)
            result = model.evaluate_line(sess, input_from_line(str, self.char_to_id), self.id_to_tag)
            result2 = entities_deduplicate(result["entities"])
            if self.jieba_flag == True:
                for i in result2:
                    if i["type"] == "LOCATION":
                        start_index = i["start"]
                        end_index = i["end"]
                        jieba_res = list(jieba.tokenize(str))
                        for j in jieba_res:
                            if j[1] <= start_index and j[2] >= end_index:
#                                print "jieba working"
                                start_index = i["start"] = j[1]
                                end_index = i["end"] = j[2]
                                i["word"] = str[start_index:end_index]
#                                print (i["start"], i["end"], i["word"])
            list1 = [i["type"] for i in result2]
            list2 = [i["word"] for i in result2]
            result_dict = dict(zip(list1, list2))
        return result_dict
#        return result2
        '''
        
    
    def api(self, str):
        NewInfo = {}
        tf.reset_default_graph()
        with tf.Session(config=self.tf_config) as sess:
            model = create_model(sess, Model, FLAGS.ckpt_path, load_word2vec, self.config,
                                 self.id_to_char, self.logger)
            result = model.evaluate_line(sess, input_from_line(str, self.char_to_id), self.id_to_tag)
            result2 = entities_deduplicate(result["entities"])
            if self.jieba_flag == True:
                for i in result2:
                    if i["type"] == "LOCATION":
                        start_index = i["start"]
                        end_index = i["end"]
                        jieba_res = list(jieba.tokenize(str))
                        for j in jieba_res:
                            if j[1] <= start_index and j[2] >= end_index:
#                                print "jieba working"
                                start_index = i["start"] = j[1]
                                end_index = i["end"] = j[2]
                                i["word"] = str[start_index:end_index]
            list1 = [i["type"] for i in result2]
            list2 = [i["word"] for i in result2]
            EventInfo = dict(zip(list1, list2))
            if EventInfo!=None:
                if "TIME" in EventInfo:
                    NewInfo["Event_time"]=EventInfo["TIME"]
                else:
                    NewInfo["Event_time"]=''
    #                            print EventInfo["Event_time"]#.decode("utf-8")
                if "LOCATION" in EventInfo:
                    NewInfo["Event_address"]=EventInfo["LOCATION"]
                else:
                    NewInfo["Event_address"]=''
                if "TYPE" in EventInfo:
                    NewInfo["Event_type"]=EventInfo["TYPE"]
                else:
                    NewInfo["Event_type"]=''
                if "TOTAL_NUM" in EventInfo:
                    NewInfo["Event_total"]=EventInfo["TOTAL_NUM"]
                else:
                    NewInfo["Event_total"]=''
                if "ORGANIZATION" in EventInfo:
                    NewInfo["Event_gname"]=EventInfo["ORGANIZATION"]
                else:
                    NewInfo["Event_gname"]=''
                if "HURT_NUM" in EventInfo:
                    NewInfo["Event_nwound"]=EventInfo["HURT_NUM"]
                else:
                    NewInfo["Event_nwound"]=''
                if "DEAD_NUM" in EventInfo:
                    NewInfo["Event_nkill"]=EventInfo["DEAD_NUM"]
                else:
                    NewInfo["Event_nkill"]=''
            else:
                NewInfo["Event_time"]=''
                NewInfo["Event_address"]=''
                NewInfo["Event_type"]=''
                NewInfo["Event_gname"]=''
                NewInfo["Event_nwound"]=''
                NewInfo["Event_nkill"]=''
        return NewInfo
                
        
    def file_test(self, file):
        with open(file) as f:
            str = process_str(f.read())
#        print str
        return self.api(str)
    
def entities_deduplicate(li):
    entities_temp = li
    entities_result = []
    if entities_temp:
        entities_result.append(entities_temp[0])
    for dict in entities_temp:
        k = 0
        for item in entities_result:
            if dict['type'] != item['type']:
                k += 1
            else:
                break
            if k == len(entities_result):
                entities_result.append(dict)
    return entities_result

def process_str(str):
    return json.dumps(str, ensure_ascii=False)


if __name__=="__main__":
    obj = crf_entities_extraction(jieba_flag=True)
#    str = process_str(raw_input(unicode("请输入带抽取文本：", "utf-8").encode('utf-8')))
    while True:
        str = input("请输入带抽取文本：")
        if str == "exit":
            break
        #res = obj.file_test("1.txt")
        print(process_str(obj.api(str)) + '\n')