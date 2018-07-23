import csv
import codecs

def write_csv(path, list_stream):
    csvFile = codecs.open(path, "w", 'utf-8')
    for stream in list_stream:
        try:
            content = ','.join(stream) + '\n'
            csvFile.write(content)
        except Exception as e:
            a=1
    # writer = csv.writer(csvFile)
    # for stream in list_stream:
    #     writer.writerow(stream)
    csvFile.close()


def read_csv(path):
    list_num = []
    dict_id = {}
    dict_mesg = {}
    reader = []
    csv_reader = csv.reader(open(path, encoding='utf-8'))
    for row in csv_reader:
        reader.append(row)
    list_id = reader[0]
    del reader[0]
    for mesg in reader:
        list_num.append(mesg[0].strip())
        for i in range(len(list_id)-1):
            dict_mesg[list_id[i + 1]] = mesg[i + 1]
        dict_id[mesg[0].strip()] = dict_mesg
        dict_mesg = {}

    return list_id, list_num, dict_id