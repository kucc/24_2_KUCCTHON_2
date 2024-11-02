# 베이스 이미지
FROM node:18

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 설치
COPY package.json package-lock.json ./
RUN npm install

# 애플리케이션 코드 복사
COPY . .

# 빌드
RUN npm run build

# 서버 실행 (예: serve 사용)
RUN npm install -g serve

# 포트 노출
EXPOSE 3000

# 애플리케이션 실행
CMD ["serve", "-s", "build", "-l", "3000"]
