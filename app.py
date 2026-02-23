import random
import streamlit as st

# ============================================================
# 0. 게임 데이터 (나중에 채워 넣을 부분)
# ============================================================

ROLES = [
    {"code": "nietzsche", "name": "니체"},
    {"code": "han_byung_chul", "name": "한병철"},
    {"code": "performance_subject", "name": "성과사회의 성과주체"},
  
]

QUESTION_CARDS = [
    {"id": 1, "text": "당신은 긍정성의 폭력에 시달린 적 있나요?"},
    {"id": 2, "text": "당신에게 '성과'란 무엇인가요?"},
    {"id": 3, "text": "당신은 휴식과 일을 어떻게 구분하나요?"},
    {"id": 4, "text": "당신은 타자와의 관계를 어떻게 봅니까?"},
    {"id": 5, "text": "당신에게 자유란 무엇인가요?"},
    {"id": 6, "text": "당신이 피로를 느끼는 순간은 언제인가요?"},
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
    }
}


# ============================================================
# 1. 유틸 & 상태 초기화
# ============================================================

def get_role_name_by_code(code: str) -> str:
    for r in ROLES:
        if r["code"] == code:
            return r["name"]
    return code


def init_session_state():
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "role_A_code" not in st.session_state:
        st.session_state.role_A_code = None
    if "role_B_code" not in st.session_state:
        st.session_state.role_B_code = None
    if "show_role" not in st.session_state:
        st.session_state.show_role = None  # "A", "B", 또는 None
    if "question_log" not in st.session_state:
        st.session_state.question_log = []  # (질문id, 질문문구, 답변, 질문자(A/B))
    if "revealed_questions" not in st.session_state:
        st.session_state.revealed_questions = []
    if "guess_A" not in st.session_state:
        st.session_state.guess_A = ""
    if "guess_B" not in st.session_state:
        st.session_state.guess_B = ""
    if "result_A" not in st.session_state:
        st.session_state.result_A = ""
    if "result_B" not in st.session_state:
        st.session_state.result_B = ""


def start_new_game():
    # 역할 2개 랜덤 배정
    chosen = random.sample(ROLES, 2)
    st.session_state.role_A_code = chosen[0]["code"]
    st.session_state.role_B_code = chosen[1]["code"]
    st.session_state.game_started = True

    # 상태 리셋
    st.session_state.show_role = None
    st.session_state.question_log = []
    st.session_state.guess_A = ""
    st.session_state.guess_B = ""
    st.session_state.result_A = ""
    st.session_state.result_B = ""


# ============================================================
# 2. 역할 확인 UI (A/B 번갈아 보기, 동시에 노출 X)
# ============================================================

def render_role_check_section():
    st.subheader("플레이어 역할 확인")

    st.markdown(
        """
        - **플레이어 A**, **플레이어 B**가 번갈아 화면을 보면서  
          아래 버튼을 눌러 자신의 역할을 확인합니다.  
        - 확인이 끝나면, 반드시 **'역할 가리기'** 버튼을 눌러 주세요.  
        - 두 역할이 동시에 화면에 보이지 않도록 합니다.
        """
    )

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### 플레이어 A")
        if st.button("플레이어 A 역할 확인"):
            st.session_state.show_role = "A"

    with colB:
        st.markdown("### 플레이어 B")
        if st.button("플레이어 B 역할 확인"):
            st.session_state.show_role = "B"

    st.markdown("---")

    # 한 번에 하나만 노출
    if st.session_state.show_role == "A":
        role_name = get_role_name_by_code(st.session_state.role_A_code)
        st.info(f"플레이어 A의 역할: **{role_name}**")
        if st.button("역할 가리기"):
            st.session_state.show_role = None
            st.rerun()

    elif st.session_state.show_role == "B":
        role_name = get_role_name_by_code(st.session_state.role_B_code)
        st.info(f"플레이어 B의 역할: **{role_name}**")
        if st.button("역할 가리기"):
            st.session_state.show_role = None
            st.rerun()

    else:
        st.caption("지금은 어떤 역할도 화면에 보이지 않습니다. 필요할 때만 버튼을 눌러 확인하세요.")


# ============================================================
# 3. 질문 카드 + 답변
# ============================================================

def handle_question_click(question_id: int, question_text: str, asker: str):
    """질문 카드 클릭 → 상대 역할 기준 답변 생성 후 로그에 기록."""
    if asker == "A":
        opponent_role_code = st.session_state.role_B_code
    else:
        opponent_role_code = st.session_state.role_A_code

    if opponent_role_code is None:
        answer = "상대방의 역할이 아직 정해지지 않았습니다."
    else:
        try:
            answer = ROLE_ANSWERS[opponent_role_code][question_id]
        except KeyError:
            answer = "[TODO] 이 역할/질문 조합에 대한 답변이 아직 정의되지 않았습니다."

    st.session_state.question_log.append(
        (question_id, question_text, answer, asker)
    )
    st.rerun()


def render_question_section():
    st.subheader("질문 카드")

    st.markdown(
        """
        1. **지금 질문하는 사람**을 선택합니다.  
        2. 질문 카드를 클릭하면,  
           → 상대방이 그 역할이라면 할 법한 답변이 로그에 기록됩니다.  
        3. 플레이어 A와 B가 번갈아 가며 질문해도 좋습니다.
        """
    )

    asker_label = st.radio(
        "지금 질문하는 플레이어를 선택하세요:",
        options=["플레이어 A", "플레이어 B"],
        index=0,
        horizontal=True,
        key="asker_radio",
    )
    asker = "A" if asker_label == "플레이어 A" else "B"

    st.markdown("#### 질문 카드 목록")

    rows = [QUESTION_CARDS[:3], QUESTION_CARDS[3:]]
    for row in rows:
        cols = st.columns(3)
        for card, c in zip(row, cols):
            with c:
                 if st.button(f"카드 {card['id']}", key=f"qcard_{card['id']}"):
                    handle_question_click(card["id"], card["text"], asker)
                    if card["id"] not in st.session_state.revealed_questions:
                        st.session_state.revealed_questions.append(card["id"])
                        st.rerun()

                # 이 카드를 한 번이라도 클릭했다면 그때부터 질문 문장 보여주기
                if card["id"] in st.session_state.revealed_questions:
                    st.caption(card["text"])
                else:
                    # 아직 안 클릭한 카드는 질문 문장 숨김
                    st.caption("질문 숨김")

    st.markdown("---")
    st.subheader("질문 & 답변 기록")

    if not st.session_state.question_log:
        st.write("아직 질문이 없습니다.")
    else:
        for i, (qid, qtext, answer, asker) in enumerate(st.session_state.question_log, start=1):
            who = "플레이어 A" if asker == "A" else "플레이어 B"
            st.markdown(f"**[{i}] {who}의 질문 (카드 {qid})**")
            st.write(f"질문: {qtext}")
            st.write(f"→ 답변: {answer}")
            st.markdown("---")


# ============================================================
# 4. 정체 지목
# ============================================================

def render_guess_section():
    st.subheader("정체 지목")

    st.markdown(
        """
        각 플레이어는 아래에서 **상대방의 정체**를 추리할 수 있습니다.  
        (플레이어 A → B의 역할을, 플레이어 B → A의 역할을 추리)
        """
    )

    role_names = [get_role_name_by_code(r["code"]) for r in ROLES]
    st.markdown("선택 가능한 역할: " + ", ".join(role_names))
    st.markdown("---")

    colA, colB = st.columns(2)

    # 플레이어 A가 B의 정체 추리
    with colA:
        st.markdown("### 플레이어 A의 추리 (상대: B)")
        guess_A = st.text_input(
            "플레이어 A가 생각하는 B의 정체:",
            value=st.session_state.guess_A,
            key="guess_input_A",
        )
        if st.button("플레이어 A: 정답 확인"):
            st.session_state.guess_A = guess_A
            real_B = get_role_name_by_code(st.session_state.role_B_code) if st.session_state.role_B_code else "알 수 없음"
            if guess_A.strip() == real_B:
                st.session_state.result_A = f"정답! 플레이어 B의 정체는 **{real_B}** 입니다."
            else:
                st.session_state.result_A = f"오답. 실제 플레이어 B의 정체는 **{real_B}** 입니다."
        if st.session_state.result_A:
            st.success(st.session_state.result_A)

    # 플레이어 B가 A의 정체 추리
    with colB:
        st.markdown("### 플레이어 B의 추리 (상대: A)")
        guess_B = st.text_input(
            "플레이어 B가 생각하는 A의 정체:",
            value=st.session_state.guess_B,
            key="guess_input_B",
        )
        if st.button("플레이어 B: 정답 확인"):
            st.session_state.guess_B = guess_B
            real_A = get_role_name_by_code(st.session_state.role_A_code) if st.session_state.role_A_code else "알 수 없음"
            if guess_B.strip() == real_A:
                st.session_state.result_B = f"정답! 플레이어 A의 정체는 **{real_A}** 입니다."
            else:
                st.session_state.result_B = f"오답. 실제 플레이어 A의 정체는 **{real_A}** 입니다."
        if st.session_state.result_B:
            st.success(st.session_state.result_B)


# ============================================================
# 5. 메인 실행부
# ============================================================

def main():
    st.title("피로사회 마피아 게임")
    init_session_state()

   

    st.markdown("---")

    # 게임 시작 / 다시 시작
    if not st.session_state.game_started:
        if st.button("게임 시작"):
            start_new_game()
            st.rerun()
    else:
        if st.button("다시 시작하기"):
            start_new_game()
            st.rerun()

    if not st.session_state.game_started:
        st.info("게임을 시작하려면 '게임 시작' 버튼을 눌러 주세요.")
        return

    # 역할 확인
    render_role_check_section()
    st.markdown("---")

    # 질문 카드
    render_question_section()
    st.markdown("---")

    # 정체 지목
    render_guess_section()


if __name__ == "__main__":
    main()
