API_BASE_URL = "http://localhost:8000"


class ProjectConfig:
    '''프로젝트 환경을 셋팅'''
    def __init__(self):
        self.poc_env_info = {
            'desc' : "이수진의 프롬프트 관리를 위한 페이지입니다.",
            'dev_env':'Python3.9',
            'Front-end': 'Streamlit',
            'Back-end': 'FastAPI',
            'openai-llm-code': 'gpt-4o-mini, gpt-4o',
            'azure-llm-code':'gpt-4o-mini, gpt-4o'
        }
        self.page_desc = {
            "프롬프트 추가하기":"새로운 프롬프트 포멧을 생성하는 메뉴입니다.",
            "만들어둔 프롬프트 관리하기":"기존에 만들어 둔 프롬프트를 관리(수정, 삭제) 하는 페이지입니다.",
            "프롬프트 실행하기(LLM)":"프롬프트 포멧을 기반으로 LLM에게 명령어를 실행시키고, 그 결과를 받아볼 수 있는 페이지입니다. 결과 수정과 저장이 가능합니다.",
            "프롬프트 실행 결과 평가하기":"프롬프트 실행 결과를 평가하는 페이지입니다.",
        }
        self.dev_info_desc = {
            "상세 내용":"https://lsjsj92.tistory.com/679",
            "코드":"https://github.com/lsjsj92",
        }
        # 확장 가능한 모델 목록
        self.LLM_PROVIDERS = {
            "OpenAI": ["gpt-4o", "gpt-4o-mini"],
            "Azure OpenAI": ["gpt-4o-mini"]
        }
        
def load_config():
    return ProjectConfig()
