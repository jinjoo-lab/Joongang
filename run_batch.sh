#!/bin/bash

# 중앙일보 데이터 배치 수집 스크립트
# 매일 자정 이후 실행

# 프로젝트 디렉토리 설정 (현재 스크립트 위치 기준)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$PROJECT_DIR/bin"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
BATCH_SCRIPT="$BIN_DIR/batch_job.py"
LOG_DIR="$PROJECT_DIR/logs"

# 로그 파일 설정
DATE=$(date +"%Y%m%d")
LOG_FILE="$LOG_DIR/batch_$DATE.log"

# 로그 디렉토리 생성
mkdir -p "$LOG_DIR"

# 실행 시간 로그
echo "$(date): 배치 작업 시작" >> "$LOG_FILE"

# 프로젝트 디렉토리로 이동
cd "$PROJECT_DIR" || {
    echo "$(date): 프로젝트 디렉토리 이동 실패" >> "$LOG_FILE"
    exit 1
}

# 가상환경 Python으로 배치 스크립트 실행
"$VENV_PYTHON" "$BATCH_SCRIPT" >> "$LOG_FILE" 2>&1

# 실행 결과 확인
if [ $? -eq 0 ]; then
    echo "$(date): 배치 작업 성공" >> "$LOG_FILE"
    exit 0
else
    echo "$(date): 배치 작업 실패" >> "$LOG_FILE"
    exit 1
fi 