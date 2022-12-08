# 주식 거래 API

## 설치

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

</br>

## ERD

<img src='/images/ERD.png'>

### CSV 로드
- stock/core/data 에 있는 csv 파일들을 로드합니다.
- apscheduler을 이용하여 하루에 한 번씩 업데이트 합니다.
- 로드할 때 account_number를 username으로, 비밀번호는 testpass로 유저를 생성합니다.

</br>

### User
- 이용자

| 내용       | Method | URL             |
| ---------- | ------ | --------------- |
| 회원가입   | POST   | api/user/create |
| Token 인증 | POST   | api/user/token  |

</br>

### 계좌(Account)
 - 조회
  ```
  [
    {
      "id": "id"
      "account_name": "계좌명"
      "bank_name": "은행"
      "account_number": "계좌번호"
      "assets": "계좌 총 자산"
    }
  ]
  ```
 - 상세
  ```
  {
    "id": "id",
    "account_name": "계좌명"
    "bank_name": "은행"
    "account_number": "계좌번호"
    "assets": "계좌 총 자산"
    "principal": "투자 원금",
    "total_earnings": "총 수익금",
    "earnings_rate": "수익률"
}

  ```

| 내용 | Method    | URL                             |
| ---- | --------- | ------------------------------- |
| 조회 | GET       | api/account/accounts            |
| 상세 | GET       | api/account/accounts/account_id |
| 변경 | PUT,PATCH | api/account/accounts/account_id |

</br>

### Invest(투자 종목)
- 조회
  ```
  [
    {
        "id": "id",
        "ISIN": "ISIN",
        "holding_name": "보유 종목명",
        "holding_type": "보유 종목의 자산군",
        "value": "평가 금액"
    }
  ]
  ```
  
| 내용 | Method | URL                |
| ---- | ------ | ------------------ |
| 조회 | GET    | api/invest/invests |

</br>

## 투자금 입금
### 1단계
 - 계좌번호, 고객명, 거래금액 순서로 hashing 하여 cache에 60초 동안 저장
 - 요청 데이터
    - 계좌번호
    - 고객명
    - 거래금액
 - 
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

| Method | URL                                           |
| ------ | --------------------------------------------- |
| POST   | api/account/accounts/account_id/deposit-valid |

### 2단계
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

| Method | URL                                     |
| ------ | --------------------------------------- |
| POST   | api/account/accounts/account_id/deposit |

</br>