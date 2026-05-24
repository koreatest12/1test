---
name: "🛡️ 보안 감사 및 인프라 점검 요청"
about: "특정 패키지 취약점 조치, CodeQL 예외 처리 또는 OWASP 스캔 점검을 요청합니다."
title: "[SECURITY] "
labels: ["security", "needs-audit"]
assignees: ["sk"]
---

### 🎯 점검 대상 (Target)
- [ ] Python 백엔드 클러스터 (FastAPI 노드)
- [ ] Node.js 프론트엔드/BFF 환경
- [ ] CI/CD 파이프라인 (GitHub Actions / Docker)
- [ ] 기타: 

### 🚨 요청 사유 (Reason for Audit)
- (예: 특정 버전의 fastapi 패키지에 새로운 취약점이 발견되어 긴급 스캔 및 판올림이 필요함)

### 📊 CodeQL / Dependabot 로그 (Logs)
```text
(관련된 취약점 경고 로그나 에러 메시지를 복사해서 붙여넣어 주세요)
