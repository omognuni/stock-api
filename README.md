# 주식 거래 API

### 설치
- git clone 후 다음 명령어 실행
```
docker-compose up --build
```
- 테스트 결과 확인
```
docker-compose run --rm store sh -c 'python manage.py test'
```
- 테스트 코드는 각 app 들의 tests 폴더 참조
  - stock/core/tests
  - stock/account/tests
  - stock/invest/tests
  - stock/user/tests

<img src='/images/test.PNG'>


### ERD
<img src='/images/ERD.png'>

### User
- 이용자

| 내용 | Method | URL |
|------|---|---------|
|회원가입|POST| api/user/create|
|Token 인증|POST| api/user/token|

### 계좌(Account)
 - 조회
   - 계좌명 (account_name)
   - 증권사(은행) (bank_name)
   - 계좌번호 (account_num)
   - 계좌 총 자산 (assets)
 - 상세
   - 계좌명 (account_name)
   - 증권사(은행) (bank_name)
   - 계좌번호 (account_num)
   - 계좌 총 자산 (assets)
   - 투자 원금 (principal)
   - 총 수익금 (total_earnings)
   - 수익률 (earnings_rate)

| Method | URL |
|---|------| 
|GET| api/account/accounts|
|PUT,PATCH| api/account/accounts/account_id|

### Invest(투자 종목)
- 조회
  - 보유 종목명 (holding_name)
  - 보유 종목의 자산군 (holding_type)
  - 보유 종목의 평가 금액(value)
  - 보유 종목의 ISIN (ISIN)
  
| Method | URL |
|--------|--------| 
|GET| api/invest/invests|

### 투자금 입금
##### 1단계
 - 계좌번호, 고객명, 거래금액 순서로 hashing 하여 cache에 60초 동안 저장
 - 요청 데이터
    - 계좌번호
    - 고객명
    - 거래금액
```
{
    "account_number": "123123",
    "username": "아이작",
    "transfer_amount": 1000
}
```
- 응답 데이터
  - 거래정보 식별자(계좌 id)
  - 실패 시 HTTP_406_NOT_ACCEPTABLE
```
{
    "transfer_id": 11
}
```

| Method | URL |
|--------|--------| 
|POST| api/account/accounts/account_id/deposit-valid|

##### 2단계
 - 요청 데이터
   - 1단계 요청 데이터 계좌번호, 고객명, 거래금액 순서로 hashing
   - cache에 가지고 있는 값과 비교하여 총 자산 업데이트
```
{
    "signature": "82b64b05dfe897e1c2bce88a62467c084d79365af1",
    "transfer_identifier": 11
}
```
- 응답 데이터
  - 입금 거래 결과
  - 실패 시 HTTP_400_BAD_REQUEST
```
{
    "status": true
}
```

| Method | URL |
|--------|--------| 
|POST| api/account/accounts/account_id/deposit|
  