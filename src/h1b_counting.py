from collections import Counter
import sys
import operator
import io


class H1B():

    def __init__(self, csv_loc='input/h1b_input.csv',out1 = 'output/top_10_states.txt',out2 = 'output/top_10_occupations.txt'): # out1,out2 output file locations  csv_loc input csv file location

        #creating a list of dictionaries, where each entry is an application
        file = io.open(csv_loc, encoding='utf8')              # opening csv file
        keys =  file.readline().rstrip('\n').split(';')[1:]   # geting the keys and removing trailing semi-colon
        dict_list =[]                                         # empty list of dictionaries
        for line in file:                                     # reading the file line by line
            values = line.rstrip('\n').split(';')[1:]
            dict_list.append(dict(zip(keys, values)))         # this creates a dictionary with the extracted key value pairs  and appends it to the list
        self.applications = dict_list
        self.out1 = out2                                      # saving the output file locations
        self.out2 = out1

    def create_text_files(self):

        total_states,total_titles = map(list,zip(*[self.get_val(d) for d in self.applications if d['CASE_STATUS']=='CERTIFIED'])) # getting a list of all the states and job titles where case status is certified

        states = Counter(total_states).most_common(10)   # gettting top 10 most common states and titles
        titles = Counter(total_titles).most_common(10)

        header1 = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'  # headers for output files
        header2 = 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n'

        self.write_file(states,header1,len(total_states),self.out1)
        self.write_file(titles,header2,len(total_titles),self.out2)

    def get_val(self,d):
        return d['WORKSITE_STATE'].replace('"', ''),d['SOC_NAME'].replace('"', '')  # this function returns the required values in the dictionary

    def write_file(self,data,header,total_apps,out_loc):
        write_data = sorted(sorted(data, key = lambda x : x[0]), key = lambda x : x[1], reverse = True)  # sorting the tupple in decending order with respect to number of applications
                                                                                                        # alphabetically if the number of applications is same
        with open(out_loc, 'w') as fh:
            fh.write(header)
            for d in write_data:
        #         print('{0};{1};{2:0.01f}%'.format(state[0],state[1],state[1]/len(a)*100))
                fh.write('{0};{1};{2:0.01f}%\n'.format(d[0],d[1],(float(d[1])/total_apps)*100))   # formatiing for printing into the file

if __name__ == '__main__':

    if(len(sys.argv) == 4):
        h1b = H1B(csv_loc=sys.argv[1],out1 = sys.argv[2],out2= sys.argv[3])       # extracting the file locations from input arguments
    else:
        h1b = H1B()                                                               # if input arguments not present use default values

    h1b.create_text_files();


# sys.arg
