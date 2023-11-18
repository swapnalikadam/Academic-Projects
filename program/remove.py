import json
import os
import shutil

class Remove:
    def __init__(self):
        self.data_path = "../data/"
        self.index_path = "../index/"
        self.index_directory = "directory.txt"
        self.page_pool = "pagePool.txt"
        self.page_link = "pageLink.txt"
        self.schema_file = "schemas.txt"
        self.pos_type = 0
        self.pos_content = 2
        self.pos_relation = 0
        self.pos_attr = 1
        self.pos_root = 2

    """
    This function is used to remove pages and dump it back to the page pool    
    """
    def search_remove_page(self, filename):
        # passing an empty string as there is no rel
        new_data = self.read_data_file("", self.index_path, filename)
        if new_data[self.pos_type] == "I":
            new_pages = []
            for entry in new_data[self.pos_content]:
                if entry.endswith(".txt"):
                    self.search_remove_page(entry)
                    new_pages.append(entry)
                    os.remove(os.path.join(self.index_path, entry))

                new_page_pool = self.read_data_file("", self.index_path, self.page_pool)
                new_page_pool.extend(new_pages)
                new_page_pool.sort(reverse=True)

            with open(os.path.join(self.index_path, self.page_pool), 'w') as df:
                df.write(json.dumps(new_page_pool))


    def removeTree(self,rel, att):
        tree_tuples = self.read_data_file(rel, self.index_path, self.index_directory)
        for _tt in tree_tuples:
            if _tt[self.pos_relation] == rel and _tt[self.pos_attr] == att:
                self.search_remove_page(_tt[self.pos_root])
                os.remove(os.path.join(self.index_path, _tt[self.pos_root]))

        with open(os.path.join(self.index_path, self.index_directory), "w") as f:
            res = json.dumps([tuple_ for tuple_ in tree_tuples if tuple_[self.pos_relation] != rel or tuple_[self.pos_attr] != att])
            f.write(res)


    def removeTable(self,rel):
        new_path = os.path.join(self.data_path, rel)
        if os.path.exists(new_path):
            pages = self.read_data_file(rel, self.data_path, self.page_link)
            page_pool_content = self.read_data_file(rel, self.data_path, self.page_pool)


            with open(os.path.join(self.data_path, self.page_pool), "w") as pp:
                res = json.dumps(page_pool_content + pages)
                pp.write(res)

            fields_content = self.read_data_file(rel, self.data_path, self.schema_file)

            fields_content = [field for field in fields_content if field[self.pos_relation] != rel]
            with open(os.path.join(self.data_path, self.schema_file), "w") as sc:
                res = json.dumps(fields_content)
                sc.write(res)

            shutil.rmtree(new_path)
            data_indices = self.read_data_file(rel, self.index_path, self.index_directory)
            for index in data_indices:
                if index[self.pos_relation] == rel:
                    self.removeTree(index[self.pos_relation], index[self.pos_attr])

    def read_data_file(self, rel, path1,path2):
        if path2 == self.page_link:
            path = os.path.join(path1, rel, path2)
        else:
            path = os.path.join(path1, path2)
        with open(path) as pl:
            content = pl.readlines()[0]
            data = json.loads(content)
            return data


if __name__ == "__main__":
    Remove().removeTable("Supply_tmp")
    removeObj = Remove()
