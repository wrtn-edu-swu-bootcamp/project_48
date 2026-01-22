"""
AI 프롬프트 템플릿
"""

# 시스템 프롬프트 - 챗봇의 역할과 규칙 정의
SYSTEM_PROMPT = """당신은 서울여자대학교 신입생 도우미 AI입니다.

**당신의 역할:**
- 신입생이 학사 일정, 공지사항, 지원 프로그램을 쉽게 이해하도록 돕습니다
- 복잡한 행정·학사 용어를 쉬운 말로 풀어 설명합니다
- 정보 제공에 그치지 않고 구체적인 행동 가이드를 제공합니다

**톤앤매너:**
- 친절하고 차분한 톤 사용
- 선배가 설명해주는 느낌으로 작성
- 불필요한 정보는 줄이고 핵심만 전달
- 과도하게 긴 답변은 지양

**답변 가이드라인:**
- 질문에 대한 핵심 답변을 먼저 제공하세요
- 필요한 경우 구체적인 설명과 예시를 추가하세요
- 실행 가능한 다음 단계나 행동 가이드를 제시하세요
- 사용한 정보의 출처를 자연스럽게 언급하세요
- 질문의 맥락과 의도를 고려하여 가장 유용한 방식으로 답변하세요

**중요 규칙:**
1. 제공된 정보만 사용하세요. 추측하지 마세요.
2. 모르는 내용은 "해당 내용은 현재 제공된 정보에서 확인되지 않아요. 학교 행정실이나 학과 사무실에 직접 문의해보시는 것을 권장드려요."라고 답변하세요.
3. 학교·제도 관련 판단이나 개인적 조언은 하지 마세요.
4. 항상 출처를 명시하세요.
"""

# RAG 프롬프트 - 검색된 문서 기반 답변 생성
RAG_PROMPT_TEMPLATE = """다음 정보를 바탕으로 질문에 답변하세요.

{context}

질문: {question}

**답변 작성 지침:**
1. 제공된 정보만 사용하세요
2. 위 질문의 핵심 의도를 정확히 파악하세요
3. 검색된 문서의 관련성을 고려하여 가장 적절한 정보를 선택하세요
4. 질문에 맞는 자연스럽고 유용한 방식으로 답변하세요
5. 구체적인 날짜, 방법, 절차를 포함하세요
6. 출처는 [문서 번호]에서 제공된 출처를 자연스럽게 언급하세요
"""

# 명확화 프롬프트 - 모호한 질문 처리
CLARIFICATION_PROMPT = """사용자의 질문이 모호합니다. 다음 중 어떤 것에 대해 알고 싶으신가요?

{options}

궁금하신 항목을 선택하거나, 질문을 다시 작성해주세요."""

# 폴백 프롬프트 - 정보 없을 때
FALLBACK_PROMPT = """죄송해요. 해당 내용은 현재 제공된 정보에서 확인되지 않아요.

**다른 방법:**
- 학교 행정실에 직접 문의: [연락처]
- 학과 사무실에 문의
- 학생성장지원시스템 확인
- 인간 상담원 연결 (아래 버튼 클릭)

다른 궁금하신 점이 있으신가요?"""


def format_context(context_items: list) -> str:
    """
    컨텍스트 아이템들을 포맷팅
    
    Args:
        context_items: 컨텍스트 리스트
        
    Returns:
        포맷팅된 컨텍스트 문자열
    """
    formatted = ""
    
    for idx, item in enumerate(context_items, 1):
        formatted += f"[문서 {idx}]\n"
        formatted += f"출처: {item.get('source', '알 수 없음')}\n"
        
        # 제목/이름
        if 'title' in item:
            formatted += f"제목: {item['title']}\n"
        elif 'name' in item:
            formatted += f"이름: {item['name']}\n"
        elif 'term' in item:
            formatted += f"용어: {item['term']}\n"
        
        # 내용/설명
        if 'content' in item:
            formatted += f"내용: {item['content']}\n"
        elif 'description' in item:
            formatted += f"설명: {item['description']}\n"
        elif 'definition' in item:
            formatted += f"정의: {item['definition']}\n"
        
        # 추가 정보
        if 'start_date' in item and item['start_date']:
            formatted += f"시작일: {item['start_date']}\n"
        if 'end_date' in item and item['end_date']:
            formatted += f"종료일: {item['end_date']}\n"
        if 'application_method' in item:
            formatted += f"신청 방법: {item['application_method']}\n"
        if 'examples' in item:
            formatted += f"예시: {item['examples']}\n"
        
        formatted += "\n"
    
    return formatted


def create_rag_prompt(question: str, context_items: list) -> str:
    """
    RAG 프롬프트 생성
    
    Args:
        question: 사용자 질문
        context_items: 컨텍스트 아이템 리스트
        
    Returns:
        완성된 RAG 프롬프트
    """
    context = format_context(context_items)
    return RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )


def create_clarification_prompt(options: list) -> str:
    """
    명확화 프롬프트 생성
    
    Args:
        options: 선택지 리스트
        
    Returns:
        완성된 명확화 프롬프트
    """
    options_text = "\n".join([f"- {opt}" for opt in options])
    return CLARIFICATION_PROMPT.format(options=options_text)
