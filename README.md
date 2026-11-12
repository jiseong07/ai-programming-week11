# 성적 CSV 실습

## 무엇을 하나요 (What)

`load_scores.py`는 성적 CSV 파일을 읽어 유효한 이름과 점수는 보관하고,
잘못된 행은 줄 번호와 이유를 함께 기록합니다.

## 왜 만들었나요 (Why)

실제 CSV에는 빈 값, 범위를 벗어난 점수, 잘못된 형식, 중복 이름 등이
섞일 수 있습니다. 이 실습은 이런 입력에도 명세대로 동작하는지 테스트합니다.

## 어떻게 쓰나요 (How)

PowerShell에서 프로젝트 폴더를 연 뒤 가상환경과 필요한 패키지를 준비합니다.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe load_scores.py scores.csv
```

## 어떻게 테스트하나요

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pytest --cov=load_scores --cov-report=term-missing
```

VS Code에서는 **Terminal → Run Task**에서 `실습: 전체 테스트 실행`,
`실습: 커버리지 측정`, `실습: 성적 CSV 실행`을 선택할 수 있습니다.
테스트 탐색기에서도 pytest 테스트를 실행할 수 있습니다.

## 파일 구성

- `load_scores.py`: CSV 로더
- `scores.csv`, `empty.csv`, `weird.csv`: 테스트 입력
- `test_load_scores.py`: 정상·예외·경계값 테스트
- `test_ai_A.py`, `test_ai_B.py`: 코드 제공·명세 제공 방식의 테스트 초안
- `test_ai_C_버그.py`: 버그 코드 함정 실험용 테스트
- `bug3_logic.py`: 논리 버그 실습 예제
- `.vscode/`: Python 테스트와 실행 작업 설정

## 만든 사람 · AI 활용

- 만든 사람: 전지성 (2026100636)
- AI 활용: VS Code 실행 설정과 테스트 코드 초안 작성에 사용했습니다.
- Assisted-by: Copilot
