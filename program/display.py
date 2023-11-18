import json
import os


class display:
    def __init__(self):
        self.data_path = "../data/"
        self.page_link = "pageLink.txt"
        self.tree_pic_path = "../treePic/"
        self.index_path = "../index/"
        self.output_path = "../queryOutput/"

        self.index_directory = "directory.txt"
        self.schemas = "schemas.txt"

        self.order_pos = 3
        self.type_pos = 0
        self.root_pos = 2
        self.content_pos = 2
        self.relation_pos = 0
        self.attr_pos = 1

    """
        This function is used to  display the table
    """
    def displayTable(self, rel, fname):
        path = os.path.join(self.data_path, rel)
        with open(os.path.join(self.data_path, rel, self.page_link)) as pl:
            content = pl.readlines()[0]
            pages = json.loads(content)

        data = []
        for page in pages:
            with open(os.path.join(path, page)) as f:
                content = f.readlines()[0]
                two_tuples = json.loads(content)
                data += two_tuples

        if not os.path.exists(self.output_path):
            os.mkdir(os.path.join(self.output_path))
        with open(os.path.join(self.output_path, fname), "a+") as qr:
            for d in data:
                qr.write(json.dumps(d) + "\r\n")

            qr.write("\r\n\r\n")


    def display_schema(self, rel, fname):
        schema = self.getschema(rel)
        with open(os.path.join(self.output_path, fname), "a+") as qr:
            qr.write(json.dumps(schema) + "\r\n")

    def getschema(self, rel):
        with open(os.path.join(self.data_path, self.schemas)) as sc:
            content = sc.readlines()[0]
            fields = json.loads(content)
            fields = [field for field in fields if field[0] == rel]
            fields.sort(key=lambda x: x[self.order_pos])
            schema = [field[1] for field in fields]
        return schema

    # Print 3 Relations(Tables) -Products, Suppliers, Supply
    def printTableRelation(self, rel):
        path = os.path.join(self.data_path, rel)
        with open(os.path.join(self.data_path, rel, self.page_link)) as pl:
            content = pl.readlines()[0]
            pages = json.loads(content)

        data = []
        for page in pages:
            with open(os.path.join(path, page)) as f:
                content = f.readlines()[0]
                two_tuples = json.loads(content)
                data += two_tuples

        for d in data:
            print(d)


    #Display Tree Logic
    def displayTreePic(self, filename="pg06.txt"):
        if not os.path.exists(self.tree_pic_path):
            os.mkdir(os.path.join(self.tree_pic_path))
        att, rel = self.getRelation(filename)
        tree_pic_name = self.getTreePicName(rel, att)
        indent_no = 0
        with open(os.path.join(self.index_path, filename)) as root, open(os.path.join(self.tree_pic_path, tree_pic_name), "w") as tree_pic:
            content = root.readlines()[0]
            tree_pic.write(" " * indent_no + filename + ": " + content + "\r\n")
            data = json.loads(content)
            if data[self.type_pos] == "I":
                for entry in data[self.content_pos]:
                    if entry.endswith(".txt"):
                        self.treePicInsert(entry, indent_no + 2, tree_pic)


    def treePicInsert(self, filename, indent_no, distfile):
        with open(os.path.join(self.index_path, filename)) as f:
            content = f.readlines()[0]
            distfile.write(" " * indent_no + filename + ": " + content + "\r\n")
            data = json.loads(content)
            if data[self.type_pos] == "I":
                for entry in data[self.content_pos]:
                    if entry.endswith(".txt"):
                        self.treePicInsert(entry, indent_no + 2, distfile)


    # get relation and it's attributes
    def getRelation(self, filename):
        with open(os.path.join(self.index_path, self.index_directory)) as id_:
            content = id_.readlines()[0]
            tuples = json.loads(content)
            for tuple_ in tuples:
                if tuple_[self.root_pos] == filename:
                    rel = tuple_[self.relation_pos]
                    att = tuple_[self.attr_pos]
                    break
        return att, rel



    # get tree pic name
    def getTreePicName(self, relation, attribute):
        return relation + "_" + attribute + ".txt"


# call to main method
if __name__ == "__main__":
    #to diaplay treepic on suppliers sid
    display().displayTreePic("pg82.txt")

    #to display treepic on supply pid
    display().displayTreePic("pg73.txt")

    #to display tables
    display().printTableRelation("Products")
    display().printTableRelation("Suppliers")
    display().printTableRelation("Supply")
