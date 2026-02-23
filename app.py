import random
import streamlit as st

# ============================================================
# 0. 게임 데이터 (나중에 채워 넣을 부분)
# ============================================================

# TODO: 실제 사용할 역할(캐릭터) 코드와 이름을 여기에 추가하세요.
ROLES = [
    {"code": "nietzsche", "name": "니체"},
    {"code": "han_byung_chul", "name": "한병철"},
    {"code": "performance_subject", "name": "성과사회의 성과주체"},
    {"code": "arendt", "name": "아렌트"},
    {"code": "bartleby", "name": "바틀비"},
]

# TODO: 실제 질문 카드 내용을 여기에 넣으세요. (6장 기준)
QUESTION_CARDS = [
    {"id": 1, "text": "질문 1 예시: 당신은 긍정성의 폭력에 시달린 적 있나요?"},
    {"id": 2, "text": "질문 2 예시: 당신에게 '성과'란 무엇인가요?"},
    {"id": 3, "text": "질문 3 예시: 당신은 휴식과 일을 어떻게 구분하나요?"},
    {"id": 4, "text": "질문 4 예시: 당신은 타자와의 관계를 어떻게 봅니까?"},
    {"id": 5, "text": "질문 5 예시: 당신에게 자유란 무엇인가요?"},
    {"id": 6, "text": "질문 6 예시: 당신이 피로를 느끼는 순간은 언제인가요?"},
]

# TODO: 역할별·질문별 답변을 여기에 채워 넣으세요.
# 구조 예시:
# ROLE_ANSWERS["nietzsche"][1]  -> 니체가 질문 1에 할 법한 답변
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
# 1. 헬퍼 함수들
# ============================================================

def get_role_name_by_code(code: str) -> str:
    """역할 코드로부터 표시용 이름을 찾아주는 함수"""
    for r in ROLES:
        if r["code"] == code:
            return r["name"]
    return code  # 못 찾으면 코드 그대로


def init_game_state():
    """새 게임 시작 시 session_state를 초기화"""
    # 두 플레이어에게 서로 다른 역할을 배정 (단순 랜덤 2개)
    chosen_roles = random.sample(ROLES, 2)
    player1_role = chosen_roles[0]["code"]
    player2_role = chosen_roles[1]["code"]

    st.session_state.page = 1
    st.session_state.player1_role = player1_role
    st.session_state.player2_role = player2_role

    # 이 앱은 한 화면에서 두 사람이 함께 본다고 가정.
    # 각자 어떤 역할인지 보여 줄 때 분리해서 안내할 수 있음.
    st.session_state.current_page = 1  # 1: 시작, 2: 질문/답변, 3: 정체 지목
    st.session_state.clicked_questions = []  # 이미 클릭한 질문 id 목록
    st.session_state.answer_log = []  # (질문id, 질문문구, 답변) 기록
    st.session_state.guess_input = ""
    st.session_state.result_message = ""


def ensure_state():
    """session_state에 필요한 값들이 없으면 기본값 세팅"""
    if "current_page" not in st.session_state:
        init_game_state()


# ============================================================
# 2. 페이지별 UI & 로직
# ============================================================

def render_page1():
    """페이지 1 - 게임 시작 페이지"""
    st.header("페이지 1: 피로사회 마피아 게임 시작")

    st.markdown(
        """
        - 플레이어 2명 (학생 1, 교사 1)이 함께 플레이합니다.  
        - '게임 시작' 버튼을 누르면, 시스템이 각 플레이어에게 **비밀 역할**을 무작위로 부여합니다.  
        - 목표: **질문 카드**를 활용해 상대방의 정체(역할)를 맞히는 것!
        """
    )

    if st.button("게임 시작"):
        init_game_state()
        st.session_state.current_page = 2
        st.experimental_rerun()

    with st.expander("디버그용 / 개발 단계에서는 역할 확인 (나중에 숨겨도 됨)"):
        st.write("Player1 역할 코드:", st.session_state.player1_role)
        st.write("Player2 역할 코드:", st.session_state.player2_role)


def render_page2():
    """페이지 2 - 역할 확인 + 질문 카드 화면"""
    st.header("페이지 2: 역할 확인 & 질문 카드")

    st.markdown(
        """
        1. 각 플레이어는 자신에게 부여된 역할을 **조용히** 확인합니다.  
        2. 오른쪽 질문 카드 중에서 **번갈아 가며** 하나씩 클릭합니다.  
        3. 카드가 클릭되면, “만약 상대방이 그 역할이라면 할 법한 답변”이 화면에 나타납니다.  
        4. 질문 카드가 다 사용되기 전에 상대방의 정체를 짐작할 수 있다면,  
           아래의 **'정체 지목' 버튼**을 눌러 다음 페이지로 이동합니다.
        """
    )

    # 좌/우 컬럼: 왼쪽은 역할 안내, 오른쪽은 질문 카드
    col_left, col_right = st.columns([1, 2])

    # -----------------------
    # 왼쪽: 플레이어 역할 안내
    # -----------------------
    with col_left:
        st.subheader("플레이어 역할 안내 (현실에서는 각자 따로 보기)")

        st.markdown("**Player 1 역할 (교사):**")
        st.info(get_role_name_by_code(st.session_state.player1_role))

        st.markdown("**Player 2 역할 (학생):**")
        st.info(get_role_name_by_code(st.session_state.player2_role))

        st.caption(
            "실제 플레이에서는 화면을 나눠 보거나, "
            "각자 자기 역할만 보고 상대방에게는 보여주지 않도록 진행하세요."
        )

    # -----------------------
    # 오른쪽: 질문 카드들
    # -----------------------
    with col_right:
        st.subheader("질문 카드")

        st.markdown("아래 6장의 질문 카드 중 하나를 선택해 클릭하세요.")

        # 3x2 레이아웃으로 카드 배치
        rows = [QUESTION_CARDS[:3], QUESTION_CARDS[3:]]

        for row in rows:
            cols = st.columns(3)
            for card, c in zip(row, cols):
                with c:
                    clicked = st.button(
                        f"카드 {card['id']}",
                        key=f"qcard_{card['id']}",
                    )
                    st.caption(card["text"])
                    if clicked:
                        handle_question_click(card["id"], card["text"])

        st.markdown("---")
        st.subheader("질문 & 답변 로그")

        if len(st.session_state.answer_log) == 0:
            st.write("아직 선택한 질문이 없습니다.")
        else:
            for i, (qid, qtext, answer) in enumerate(st.session_state.answer_log, start=1):
                st.markdown(f"**[{i}] 질문 {qid}:** {qtext}")
                st.write(f"→ 답변: {answer}")
                st.markdown("---")

        st.markdown("### 정체 지목으로 넘어가기")

        st.caption(
            "질문 카드가 모두 사용되기 전이라도, "
            "상대방의 역할을 어느 정도 짐작했다면 아래 버튼을 눌러보세요."
        )

        if st.button("정체 지목 페이지로 이동"):
            st.session_state.current_page = 3
            st.experimental_rerun()


def handle_question_click(question_id: int, question_text: str):
    """질문 카드 클릭 시 동작: 상대방 역할 기준 답변 제공"""
    # 여기서는 예시로 "Player1이 질문을 한다 → Player2 역할 기준으로 답변"
    # 실제 수업 상황에 맞게, 누가 질문자인지 룰을 더 세밀하게 정해도 됩니다.
    opponent_role_code = st.session_state.player2_role

    # 역할별·질문별 답변에서 텍스트 가져오기
    try:
        answer = ROLE_ANSWERS[opponent_role_code][question_id]
    except KeyError:
        answer = "[TODO] 이 역할/질문 조합에 대한 답변이 아직 정의되지 않았습니다."

    # 클릭한 질문 id 기록 (중복 클릭 체크용으로도 활용 가능)
    if question_id not in st.session_state.clicked_questions:
        st.session_state.clicked_questions.append(question_id)

    # 로그에 추가
    st.session_state.answer_log.append((question_id, question_text, answer))


def render_page3():
    """페이지 3 - 정체 지목 & 결과"""
    st.header("페이지 3: 상대방 정체 지목")

    st.markdown(
        """
        이제까지의 질문과 답변을 바탕으로,  
        **상대방의 정체(역할)가 누구라고 생각하는지** 적어보세요.
        """
    )

    st.markdown("#### 선택 가능한 역할 목록")
    role_names = [get_role_name_by_code(r["code"]) for r in ROLES]
    st.write(", ".join(role_names))

    st.markdown("---")

    # 텍스트 입력으로 추측 (학생/교사 중 실제로 입력할 사람을 정해서)
    guess = st.text_input(
        "상대방의 정체를 입력하세요 (예: 니체, 한병철, 성과사회의 성과주체 등)",
        value=st.session_state.get("guess_input", ""),
    )

    if st.button("정답 확인"):
        st.session_state.guess_input = guess

        # 실제 상대방 역할: 여기서는 예시로 Player2를 '상대방'으로 간주
        real_role_name = get_role_name_by_code(st.session_state.player2_role)

        if guess.strip() == real_role_name:
            st.session_state.result_message = f"정답입니다! 상대방의 정체는 **{real_role_name}** 이었습니다."
        else:
            st.session_state.result_message = (
                f"아쉽지만 오답입니다. "
                f"실제 상대방의 정체는 **{real_role_name}** 이었습니다."
            )

    if st.session_state.get("result_message"):
        st.success(st.session_state.result_message)

    st.markdown("---")
    if st.button("다시 시작하기"):
        init_game_state()
        st.session_state.current_page = 1
        st.experimental_rerun()


# ============================================================
# 3. 메인 실행부
# ============================================================

def main():
    st.title("피로사회 마피아 게임 (Streamlit 골격)")

    ensure_state()

    # 간단한 상단 네비게이션 (디버그/개발 편의용)
    page = st.session_state.current_page

    tabs = st.tabs(["페이지 1: 시작", "페이지 2: 질문 카드", "페이지 3: 정체 지목"])
    with tabs[0]:
        if page == 1:
            render_page1()
        else:
            st.caption("현재 게임 상태에서는 이 페이지는 시작 상태를 보여줍니다.")
            render_page1()

    with tabs[1]:
        if page == 2:
            render_page2()
        else:
            st.caption("정식 흐름에서는 '게임 시작'을 먼저 눌러 주세요.")
            render_page2()

    with tabs[2]:
        if page == 3:
            render_page3()
        else:
            st.caption("정식 흐름에서는 질문을 어느 정도 한 뒤에 넘어옵니다.")
            render_page3()


if __name__ == "__main__":
    main()

