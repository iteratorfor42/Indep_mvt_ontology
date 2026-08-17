#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ttl_to_lst.py
-------------
독립운동-근대학교 온톨로지(.ttl, RDF/OWL Turtle)를
MakeGraph2022 호환 재구현(phase1-compatible/makegraph.py)이 읽는
.lst 포맷으로 변환한다.

TTL이 정본(GitHub 보관, Protégé 추론용)이고,
.lst는 이 스크립트로 언제든 다시 생성 가능한 파생 산출물이다.

사용법:
    python ttl_to_lst.py independence_school_ontology.ttl -o independence.lst
"""

import argparse
import sys
from pathlib import Path
from rdflib import Graph, RDF, RDFS, Namespace
from rdflib.namespace import split_uri

NS = Namespace("http://example.org/independence-school#")

# 상위 클래스로 묶기 위한 매핑 (온톨로지의 subClassOf 계층을 .lst의
# 6개 표시 클래스로 축약한다. .lst는 노드 하나에 클래스 하나만 허용하므로,
# ColonialCollaborator만 별도 클래스로 분리해 시각적으로 구분되게 한다)
SCHOOL_TYPES = {"School", "MilitaryAcademy"}
ORG_TYPES = {"Organization", "IndependenceMovementGroup", "ReligiousOrganization",
             "ProvisionalGovernment"}
EVENT_TYPES = {"Event", "PoliticalMovement", "Incident", "Battle"}
PLACE_TYPES = {"Place"}
PERSON_TYPES = {"Person", "IndependenceActivist", "Educator", "Missionary"}
COLLAB_TYPE = "ColonialCollaborator"

# .lst 스펙상 유효한 값 (phase1-compatible/makegraph.py 기준)
CLASS_STYLE = {
    "School":       ("navy", "square"),
    "Organization": ("green", "box"),
    "Event":        ("orange", "star"),
    "Place":        ("gray", "circle"),
    "Person":       ("blue", "dot"),
    COLLAB_TYPE:    ("red", "triangle"),
}

# 온톨로지의 object property -> (.lst 관계명, 한글설명, 화살표유형)
RELATION_STYLE = {
    "foundedSchool":    ("설립", "arrow"),
    "taughtAt":         ("재직", "arrow"),
    "graduatedFrom":    ("졸업", "arrow"),
    "administeredSchool": ("경영", "arrow"),
    "memberOf":         ("소속", "arrow"),
    "foundedOrg":       ("창설", "arrow"),
    "participatedIn":   ("참여", "arrow"),
    "mentoredBy":       ("사사", "arrow"),
    "influencedBy":     ("영향받음", "arrow"),
    "establishedByOrg": ("설립근거", "arrow"),
    "modeledAfter":     ("모델", "arrow"),
    "acquiredBy":       ("인수됨", "arrow"),
    "locatedIn":        ("위치", "arrow"),
    "ledTo":            ("확대이어짐", "sequence"),
    "printedAt":        ("인쇄", "arrow"),
}


def local_name(uri) -> str:
    try:
        return split_uri(str(uri))[1]
    except Exception:
        return str(uri).rsplit("#", 1)[-1]


def classify(types: set) -> str:
    if COLLAB_TYPE in types:
        return COLLAB_TYPE
    if types & SCHOOL_TYPES:
        return "School"
    if types & ORG_TYPES:
        return "Organization"
    if types & EVENT_TYPES:
        return "Event"
    if types & PLACE_TYPES:
        return "Place"
    if types & PERSON_TYPES:
        return "Person"
    return "Organization"  # 안전한 기본값


def sanitize(text: str) -> str:
    # .lst는 홑따옴표 금지, 필드는 공백으로 분리되므로 라벨 내부 공백도 제거
    return text.replace("'", "").replace(" ", "").strip()


def convert(ttl_path: Path, title: str) -> str:
    g = Graph()
    g.parse(ttl_path, format="turtle")

    # 1) 개체별 rdf:type 수집 (owl:Class 자체는 제외)
    individual_types: dict[str, set] = {}
    for s, _, o in g.triples((None, RDF.type, None)):
        s_local = local_name(s)
        o_local = local_name(o)
        if o_local in ("Ontology", "Class", "ObjectProperty", "DatatypeProperty"):
            continue
        individual_types.setdefault(s_local, set()).add(o_local)

    nodes = {}  # id -> (class, label)
    for ind, types in individual_types.items():
        cls = classify(types)
        nodes[ind] = (cls, sanitize(ind))

    # 2) object property 사용 인스턴스 -> Links
    links = []
    relations_used = set()
    for prop_local in RELATION_STYLE:
        prop_uri = NS[prop_local]
        for s, _, o in g.triples((None, prop_uri, None)):
            s_local, o_local = local_name(s), local_name(o)
            if s_local in nodes and o_local in nodes:
                links.append((s_local, o_local, prop_local))
                relations_used.add(prop_local)

    # 3) .lst 조립
    lines = []
    lines.append("#Project")
    lines.append(f"h1 {sanitize(title)}")
    lines.append("")
    lines.append("#Class")
    for cls in CLASS_STYLE:
        color, shape = CLASS_STYLE[cls]
        lines.append(f"{cls} {color} {shape}")
    lines.append("")
    lines.append("#Relation")
    for rel in sorted(relations_used):
        desc, arrow = RELATION_STYLE[rel]
        lines.append(f"{rel} {desc} {arrow} 1")
    lines.append("")
    lines.append("#Nodes")
    for node_id, (cls, label) in nodes.items():
        lines.append(f"{node_id} {cls} {label}")
    lines.append("")
    lines.append("#Links")
    for s, o, rel in links:
        lines.append(f"{s} {o} {rel}")
    lines.append("")
    lines.append("#End")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="TTL -> MakeGraph2022 .lst 변환기")
    ap.add_argument("input", help="입력 .ttl 파일")
    ap.add_argument("-o", "--output", help="출력 .lst 파일 (기본: 입력명.lst)")
    ap.add_argument("--title", default="독립운동-근대학교 온톨로지",
                     help="#Project 제목")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output) if args.output else in_path.with_suffix(".lst")

    lst_text = convert(in_path, args.title)
    out_path.write_text(lst_text, encoding="utf-8")
    print(f"변환 완료: {out_path}")


if __name__ == "__main__":
    sys.exit(main())
