#!/bin/bash
# Docker Compose 시작 및 테스트 스크립트

set -e

echo "================================"
echo "FastAPI Learning Project Setup"
echo "================================"
echo ""

# Docker 설치 확인
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되어 있지 않습니다."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되어 있지 않습니다."
    exit 1
fi

echo "✅ Docker 및 Docker Compose 설치 확인됨"
echo ""

# Docker 데몬 실행 확인
if ! docker ps &> /dev/null; then
    echo "❌ Docker 데몬이 실행 중이 아닙니다."
    exit 1
fi

echo "✅ Docker 데몬 실행 중"
echo ""

echo "================================"
echo "1단계: 이미지 빌드"
echo "================================"
docker-compose build

echo ""
echo "================================"
echo "2단계: 컨테이너 시작"
echo "================================"
docker-compose up -d

echo ""
echo "================================"
echo "3단계: 서비스 초기화 대기"
echo "================================"
sleep 5

echo ""
echo "================================"
echo "서비스 상태 확인"
echo "================================"
docker-compose ps

echo ""
echo "================================"
echo "✅ 설정 완료!"
echo "================================"
echo ""
echo "🌐 API 접속: http://localhost:8001"
echo "📚 Swagger UI: http://localhost:8001/docs"
echo "📖 ReDoc: http://localhost:8001/redoc"
echo "❤️  Health Check: http://localhost:8001/health"
echo ""
echo "📝 로그 확인:"
echo "   docker-compose logs -f app"
echo ""
echo "🛑 모든 서비스 중지:"
echo "   docker-compose down"
echo ""

