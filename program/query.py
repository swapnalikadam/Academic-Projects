import os

from relAlg import select, project, join
from display import display
from remove import Remove

class QueryClass:
    def __init__(self):
        self.SUPPLY = "Supply"
        self.PRODUCTS = "Products"
        self.SUPPLIERS = "Suppliers"
        self.QUERY_OUTPUT = "../queryOutput/"
        self.QUERY_RESULT = "queryResult.txt"

    def query_a(self):
        temp_result = select(self.SUPPLIERS, "sid", "=", "s23")
        query_result = project(temp_result, ["sname"])
        Remove().removeTable("Suppliers_tmp")
        return query_result


    def query_b(self):
        tmp_result = select(self.SUPPLIERS, "sid", "=", "s23")
        query_result = project(tmp_result, ["sname"])
        Remove().removeTable("Suppliers_tmp")
        return query_result


    def query_c(self):
        tmp_result = select(self.SUPPLY, "pid", "=", "p15")
        tmp_result = join(tmp_result, "sid", self.SUPPLIERS, "sid")
        query_result = project(tmp_result, ["address"])
        Remove().removeTable("Supply_tmp")
        Remove().removeTable(tmp_result)
        return query_result

    def query_d(self):
        tmp_res1 = select(self.SUPPLIERS, "sname", "=", "Kiddie")
        tmp_res2 = select(self.SUPPLY, "pid", "=", "p20")
        tmp_result = join(tmp_res1, "sid", tmp_res2, "sid")
        query_result = project(tmp_result, ["cost"])
        Remove().removeTable("Suppliers_tmp")
        Remove().removeTable("Supply_tmp")
        Remove().removeTable(tmp_result)
        return query_result


    def query_e(self):
        tmp_result = select(self.SUPPLY, "cost", ">=", 47.00)
        tmp_res1 = join(tmp_result, "pid", self.PRODUCTS, "pid")
        tmp_res2 = join(tmp_res1, "sid", self.SUPPLIERS, "sid")
        query_result = project(tmp_res2, ["sname", "pname", "cost"])
        Remove().removeTable("Supply_tmp")
        Remove().removeTable(tmp_res1)
        Remove().removeTable(tmp_res2)
        return query_result

    def display_table(self, result):
        display().display_schema(result, self.QUERY_RESULT)
        display().displayTable(result, self.QUERY_RESULT)
        Remove().removeTable(res)

    def open_file(self,string):
        with open(os.path.join(self.QUERY_OUTPUT, self.QUERY_RESULT), "a+") as qr:
            qr.write(string)


if __name__ == "__main__":

    ###### QUERY A ########
    QueryClass().open_file("Query A : Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid.\r\n\r\n")
    res = QueryClass().query_a()
    QueryClass().display_table(res)

    ###### QUERY B ########
    Remove().removeTree(QueryClass().SUPPLIERS, "sid")
    QueryClass().open_file("Query B : Remove the B+_tree from Suppliers.sid, and repeat Question a.\r\n\r\n")
    res = QueryClass().query_b()
    QueryClass().display_table(res)

    ###### QUERY C ########
    QueryClass().open_file("Query C : Find the address of the suppliers who supplied ‘p15’.\r\n\r\n")
    res = QueryClass().query_c()
    QueryClass().display_table(res)

    ###### QUERY D ########
    QueryClass().open_file("Query D : What is the cost of ‘p20’ supplied by ‘Kiddie’?\r\n\r\n")
    res = QueryClass().query_d()
    QueryClass().display_table(res)

    ###### QUERY E ########
    QueryClass().open_file("Query E : For each supplier who supplied products with a cost of 47 or higher, list his/her name, product name and the cost.\r\n\r\n")
    res = QueryClass().query_e()
    QueryClass().display_table(res)

