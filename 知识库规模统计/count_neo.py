import json
import os
from py2neo import Graph


def store_json(data, file_path):
    """
    将json写入文件
    :param data:
    :param file_path:
    :return:
    """
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def query_entity_count(graph, ndigits=2):        
    query_dict = dict()
    cql = "MATCH (n:Ontology) RETURN DISTINCT n.type AS ntype,count(n) AS num"
    query_result = graph.run(cql).data()
    for entity in query_result:
        query_dict[entity["ntype"]] = entity["num"]
    
    count_dict = dict()
    total = sum(list(query_dict.values()))
    key_num = len(list(query_dict.keys()))
    for key,value in query_dict.items():
        entity = dict()
        entity["count"] = value
        entity["percent"] = round(100*value/total,ndigits)
        count_dict[key] = entity

    result = dict()
    result["total"] = total
    result["type_num"] = key_num
    result["type_count"] = count_dict
    return result
    

def query_rel_count(graph, ndigits=2):
    query_dict = dict()
    cql = "MATCH (n:Ontology)-[r]->(m:Ontology) RETURN DISTINCT type(r) AS rtype,count(r) AS num"
    query_result = graph.run(cql).data()
    for entity in query_result:
        query_dict[entity["rtype"]] = entity["num"]
    
    count_dict = dict()
    total = sum(list(query_dict.values()))
    key_num = len(list(query_dict.keys()))
    for key,value in query_dict.items():
        entity = dict()
        entity["count"] = value
        entity["percent"] = round(100*value/total,ndigits)
        count_dict[key] = entity

    result = dict()
    result["total"] = total
    result["type_num"] = key_num
    result["type_count"] = count_dict
    return result


if __name__ == "__main__":
    graph = Graph(host="202.120.40.114", http_port=37475, user="neo4j", password="neo4j", bolt=False)
    out_folder = "结果"
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        
    entity_dict = query_entity_count(graph)
    rel_dict = query_rel_count(graph)
    print("实体统计:")
    print(entity_dict)
    print("关系统计:")
    print(rel_dict)
    store_json(entity_dict, os.path.join(out_folder, "实体统计.json"))
    store_json(rel_dict, os.path.join(out_folder, "关系统计.json"))

