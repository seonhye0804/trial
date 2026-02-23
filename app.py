import random
import string
import streamlit as st

# ============================================================
# 0. 게임 데이터 (나중에 채워 넣을 부분)
# ============================================================

ROLES = [
    {"code": "nietzsche", "name": "니체"},
    {"code": "han_byung_chul", "name": "한병철"},
    {"code": "performance_subject", "name": "성과사회의 성과주체"},
    {"code": "arendt", "name": "아렌트"},
    {"code": "bartleby", "name": "바틀비"},
]

QUESTION_CARDS = [
    {"id": 1, "text": "질문 1 예시: 당신은 긍정성의 폭력에 시달린 적 있나요?"},
    {"id": 2, "text": "질문 2 예시: 당신에게 '성과'란 무엇인가요?"},
    {"id": 3, "text": "질문 3 예시: 당신은 휴식과 일을 어떻게 구분하나요?"},
    {"id": 4, "text": "질문 4 예시: 당신은 타자와의 관계를 어떻게 봅니까?"},
    {"id": 5, "text": "질문 5 예시: 당신에게 자유란 무엇인가요?"},
    {"id": 6, "text": "질문 6 예시: 당신이 피로를 느끼는 순간은 언제인가요?"},
]

ROLE_ANSWERS = {
    "nietzsche": {
        1: "[니체] 답변 예시 (질문 1) - TODO: 실제 내용 채우기",
        2: "[니체] 답변 예시 (질문 2) - TODO",
        3: "[니체] 답변 예시 (질문 3) - TODO",
        4: "[니체] 답변 예시 (질문 4) - TODO",
        5: "[니체] 답변 예시 (질문 5) - TODO",
        6: "[니체] 답변 예시 (질문 6) - TODO",
    },
    "han_byung_chul": {
        1: "[한병철] 답변 예시 (질문 1) - TODO",
        2: "[한병철] 답변 예시 (질문 2) - TODO",
        3: "[한병철] 답변 예시 (질문 3) - TODO",
        4: "[한병철] 답변 예시 (질문 4) - TODO",
        5: "[한병철] 답변 예시 (질문 5) - TODO",
        6: "[한병철] 답변 예시 (질문 6) - TODO",
    },
    "performance_subject": {
        1: "[성과주체] 답변 예시 (질문 1) - TODO",
        2: "[성과주체] 답변 예시 (질문 2) - TODO",
        3: "[성과주체] 답변 예시 (질문 3) - TODO",
        4: "[성과주체] 답변 예시 (질문 4) - TODO",
        5: "[성과주체] 답변 예시 (질문 5) - TODO",
        6: "[성과주체] 답변 예시 (질문 6) - TODO",
    },
    "arendt": {
        1: "[아렌트] 답변 예시 (질문 1) - TODO",
        2: "[아렌트] 답변 예시 (질문 2) - TODO",
        3: "[아렌트] 답변 예시 (질문 3) - TODO",
        4: "[아렌트] 답변 예시 (질문 4) - TODO",
        5: "[아렌트] 답변 예시 (질문 5) - TODO",
        6: "[아렌트] 답변 예시 (질문 6) - TODO",
    },
    "bartleby": {
        1: "[바틀비] 답변 예시 (질문 1) - TODO",
        2: "[바틀비] 답변 예시 (질문 2) - TODO",
        3: "[바틀비] 답변 예시 (질문 3) - TODO",
        4: "[바틀비] 답변 예시 (질문 4) - TODO",
        5: "[바틀비] 답변 예시 (질문 5) - TODO",
        6: "[바틀비] 답변 예시 (질문 6) - TODO",
    },
}


# ============================================================
# 1. 앱 전체에서 공유되는 "방 정보" 저장소 (모든 세션 공유)
# ============================================================

@st.singleton
def get_rooms():
    """
    앱 전체에서 공유하는 방(room) 딕셔너리.
    여러 브라우저(세션)가 같은 room_code로 접속하면
    이 딕셔너리를 통해 서로 상태를 공유한다.
    """
    return {}  # {room_code: room_state_dict}


# ============================================================
# 2. 유틸 함수들
# ============================================================

def generate_player_id(n=8):
    """각 브라우저 세션을 구분하기 위한 간단한 랜덤 ID"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def get_role_name_by_code(code: str) -> str:
    for r in ROLES:
        if r["code"] == code:
            return r["name"]
    return code


def init_session_state():
    """각 세션(브라우저)에서 한 번만 초기화"""
    if "player_id" not in st.session_state:
        st.session_state.player_id = generate_player_id()
    if "room_code" not in st.session_state:
        st.session_state.room_code = ""
    if "player_name" not in st.session_state:
        st.session_state.player_name = ""
    if "joined" not in st.session_state:
        st.session_state.joined = False
    if "my_role_code" not in st.session_state:
        st.session_state.my_role_code = None
    if "guess_input" not in st.session_state:
        st.session_state.guess_input = ""
    if "result_message" not in st.session_state:
        st.session_state.result_message = ""


def get_or_create_room(room_code: str):
    """room_code에 해당하는 방 상태를 가져오거나 새로 만든다."""
    rooms = get_rooms()
    if room_code not in rooms:
        rooms[room_code] = {
            "players": {},       # player_id -> {"name": str, "role_code": None}
            "started": False,
            "question_log": [],  # [(question_id, question_text, answer, answered_by_player_id)]
        }
    return rooms[room_code]


def assign_roles_for_room(room):
    """해당 방에 등록된 2명의 플레이어에게 역할을 랜덤 배정"""
    player_ids = list(room["players"].keys())
    if len(player_ids) != 2:
        return  # 2명 아닐 때는 배정 안 함

    role_codes = [r["code"] for r in ROLES]
    random.shuffle(role_codes)
    chosen_roles = role_codes[:2]

    room["players"][player_ids[0]]["role_code"] = chosen_roles[0]
    room["players"][player_ids[1]]["role_code"] = chosen_roles[1]
    room["started"] = True


def get_opponent_role_code(room, my_player_id):
    """상대방의 역할 코드 반환 (없으면 None)"""
    for pid, info in room["players"].items():
        if pid != my_player_id:
            return info.get("role_code")
    return None


# ============================================================
# 3. UI: 방 접속 & 게임 시작
# ============================================================

def render_lobby():
    st.header("피로사회 마피아 게임")

    st.markdown(
        """
        1. 두 플레이어가 **같은 방 코드**와 **각자의 이름**을 입력합니다.  
        2. 두 사람이 모두 접속하면, '게임 시작' 버튼이 활성화됩니다.  
        3. 게임이 시작되면, 각자 **자신의 역할만** 볼 수 있습니다.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        room_code = st.text_input(
            "방 코드 (예: class1, 1234 등)",
            value=st.session_state.room_code,
            max_chars=20,
        )
        player_name = st.text_input(
            "당신의 이름 또는 닉네임",
            value=st.session_state.player_name,
            max_chars=20,
        )

        if st.button("방 접속 / 만들기"):
            if not room_code.strip() or not player_name.strip():
                st.warning("방 코드와 이름을 모두 입력하세요.")
            else:
                st.session_state.room_code = room_code.strip()
                st.session_state.player_name = player_name.strip()
                room = get_or_create_room(st.session_state.room_code)

                # 플레이어 등록 (최대 2명)
                if st.session_state.player_id not in room["players"]:
                    if len(room["players"]) >= 2:
                        st.error("이 방에는 이미 2명이 접속해 있습니다. 다른 방 코드를 사용하세요.")
                    else:
                        room["players"][st.session_state.player_id] = {
                            "name": st.session_state.player_name,
                            "role_code": None,
                        }
                        st.session_state.joined = True
                        st.session_state.my_role_code = None
                        st.success("방에 접속했습니다. 상대방이 들어오기를 기다리세요.")
                        st.rerun()
                else:
                    # 이미 이 세션이 등록되어 있는 경우
                    st.session_state.joined = True
                    st.success("이미 이 방에 접속해 있습니다.")
                    st.rerun()

    with col2:
        # 현재 방 상태 표시
        if st.session_state.room_code:
            room = get_or_create_room(st.session_state.room_code)
            st.subheader(f"현재 방: {st.session_state.room_code}")
            if room["players"]:
                st.write("접속한 플레이어:")
                for info in room["players"].values():
                    st.write(f"- {info['name']}")
            else:
                st.write("아직 접속한 플레이어가 없습니다.")

            # 게임 시작 버튼 (2명 모두 들어왔을 때만)
            if len(room["players"]) < 2:
                st.info("두 명이 모두 접속하면 게임을 시작할 수 있습니다.")
            else:
                if not room["started"]:
                    if st.button("게임 시작"):
                        assign_roles_for_room(room)
                        # 내 역할 코드 세션에 반영
                        st.session_state.my_role_code = room["players"][st.session_state.player_id]["role_code"]
                        st.success("게임이 시작되었습니다!")
                        st.rerun()
                else:
                    st.success("게임이 이미 시작되었습니다.")

    # 방에 정상 접속한 상태이고, 게임도 시작되었다면 메인 게임 화면으로
    if st.session_state.joined and st.session_state.room_code:
        room = get_or_create_room(st.session_state.room_code)
        if room["started"]:
            # 내 역할 코드 동기화
            my_info = room["players"].get(st.session_state.player_id)
            if my_info:
                st.session_state.my_role_code = my_info.get("role_code")
            st.markdown("---")
            render_game(room)


# ============================================================
# 4. UI: 메인 게임 화면 (질문 카드 + 정체 지목)
# ============================================================

def render_game(room):
    # 페이지 2+3을 합친 메인 플레이 화면
    st.subheader("당신의 비밀 역할")

    if st.session_state.my_role_code is None:
        st.warning("아직 역할이 배정되지 않았습니다. 상대방과 함께 '게임 시작'을 눌러주세요.")
        return

    my_role_name = get_role_name_by_code(st.session_state.my_role_code)
    st.info(f"당신의 역할: **{my_role_name}**")

    st.markdown(
        """
        - 이 역할은 **당신만** 알고 있어야 합니다.  
        - 질문 카드를 활용해, 상대방의 정체가 누구인지 추리해 보세요.
        """
    )

    st.markdown("---")
    st.subheader("질문 카드")

    st.markdown("질문 카드를 클릭하면, **상대방이 그 역할이라면 할 법한 답변**이 나타납니다.")

    # 질문 카드 배치 (3x2)
    rows = [QUESTION_CARDS[:3], QUESTION_CARDS[3:]]

    for row in rows:
        cols = st.columns(3)
        for card, c in zip(row, cols):
            with c:
                if st.button(f"카드 {card['id']}", key=f"qcard_{card['id']}"):
                    handle_question_click(room, card["id"], card["text"])
                st.caption(card["text"])

    st.markdown("---")
    st.subheader("질문 & 답변 기록")

    if not room["question_log"]:
        st.write("아직 질문이 없습니다.")
    else:
        for i, (qid, qtext, answer, pid) in enumerate(room["question_log"], start=1):
            # 누가 질문했는지는 필요 없으면 표시 안 해도 됨
            st.markdown(f"**[{i}] 질문 {qid}:** {qtext}")
            st.write(f"→ 답변: {answer}")
            st.markdown("---")

    st.markdown("---")
    render_guess_section(room)


def handle_question_click(room, question_id: int, question_text: str):
    """질문 카드 클릭 시, 상대방 역할 기준 답변 생성"""
    opponent_role_code = get_opponent_role_code(room, st.session_state.player_id)

    if opponent_role_code is None:
        answer = "상대방의 역할이 아직 정해지지 않았습니다."
    else:
        try:
            answer = ROLE_ANSWERS[opponent_role_code][question_id]
        except KeyError:
            answer = "[TODO] 이 역할/질문 조합에 대한 답변이 아직 정의되지 않았습니다."

    # 방 전체에 공유되는 질문/답변 로그에 추가
    room["question_log"].append(
        (question_id, question_text, answer, st.session_state.player_id)
    )
    st.rerun()


def render_guess_section(room):
    st.subheader("상대방 정체 지목")

    st.markdown(
        """
        지금까지의 질문과 답변을 바탕으로,  
        **상대방의 역할이 누구라고 생각하는지** 입력해 보세요.
        """
    )

    st.markdown("선택 가능한 역할:")
    role_names = [get_role_name_by_code(r["code"]) for r in ROLES]
    st.write(", ".join(role_names))

    guess = st.text_input(
        "상대방의 정체를 입력하세요 (예: 니체, 한병철, 성과사회의 성과주체 등)",
        value=st.session_state.guess_input,
    )

    if st.button("정답 확인"):
        st.session_state.guess_input = guess

        opponent_role_code = get_opponent_role_code(room, st.session_state.player_id)
        if opponent_role_code is None:
            st.session_state.result_message = "상대방의 역할이 아직 정해지지 않았습니다."
        else:
            real_role_name = get_role_name_by_code(opponent_role_code)
            if guess.strip() == real_role_name:
                st.session_state.result_message = f"정답입니다! 상대방의 정체는 **{real_role_name}** 이었습니다."
            else:
                st.session_state.result_message = (
                    f"아쉽지만 오답입니다. 실제 상대방의 정체는 **{real_role_name}** 이었습니다."
                )

    if st.session_state.result_message:
        st.success(st.session_state.result_message)


# ============================================================
# 5. 메인 실행부
# ============================================================

def main():
    init_session_state()
    render_lobby()


if __name__ == "__main__":
    main()
