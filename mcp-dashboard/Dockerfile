FROM node:20

WORKDIR /app
# package.json 복사
COPY package.json .
# 의존성 설치
RUN npm install
# 모든 파일 복사
COPY . .

EXPOSE 3000

# npm start 스크립트 실행
CMD ["npm", "start"]
