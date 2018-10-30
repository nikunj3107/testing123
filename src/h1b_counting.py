from collections import Counter
import sys
import operator
import io


class H1B():

    def __init__(self, csv_loc='input/h1b_input.csv',out1 = 'output/top_10_states.txt',out2 = 'output/top_10_occupations.txt'):

        file = io.open(csv_loc, encoding='utf8')
        keys =  file.readline().rstrip('\n').split(';')[1:]
        dict_list =[]
        for line in file:
            values = line.rstrip('\n').split(';')[1:]
            dict_list.append(dict(zip(keys, values)))
        self.applications = dict_list
        self.out1 = out2
        self.out2 = out1

    def create_text_files(self):

        total_states,total_titles = map(list,zip(*[self.get_val(d) for d in self.applications if d['CASE_STATUS']=='CERTIFIED']))

        states = Counter(total_states).most_common(10)
        titles = Counter(total_titles).most_common(10)

        header1 = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'
        header2 = 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'

        self.write_file(states,header1,len(total_states),self.out1)
        self.write_file(titles,header2,len(total_titles),self.out2)

    def get_val(self,d):
        return d['WORKSITE_STATE'].replace('"', ''),d['SOC_NAME'].replace('"', '')

    def write_file(self,data,header,total_apps,out_loc):
        write_data = sorted(sorted(data, key = lambda x : x[0]), key = lambda x : x[1], reverse = True)
        with open(out_loc, 'w') as fh:
            fh.write(header)
            for d in write_data:
        #         print('{0};{1};{2:0.01f}%'.format(state[0],state[1],state[1]/len(a)*100))
                fh.write('{0};{1};{2}%\n'.format(d[0],d[1],d[1]/total_apps*100))

if __name__ == '__main__':

    if(len(sys.argv) == 4):
#         print(sys.argv)
        h1b = H1B(csv_loc=sys.argv[1],out1 = sys.argv[2],out2= sys.argv[3])
    else:
        h1b = H1B()

    h1b.create_text_files();


# sys.arg
