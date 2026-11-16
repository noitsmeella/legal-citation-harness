# legal-citation-harness

**판례 인용 오귀속 진단 벤치마크와 구조 인식형 검증기**

> 2026-2 알파프로젝트Ⅶ (학생설계형 · 개인) · 안지오 (법학부 공법학전공) · 지도교수 신홍균

LLMs often answer from a court judgment yet attribute a party's allegation, a lower court's ruling, a cited precedent, or a dissent to the court's own holding. This repository (A) measures that misattribution with a discourse-role-annotated benchmark of Korean and U.S. criminal judgments, (B) builds a structure-aware verifier that flags misattributed legal claims, and (C) specifies the interface for plugging the verifier into an online law course.

---

## 무엇을 하는가

| 층 | 내용 | 상태 |
|---|---|---|
| **A. 진단 벤치마크** | 담화 역할이 표시된 한·미 형사 판결문, 함정 문항, 모델 평가 하니스 | 진행 중 |
| **B. 검증기** | 강의록의 주장 한 문장과 판결문을 받아 오귀속 여부를 판정 | 설계 중 |
| **C. 연동 인터페이스** | `verify()` 입출력 규격, 강의록 인용 오프라인 시연 | 예정 |

핵심 질문은 하나다. **AI는 문서에 답이 있어도, 그것이 누구의 말인지 헷갈려서 틀리는가? 그리고 그 오류를 판결문의 구조 정보로 잡아낼 수 있는가?**

### 연구 질문

- **RQ1** 근거 문서를 주어도 모델은 출처를 잘못 귀속하는가?
- **RQ2** 어떤 담화 역할(당사자 주장, 원심, 인용, 반대의견)이 오류를 가장 많이 유발하는가?
- **RQ3** 방해 문장, 문서 길이, 근거 위치가 오류율을 바꾸는가?
- **RQ4** 모델 간 오류 패턴은 정답률 순위와 일치하는가?
- **RQ5** 정답률만으로는 신뢰성을 과대평가하는가? (답은 맞고 근거는 틀린 비율)
- **RQ6** 한국과 미국 판결문에서 오류 프로파일이 다른가?
- **RQ7** 역할 정보를 쓰는 검증기가 단순 근거 확인보다 오귀속을 더 잘 잡는가?

## 저장소 구조

```
legal-citation-harness/
├─ src/harness/          # 직접 구현하는 코드 (처음엔 비어 있음)
│  ├─ segment.py         # 판결문 문장 분할, 번호 부여
│  ├─ schema.py          # 문항·응답 형식 검증
│  ├─ build_context.py   # 조건별 지문과 프롬프트 구성
│  ├─ llm.py             # 모델 호출, 캐시, 로그
│  ├─ score.py           # 자동 채점
│  ├─ run_eval.py        # [A] 평가 실행
│  ├─ role_tagger.py     # [B] 문장 역할 자동 분류
│  ├─ verifier.py        # [B] 주장 검증
│  ├─ eval_verifier.py   # [B] 검증기 평가
│  └─ cli.py             # [C] 시연용 실행
├─ tests/                # 동작 명세 = 테스트. 구현하면 통과해야 한다
├─ data/                 # 판결문, 분할 결과, 문항, 주장 쌍
├─ docs/                 # 개요, 코드북, 설계서, 연동 명세
├─ notes/                # 리딩 메모, 활동일지
├─ analysis/             # 통계 분석
├─ runs/                 # 모델 응답 로그 (캐시는 git 제외)
└─ report/               # 보고서
```

## 시작하기

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # API 키는 .env에만. 절대 커밋하지 말 것
pytest
```

처음에는 **모든 테스트가 실패한다** (`NotImplementedError`). 아래 순서로 모듈을 하나씩 구현해서 테스트를 초록색으로 바꾸는 방식으로 개발한다.

```bash
pytest tests/test_segment.py -v    # 한 모듈씩 확인
```

## 개발 순서

| 순서 | 모듈 | 테스트 | 층 |
|---|---|---|---|
| 1 | `segment.py` | `test_segment.py` | A |
| 2 | `schema.py` | `test_schema.py` | A |
| 3 | `build_context.py` | `test_build_context.py` | A |
| 4 | `score.py` | `test_score.py` | A |
| 5 | `llm.py` | `test_llm.py` | A |
| 6 | `run_eval.py` | (실행으로 확인) | A |
| 7 | `role_tagger.py` | `test_role_tagger.py` | B |
| 8 | `verifier.py` | `test_verifier.py` | B |
| 9 | `eval_verifier.py`, `cli.py` | (실행으로 확인) | B, C |

## 데이터

- 한국: 대법원 형사 판결 (국가법령정보센터, 대법원 종합법률정보)
- 미국: 연방항소법원 형사 판결 (CourtListener)
- 모든 판결의 출처 URL과 선고일은 `data/cases.csv`에 기록한다.
- `tests/fixtures/`의 판결문은 테스트용으로 만든 **가상 판결문**이며 실제 사건이 아니다.

형식은 [`data/README.md`](data/README.md), 역할 정의는 [`docs/codebook.md`](docs/codebook.md)를 본다.

## AI 사용 내역

저장소 골격(폴더 구조, 함수 이름과 설명, 테스트 명세, 문서 양식)은 Claude의 도움을 받아 만들었다. `src/harness/`의 구현, 판결문 선정과 역할 주석, 문항 작성, 분석과 보고서는 직접 수행한다. 이후 AI 도움을 받은 부분은 커밋 메시지와 이 절에 기록한다.

## 라이선스

미정. 코드는 MIT, 데이터 주석은 CC BY 4.0을 검토 중이다.
