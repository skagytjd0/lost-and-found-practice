# 분실물 관리 서비스 - 코드 품질 실습용

STATUS_STORED = "보관 중"
STATUS_HANDED_OVER = "인도 완료"

items = []
NEXT_NO = 1


def RegisterItem(name, category, found_date, location, finder="", memo=""):
    global NEXT_NO
    if not name:
        return "물품명을 입력하세요"
    if not category:
        return "분류를 입력하세요"

    item = {
        "no": f"P{NEXT_NO}",
        "name": name,
        "category": category,
        "found_date": found_date,
        "location": location,
        "status": STATUS_STORED,
    }
    items.append(item)
    NEXT_NO += 1
    return item["no"]


def _format_item(item):
    return (
        f"{item['no']} {item['name']} [{item['category']}] "
        f"습득일 {item['found_date']} / 보관 장소 {item['location']}"
    )


def _is_stored_match(item, field, keyword):
    return item["status"] == STATUS_STORED and keyword in item[field]


def _search_items(field, keyword):
    result = [
        _format_item(item)
        for item in items
        if _is_stored_match(item, field, keyword)
    ]
    if not result:
        print("검색 결과가 없습니다. 학생지원팀에 문의하세요.")
    return result


def search_by_name(keyword):
    return _search_items("name", keyword)


def search_by_category(keyword):
    return _search_items("category", keyword)


def _find_item(item_no):
    for item in items:
        if item["no"] == item_no:
            return item
    return None


def _validate_item_status(item):
    status = item["status"]
    if status == STATUS_HANDED_OVER:
        return "이미 인도된 물품입니다"
    if status != STATUS_STORED:
        return "알 수 없는 상태입니다"
    return None


def _validate_handover_inputs(owner_checked, today, staff):
    if not owner_checked:
        return "주인 확인이 필요합니다"
    if not today:
        return "인도일을 입력하세요"
    if not staff:
        return "담당자를 입력하세요"
    return None


def _validate_handover(item, owner_checked, today, staff):
    status_error = _validate_item_status(item)
    if status_error:
        return status_error
    return _validate_handover_inputs(owner_checked, today, staff)


def handover(item_no, owner_checked, today, staff):
    if not item_no:
        return "물품 번호를 입력하세요"

    item = _find_item(item_no)
    if item is None:
        return "등록되지 않은 물품 번호입니다"

    error = _validate_handover(item, owner_checked, today, staff)
    if error:
        return error

    item["status"] = STATUS_HANDED_OVER
    item["handover_date"] = today
    item["staff"] = staff
    return STATUS_HANDED_OVER


def _count_status(target_status):
    return sum(1 for item in items if item["status"] == target_status)


def count_by_status():
    try:
        return {
            STATUS_STORED: _count_status(STATUS_STORED),
            STATUS_HANDED_OVER: _count_status(STATUS_HANDED_OVER),
        }
    except (KeyError, TypeError):
        return None


if __name__ == "__main__":
    RegisterItem("검정 우산", "기타", "2026-11-12", "학생지원팀 보관함", "학생A", "")
    print(search_by_name("우산"))
    print(handover("P1", True, "2026-11-19", "담당자A"))
    print(count_by_status())
