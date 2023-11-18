import json
import os

import pandas as pd

from dataSetTypes import CAPACITY, DATA_PATH, INDEX_PATH, INDEX_DIRECTORY, PAGE_LINK, SCHEMAS, PAGE_POOL, ORDER_POS, \
    TYPE_POS, CONTENT_POS, RELATION_POS, ATTR_POS, ROOT_POS, LEAF_NODE, INDEX_TYPE, ATT_CATEGORY, DIRECTION, \
    clustered_index, xid_att, att_type


def get_tuples_by_clustered_index(leaf_node, rel, val, op):
    print(leaf_node, rel, val, op)
    res = []
    content = leaf_node[LEAF_NODE.CONTENT.value]
    counter = 0
    related_list = []
    for index, value in enumerate(content):
        if isinstance(value, str) and value == val:
            related_list = content[index + 1]

    if not related_list:
        raise Exception("Invalid val detected!! Please check your input value!!")

    with open(os.path.join(DATA_PATH, rel, PAGE_LINK)) as pl:
        content = pl.readlines()[0]
        pages = json.loads(content)

        if op == '=':
            # Simple case : add every row in Related list
            for pointer in related_list:
                filename, index = pointer[:-2], int(pointer[-1])
                print("1 FileName", filename)
                print("Index", index)
                print("Value and Operation", value, op)
                res = get_single_tuple(filename, index, rel, res)
        elif op == "<=":
            # if pages are related to values to be searched then it is stored in related_list
            # Search stops on last related file
            filename, index = related_list[-1][:-2], int(related_list[-1][-1])
            print("2 FileName", filename)
            print("Index", index)
            print("Value and Operation", value, op)
            for idx, val in enumerate(pages):
                counter += 1
                # Break if Last page is reached
                if val == filename:
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        res.append(data[0])
                        if index == 1:
                            res.append(data[1])
                    break

                with open(os.path.join(DATA_PATH, rel, val)) as f:
                    content = f.readlines()[0]
                    data = json.loads(content)
                    res += data
        elif op == '<':
            filename, index = related_list[0][:-2], int(related_list[0][-1])
            print("3 FileName", filename)
            print("Index", index)
            print("Value and Operation", value, op)
            for idx, val in enumerate(pages):
                counter += 1
                # Stop on the first file in Related list considering index position
                if val == filename:
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        if index == 1:
                            res.append(data[0])
                    break

                with open(os.path.join(DATA_PATH, rel, val)) as f:
                    content = f.readlines()[0]
                    data = json.loads(content)
                    res += data
        elif op == ">=":
            filename, index = related_list[0][:-2], int(related_list[0][-1])

            print("4 FileName", filename)
            print("Index", index)
            print("Value and Operation", value, op)
            flag = False
            for idx, val in enumerate(pages):
                counter += 1
                if flag:
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        res += data

                # Start from the First file in related list and search till the end of the pages
                if val == filename:
                    flag = True
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        if index == 0:
                            res.append(data[0])

                        res.append(data[1])
        elif op == '>':
            filename, index = related_list[-1][:-2], int(related_list[-1][-1])
            print("5 FileName", filename)
            print("Index", index)
            print("Value and Operation", value, op)
            flag = False
            for idx, val in enumerate(pages):
                counter += 1
                if flag:
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        res += data

                if val == filename:
                    flag = True
                    with open(os.path.join(DATA_PATH, rel, val)) as f:
                        content = f.readlines()[0]
                        data = json.loads(content)
                        if index == 0:
                            res.append(data[1])
        else:
            raise Exception('Invalid op value !!!')

    return res, counter


def get_single_tuple(filename, index, rel, res):
    with open(os.path.join(DATA_PATH, rel, filename)) as f:
        content = f.readlines()[0]
        data = json.loads(content)
        res.append(data[index])

    return res


def get_data_files(rel, node_content, res):
    for item in node_content:
        if isinstance(item, list):
            for pointer in item:
                filename, index = pointer[:-2], int(pointer[-1])
                with open(os.path.join(DATA_PATH, rel, filename)) as f:
                    content = f.readlines()[0]
                    data = json.loads(content)
                    res.append(data[index])

    return res


def search(pointer, rel, res, direction=DIRECTION.LEFT):
    with open(os.path.join(INDEX_PATH, pointer)) as f:
        node = f.readlines()[0]
        data = json.loads(node)
        content = data[LEAF_NODE.CONTENT.value]
        if direction == DIRECTION.LEFT:
            content.reverse()
        res = get_data_files(rel, content, res)
        next_pointer = data[
            LEAF_NODE.LEFT_POINTER.value if direction == DIRECTION.LEFT else LEAF_NODE.RIGHT_POINTER.value]

    if next_pointer != "nil":
        res = search(next_pointer, rel, res, direction)
    return res


def get_tuples_by_unclustered_index(leaf_node, rel, val, op):
    res = []
    counter = 0
    content = leaf_node[LEAF_NODE.CONTENT.value]
    if op in ('<', '<='):
        content.reverse()
        print("edited < <=", content)
        for index, value in enumerate(content):
            counter += 1
            if (isinstance(value, str) and value == val and op == '<=') or (isinstance(value, str) and value < val):
                item = content[index - 1]
                for pointer in item:
                    filename, index = pointer[:-2], int(pointer[-1])
                    res = get_single_tuple(filename, index, rel, res)
        if leaf_node[LEAF_NODE.LEFT_POINTER.value] != "nil":
            res = search(leaf_node[LEAF_NODE.LEFT_POINTER.value], rel, res, DIRECTION.LEFT)
    elif op in ('>', '>='):
        print("edited > >=", content)
        for index, value in enumerate(content):
            counter += 1
            if (isinstance(value, str) and value == val and op == '>=') or (isinstance(value, str) and value > val):
                item = content[index + 1]
                for pointer in item:
                    filename, index = pointer[:-2], int(pointer[-1])
                    res = get_single_tuple(filename, index, rel, res)
        if leaf_node[LEAF_NODE.RIGHT_POINTER.value] != "nil":
            res = search(leaf_node[LEAF_NODE.RIGHT_POINTER.value], rel, res, DIRECTION.RIGHT)
    elif op == '=':
        print("edited =", content)
        for index, value in enumerate(content):
            counter += 1
            if isinstance(value, str) and value == val:
                item = content[index + 1]
                for pointer in item:
                    filename, index = pointer[:-2], int(pointer[-1])
                    res = get_single_tuple(filename, index, rel, res)
    else:
        raise Exception('Invalid op value!!!')

    return res, counter


def convert_id_to_int(id_):
    return int(id_[1:])


def dfs(filename, rel, searchVal, op, index_type=INDEX_TYPE.CLUSTERED_INDEX, att_type=ATT_CATEGORY.OTHER):
    """
        :param filename: Starting point of B+ tree, Treeroot
        :param rel: Relation Name
        :param searchVal: KeyValue
        :param op: Operation >, < , ==
        :param index_type: Clustered/Un-Clustered
        :param att_type: Primary/ XID or Secondary
        :return:
    """
    res = None

    #set counter to 1
    counter = 1
    with open(os.path.join(INDEX_PATH, filename)) as f:
        info = f.readlines()[0]
        data = json.loads(info)
        if data[TYPE_POS] == "I":
            content = data[CONTENT_POS]
            located = False

            for index, value in enumerate(content):
                if not value.endswith(".txt"):
                    if att_type == ATT_CATEGORY.XID:
                        int_val, int_value = convert_id_to_int(searchVal), convert_id_to_int(value)
                    if int_val < int_value if att_type == ATT_CATEGORY.XID else searchVal < value:
                        res, page_read_ctr = dfs(content[index - 1], rel, searchVal, op, index_type, att_type)
                        located = True
                        counter += page_read_ctr
                        break
                    elif searchVal == value:
                        res, page_read_ctr = dfs(content[index + 1], rel, searchVal, op, index_type, att_type)
                        located = True
                        counter += page_read_ctr
                        break

            if not located:
                res, page_read_ctr = dfs(content[-1], rel, searchVal, op, index_type, att_type)
                counter += page_read_ctr
        else:
            counter = 0
            if index_type == INDEX_TYPE.CLUSTERED_INDEX:
                print("&&1")
                res, page_read_ctr = get_tuples_by_clustered_index(data, rel, searchVal, op)
                counter += page_read_ctr
            else:
                print("&&2")
                res, page_read_ctr = get_tuples_by_unclustered_index(data, rel, searchVal, op)
                counter += page_read_ctr

    return res, counter


def get_page():
    # get page from page pool
    with open(os.path.join(DATA_PATH, PAGE_POOL)) as pp:
        content = pp.readlines()[0]
        page_pool = json.loads(content)
        if page_pool:
            page = page_pool.pop(0)
        else:
            raise Exception("Run out of pages!!!")

    # update page pool
    with open(os.path.join(DATA_PATH, PAGE_POOL), 'w') as f:
        f.write(json.dumps(page_pool))
    return page


def join_by_index(rel, att, val):
    tree_root = None
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as id_:
        indices = json.loads(id_.readlines()[0])
        for index in indices:
            if index[RELATION_POS] == rel and index[ATTR_POS] == att:
                tree_root = index[ROOT_POS]
                break

    if att in xid_att:
        att_type = ATT_CATEGORY.XID
    else:
        att_type = ATT_CATEGORY.OTHER

    index_type = INDEX_TYPE.UNCLUSTERED_INDEX
    for ci in clustered_index:
        if rel == ci[0] and att == ci[1]:
            index_type = INDEX_TYPE.CLUSTERED_INDEX
            break

    res, _ = dfs(tree_root, rel, val, "=", index_type, att_type)
    return res


def select(rel, att, op, val):
    counter = 0 #page counter
    tree_root = None
    # searching for tree root from directory.txt
    # if found set the tree root
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as id_:
        indices = json.loads(id_.readlines()[0])
        for index in indices:
            if index[RELATION_POS] == rel and index[ATTR_POS] == att:
                tree_root = index[ROOT_POS]
                break

    # set attribute type
    if att in xid_att:
        att_type = ATT_CATEGORY.XID
    else:
        att_type = ATT_CATEGORY.OTHER

    # reading schema of the table
    schema = get_schema(rel)

    data = []
    if tree_root:
        index_type = INDEX_TYPE.UNCLUSTERED_INDEX
        for ci in clustered_index:
            if rel == ci[0] and att == ci[1]:
                index_type = INDEX_TYPE.CLUSTERED_INDEX
                break

        #we are calling dfs function with 6 parameters
        res, res_count = dfs(tree_root, rel, val, op, index_type, att_type)
        counter += res_count
        print("With B+_tree, the cost of searching {att} {op} {val} on {rel} is {value} pages".format(rel=rel,
                                                                                                      att=att,
                                                                                                      op=op,
                                                                                                      val=val,
                                                                                                      value=counter))
    else:
        with open(os.path.join(DATA_PATH, rel, PAGE_LINK)) as pl:
            content = pl.readlines()[0]
            pages = json.loads(content)

            res = []
            for page in pages:
                counter += 1
                with open(os.path.join(DATA_PATH, rel, page)) as pg:
                    page_content = pg.readlines()[0]
                    page_data = json.loads(page_content)
                    data += page_data

                    df = pd.DataFrame(data, columns=schema)
                    if op == '<':
                        df = df.loc[df[att] < val]
                    elif op == '<=':
                        df = df.loc[df[att] <= val]
                    elif op == '=':
                        df = df.loc[df[att] == val]
                    elif op == '>':
                        df = df.loc[df[att] > val]
                    elif op == '>=':
                        df = df.loc[df[att] >= val]
                    else:
                        raise Exception('Invalid op value!!!')
                    res = df.values.tolist()

        print("Without B+_tree, the cost of searching {att} {op} {val} on {rel} is {value} pages".format(rel=rel,
                                                                                                         att=att,
                                                                                                         op=op,
                                                                                                         val=val,
                                                                                                         value=counter))

    update_schemas(rel + "_tmp", schema)
    write_to_pages(rel, res)

    return rel


def get_schema(rel):
    with open(os.path.join(DATA_PATH, SCHEMAS)) as sc:
        content = sc.readlines()[0]
        fields = json.loads(content)
        #list comprehension
        fields = [field for field in fields if field[0] == rel]
        fields.sort(key=lambda x: x[ORDER_POS])
        schema = [field[1] for field in fields]

    return schema



def write_to_pages(rel, res):
    rel_name = rel
    if os.path.exists(os.path.join(DATA_PATH, rel)):
        rel_name = rel + "_tmp"
        if os.path.exists(os.path.join(DATA_PATH, rel_name)):
            return

        os.mkdir(os.path.join(DATA_PATH, rel_name))
    else:
        os.mkdir(os.path.join(DATA_PATH, rel))

    page_link = []
    length = len(res)
    for i in range(0, length, CAPACITY):
        page = get_page()
        page_link.append(page)
        with open(os.path.join(DATA_PATH, rel_name, page), "w") as f:
            f.write(json.dumps(res[i:i + CAPACITY]))

    with open(os.path.join(DATA_PATH, rel_name, PAGE_LINK), "w") as pl:
        pl.write(json.dumps(page_link))


def update_schemas(rel, attList):
    new_items = []
    for index, value in enumerate(attList):
        new_items.append([rel, value, att_type[value], index])
    with open(os.path.join(DATA_PATH, SCHEMAS)) as sc:
        content = sc.readlines()[0]
        schemas = json.loads(content)

    schemas += new_items
    with open(os.path.join(DATA_PATH, SCHEMAS), 'w') as f:
        f.write(json.dumps(schemas))


def project(rel, attList):
    tmp_path = os.path.join(DATA_PATH, rel + "_tmp")
    # TODO: handle the case when path is the initial folder
    path = tmp_path if os.path.exists(tmp_path) else os.path.join(DATA_PATH, rel)
    #print('path', path, '..page-link', os.path.join(path, PAGE_LINK))
    with open(os.path.join(path, PAGE_LINK)) as pl:
        content = pl.readlines()[0]
        page_files = json.loads(content)

    data = []
    for page_file in page_files:
        with open(os.path.join(path, page_file)) as f:
            content = f.readlines()[0]
            page_data = json.loads(content)
            data += page_data

    schema = get_schema(rel)
    df = pd.DataFrame(data, columns=schema)
    df = df.filter(attList)
    df.drop_duplicates(keep=False, inplace=True)
    data = df.values.tolist()

    res = name_the_new_relation(attList, rel)
    update_schemas(res, attList)
    write_to_pages(res, data)

    return res


def name_the_new_relation(attList, rel):
    return rel[:3] + "_" + attList[0][:3]


def name_the_new_relation_v2(rel1, rel2):
    return rel1[:3] + "_" + rel2[:3]


def join(rel1, att1, rel2, att2):
    tmp_rel1_path = os.path.join(DATA_PATH, rel1 + "_tmp")
    if os.path.exists(tmp_rel1_path):
        rel1 = rel1 + "_tmp"
    tmp_rel2_path = os.path.join(DATA_PATH, rel2 + "_tmp")
    if os.path.exists(tmp_rel2_path):
        rel2 = rel2 + "_tmp"
    schema1 = get_schema(rel1)
    schema2 = get_schema(rel2)
    att1_pos = schema1.index(att1)
    att2_pos = schema2.index(att2)
    schema = schema1 + schema2
    schema.pop(att1_pos)

    data = []
    tree_root = None
    with open(os.path.join(INDEX_PATH, INDEX_DIRECTORY)) as id_:
        indices = json.loads(id_.readlines()[0])
        for index in indices:
            # if index[RELATION_POS] == rel1 and index[ATTR_POS] == att1:
            #     tree_rel, tree_root = rel1, index[ROOT_POS]
            #     break
            if index[RELATION_POS] == rel2 and index[ATTR_POS] == att2:
                tree_rel, tree_root = rel2, index[ROOT_POS]
                break

    if tree_root:
        # if tree_rel == rel1:
        #     with open(os.path.join(DATA_PATH, rel2, PAGE_LINK)) as pl2:
        #         rel2_page_files = json.loads(pl2.readlines()[0])
        #
        #     for rel2_page_file in rel2_page_files:
        #         with open(os.path.join(DATA_PATH, rel2, rel2_page_file)) as pg2:
        #             rel2_tuples = json.loads(pg2.readlines()[0])
        #             for rel2_tuple in rel2_tuples:
        #                 res = join_by_index(rel1, att1, rel2_tuple[att2_pos])
        #                 new_data = [r + rel2_tuple for r in res]
        #                 new_data = [nd[:att1_pos] + nd[att1_pos+1:] for nd in new_data]
        #                 data += new_data
        # else:
        with open(os.path.join(DATA_PATH, rel1, PAGE_LINK)) as pl1:
            rel1_page_files = json.loads(pl1.readlines()[0])

        for rel1_page_file in rel1_page_files:
            with open(os.path.join(DATA_PATH, rel1, rel1_page_file)) as pg1:
                rel1_tuples = json.loads(pg1.readlines()[0])
                for rel1_tuple in rel1_tuples:
                    res = join_by_index(rel2, att2, rel1_tuple[att1_pos])
                    new_data = [rel1_tuple + r for r in res]
                    new_data = [nd[:att1_pos] + nd[att1_pos+1:] for nd in new_data]
                    data += new_data
    else:
        with open(os.path.join(DATA_PATH, rel1, PAGE_LINK)) as pl1, open(os.path.join(DATA_PATH, rel2, PAGE_LINK)) as pl2:
            rel1_page_files = json.loads(pl1.readlines()[0])
            rel2_page_files = json.loads(pl2.readlines()[0])

        for rel1_page_file in rel1_page_files:
            with open(os.path.join(DATA_PATH, rel1, rel1_page_file)) as pg1:
                rel1_tuples = json.loads(pg1.readlines()[0])

                for rel2_page_file in rel2_page_files:
                    with open(os.path.join(DATA_PATH, rel2, rel2_page_file)) as pg2:
                        rel2_tuples = json.loads(pg2.readlines()[0])
                        new_data = [t1 + t2 for t1 in rel1_tuples for t2 in rel2_tuples if t1[att1_pos] == t2[att2_pos]]
                        new_data = [nd[:att1_pos] + nd[att1_pos+1:] for nd in new_data]
                        data += new_data

    res = name_the_new_relation_v2(rel1, rel2)
    update_schemas(res, schema)
    write_to_pages(res, data)

    return res
