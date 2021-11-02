import csv
import io
import pandas as pd
import logging
from lxml import etree as et



class Xml:

    def __init__(self, i_file_path=None):
        self.main_df = None
        self.main_flag = None
        self.i_file_path = i_file_path
        self.row_dict = {}
        self.tree = self.read_tree()

    def read_tree(self):
        if not self.i_file_path:
            i_file_path = self.config.make_input_path()
        else:
            i_file_path = self.i_file_path

        tree = et.ElementTree(file=i_file_path)
        return tree

    def get_xml(self):
        return self.tree


    def travel_element(self, element, tag):
        for child in element:
            if len(child) == 0: 
                key = str(child.tag).replace("{__}","")
                value = child.text if child.text is not None else ''
                if key not in self.row_dict.keys():
                    self.row_dict[key] = value
                else:
                    self.row_dict[key] = self.row_dict[key] + '||' + value
            else:
                self.travel_element(child, child.tag)


    def parse_from_root(self):
        root = self.tree.getroot()
        for product_specs in root:
            self.row_dict = {} 
            self.travel_element(product_specs, product_specs.tag)
            result = pd.DataFrame([self.row_dict], columns=self.row_dict.keys())
            if not self.main_flag:  
                self.main_df = result
                self.main_flag = True
            else:
                self.main_df = pd.concat([self.main_df, result])


    def to_csv(self):

        self.main_df.to_csv('books.csv', index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')



if __name__=='__main__':
    xml_class = Xml("books.xml")
    xml_class.parse_from_root()
    xml_class.to_csv()
