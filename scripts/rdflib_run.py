"""
2개 방향 중 1번으로 먼저 접근했는데, 막상 온톨로지 수정하려고 하니 복잡해서 2>를 위해 rdflib_run.py 만듦.
1> TTL → .lst 변환기를 만들고, 기존 makegraph.py로 넘기기rdflib 같은 라이브러리로 TTL을 파싱
트리플에서 Class(rdf:type), Relation(predicate), Node(subject/object)를 추출해 .lst 형식으로 매핑
그다음 지금 만든 makegraph.py로 그대로 그래프 생성
2> TTL을 바로 읽어서 Vis.js로 그리는 별도 스크립트 작성.lst 경유 없이 rdflib으로 파싱한 트리플을 곧장 nodes/edges로 변환
"""

from rdflib import Graph, RDF, RDFS

# 1. TTL 파일 파싱
g = Graph()
g.parse("semantic_archive_v3_full_sourced.ttl", format="turtle")

nodes = []
edges = []
node_set = set()

# 2. Triple 순회 및 Vis.js 포맷 변환
for s, p, o in g:
    # URI를 보기 편한 라벨이나 이름으로 정리
    subj = str(s).split('#')[-1].split('/')[-1]
    pred = str(p).split('#')[-1].split('/')[-1]
    obj = str(o).split('#')[-1].split('/')[-1]
    
    # Node 추가 (중복 제거)
    if subj not in node_set:
        nodes.append({"id": subj, "label": subj})
        node_set.add(subj)
    if obj not in node_set:
        nodes.append({"id": obj, "label": obj})
        node_set.add(obj)
        
    # Edge(관계) 추가
    edges.append({"from": subj, "to": obj, "label": pred})

# 3. 이 nodes/edges 배치를 JSON으로 추출 후 Vis.js HTML에 주입