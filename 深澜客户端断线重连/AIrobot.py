# -*- coding: utf-8 -*-
import io

conv_path = "dgk_shooter_min.conv"
ask_file_path = "ask.conv"
answer_file_path = "answer.conv"

def gen_ask_ans(conv_path, ask_file_path, answer_file_path):
    convs = []  # conversation set
    with io.open(conv_path, encoding="utf8") as f:
        one_conv = []  # a complete conversation
        for line in f:
            line = line.strip('\n').replace('/', '')
            if line == '':
                continue
            if line[0] == 'E':
                if one_conv:
                    convs.append(one_conv)
                one_conv = []
            elif line[0] == 'M':
                one_conv.append(line.split(' ')[1])
# Grasping calligraphy answer answer
    ask = []  # ask
    response = []  # answers
    ask_file = io.open(ask_file_path,"w", encoding="utf-8")
    answer_file = io.open(answer_file_path,"w", encoding="utf-8")
    for conv in convs:
        if len(conv) == 1:
            continue
        if len(conv) % 2 != 0:
            conv = conv[:-1]
        for i in range(len(conv)):
            if i % 2 == 0:
                ask.append(conv[i])
                ask_file.write(conv[i]+"\n")
            else:
                response.append(conv[i])
                answer_file.write(conv[i]+"\n")

def gen_vocabulary_file(input_file, output_file):
    vocabulary = {}
    with io.open(input_file, encoding="utf-8") as f:
        counter = 0
        for line in f:
            counter += 1
            tokens = [word for word in line.strip()]
            for word in tokens:
                if word in vocabulary:
                    vocabulary[word] += 1
                else:
                    vocabulary[word] = 1
        vocabulary_list = sorted(vocabulary, key=vocabulary.get, reverse=True)
        # For taking 10000 custom character kanji
        if len(vocabulary_list) > 10000:
            vocabulary_list = vocabulary_list[:10000]
        print(input_file + " phrase table size:", len(vocabulary_list))
        with io.open(output_file, "w", encoding="utf-8") as ff:
            for word in vocabulary_list:
                ff.write(word + "\n")

def convert_conversation_to_vector(input_file, vocabulary_file, output_file):
    in_file = io.open(input_file, "r", encoding="utf-8")
    out_file = io.open(output_file, "w", encoding="utf-8")
    tmp_vocab = []
    with io.open(vocabulary_file, "r", encoding="utf-8") as f:
        tmp_vocab.extend(f.readlines())
    tmp_vocab = [line.strip() for line in tmp_vocab]
    vocab = dict([(x, y) for (y, x) in enumerate(tmp_vocab)])
    #for (k,v) in vocab.items():
    #    print "dict[%s]=" % v,k.encode('utf-8')
    with in_file as f:
        for line in f:
            temp_str=""
            for word in line.strip():
                if word in vocab:
                    temp_str += str(vocab[word])+" "
            #temp_str += "\n"
            print temp_str
            #out_file.write(temp_str)
    
#    for item in vocab:
#        print item.encode('utf-8')

#gen_vocabulary_file(conv_path, "vocabulary.dic")
#convert_conversation_to_vector(ask_file_path, "vocabulary.dic", "train_ask.vec")
convert_conversation_to_vector(answer_file_path, "vocabulary.dic", "train_answer.vec")
