# User Signup Endpoint (`POST /api/v1/signup/user`)

## 1. Overview
The **User Signup Endpoint** provides complete user onboarding and account registration for the Sofia platform. It extracts client telemetry headers (`X-Forwarded-For`, `User-Agent`, `X-Device-Id`), validates registration payloads (`SignupUserRequest`), enforces terms acceptance and active terms version verification, checks email uniqueness, validates password complexity rules, hashes passwords with bcrypt, and persists the user (`member.user`), legal agreement (`signup.user_agreements`), and client device (`member.device`) in PostgreSQL.

---

## 2. Architecture & Sequence Diagram

The following Mermaid sequence diagram details the end-to-end request lifecycle across FastAPI validation, header extraction, dependency-injected repositories, password encryption, PostgreSQL persistence, and error handling:

```mermaid
sequenceDiagram
    autonumber
    actor Client
    box Application Layer
        participant App as FastAPI App
        participant Controller as SignupController
        participant Service as SignupService
        participant Validator as SignupUserValidator
        participant Crypto as Encryption
        participant Handler as ServerExceptionHandler
    end
    box Infrastructure Layer
        participant SessionMgr as SessionManager
        participant UserRepo as UserRepository
        participant UserDetailsRepo as UserDetailsRepository
        participant TermsRepo as TermsRepository
        participant AgreeRepo as UserAgreementsRepository
        participant DeviceRepo as DeviceRepository
        participant DB as PostgreSQL (accounts)
    end

    Client ->> App: POST /api/v1/signup/user (Headers + SignupUserRequest)
    activate App
    App ->> App: Validate SignupUserRequest via Pydantic (inc. PastDate born_date)

    alt Invalid Request Schema (422)
        App -->> Client: 422 Unprocessable Entity (Validation Errors)
    else Valid Request Schema
        App ->>+ SessionMgr: get_db()
        SessionMgr -->>- App: Yield SQLAlchemy Session
        App ->> Controller: signup(request, request_contract, headers, signup_service)
        activate Controller
        Controller ->> Controller: Resolve client_ip, user_agent, x_device_id
        Controller ->> Service: signup_user(request_contract)
        activate Service

        Service ->>+ Validator: validate_request(request_contract)
        Validator -->>- Service: (status, response)

        alt Metadata Missing, Terms Not Accepted, or Invalid Age (400)
            Service -->> Controller: (400, BaseApiError IDs 4, 5, 6, 7, 11)
            Controller ->> Controller: Log warning if BaseApiError
            Controller -->> App: JSONResponse (400)
            App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [id]}
        else Valid Request Metadata & Eligibility
            Service ->>+ UserRepo: get_by_mail(email)
                UserRepo ->>+ DB: SELECT FROM member.user WHERE email = ?
                DB -->>- UserRepo: User record or None
                UserRepo -->>- Service: Optional[User]

                alt Email Already Registered
                    Service -->> Controller: (400, BaseApiError ID 1)
                    Controller ->> Controller: Log warning if BaseApiError
                    Controller -->> App: JSONResponse (400)
                    App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [1]}
                else Email Available
                    Service ->>+ TermsRepo: get_by_tag_and_version(term_code, term_version)
                    TermsRepo ->>+ DB: SELECT FROM signup.terms WHERE tag = ? AND version = ? AND active = true
                    DB -->>- TermsRepo: Terms record or None
                    TermsRepo -->>- Service: Optional[Terms]

                    alt Invalid or Inactive Term
                        Service -->> Controller: (400, BaseApiError ID 3)
                        Controller ->> Controller: Log warning if BaseApiError
                        Controller -->> App: JSONResponse (400)
                        App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [3]}
                    else Active Term Found
                        Service ->>+ Crypto: validate_password(password)
                        Crypto -->>- Service: bool (regex complexity match)

                        alt Password Fails Complexity Policy
                            Service -->> Controller: (400, BaseApiError ID 2)
                            Controller ->> Controller: Log warning if BaseApiError
                            Controller -->> App: JSONResponse (400)
                            App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [2]}
                        else Password Valid
                            Service ->>+ Crypto: encrypt_password(password)
                            Crypto -->>- Service: bcrypt password hash

                            Note over Service,DB: Transaction Pipeline (create_without_commit)

                            Service ->>+ UserRepo: create_without_commit(session, nick_name, email, hash_password)
                            UserRepo ->>+ DB: INSERT INTO member.user ... (flush)
                            DB -->>- UserRepo: new_user, success
                            UserRepo -->>- Service: (new_user, true)

                            alt User Creation Failed
                                Service ->> DB: rollback()
                                Service -->> Controller: (400, BaseApiError ID 3)
                                Controller -->> App: JSONResponse (400)
                                App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [3]}
                            else User Created
                                Service ->>+ UserDetailsRepo: create_without_commit(session, new_user.id, born_date)
                                UserDetailsRepo ->>+ DB: INSERT INTO member.user_details ... (flush)
                                DB -->>- UserDetailsRepo: new_user_details, success
                                UserDetailsRepo -->>- Service: (new_user_details, true)

                                alt User Details Creation Failed
                                    Service ->> DB: rollback()
                                    Service -->> Controller: (400, BaseApiError ID 10)
                                    Controller -->> App: JSONResponse (400)
                                    App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [10]}
                                else User Details Created
                                    Service ->>+ AgreeRepo: create_without_commit(session, new_user.id, term.id)
                                    AgreeRepo ->>+ DB: INSERT INTO signup.user_agreements ... (flush)
                                    DB -->>- AgreeRepo: new_user_agreement, success
                                    AgreeRepo -->>- Service: (new_user_agreement, true)

                                    alt Agreement Creation Failed
                                        Service ->> DB: rollback()
                                        Service -->> Controller: (400, BaseApiError ID 3)
                                        Controller -->> App: JSONResponse (400)
                                        App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [3]}
                                    else Agreement Created
                                        Service ->>+ DeviceRepo: create_without_commit(session, new_user.id, x_device_id, [client_ip], user_agent)
                                        DeviceRepo ->>+ DB: INSERT INTO member.device ... (flush)
                                        DB -->>- DeviceRepo: new_device, success
                                        DeviceRepo -->>- Service: (new_device, true)

                                        alt Device Creation Failed
                                            Service ->> DB: rollback()
                                            Service -->> Controller: (400, BaseApiError ID 8)
                                            Controller -->> App: JSONResponse (400)
                                            App -->> Client: 400 Bad Request {"status": "ERROR", "errors": [8]}
                                        else All Entities Created
                                            Service ->> DB: commit()
                                            Service -->> Controller: (201, BaseApiSuccess)
                                            Controller -->> App: JSONResponse (201)
                                            App -->> Client: 201 Created {"status": "SUCESS", "message": "User registered successfully.", "data": null}
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
        deactivate Service
        deactivate Controller
    end
    deactivate App
```

---

## 3. Specifications & Contracts

### 3.1 HTTP Request
- **Method**: `POST`
- **Path**: `/api/v1/signup/user`

#### Request Headers
| Header | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `Content-Type` | `string` | Yes | Must be `application/json`. |
| `X-Device-Id` | `string` | Yes | Unique client device identifier (up to 200 characters). |
| `User-Agent` | `string` | Yes | Client application or browser User-Agent string. |
| `X-Forwarded-For` | `string` | No | Proxy-forwarded client IP list; falls back to `request.client.host`. |

#### Request Body (`SignupUserRequest`)
| Field | Type | Required | Constraints & Description |
| :--- | :--- | :---: | :--- |
| `nick_name` | `string` | Yes | Public display nickname between 1 and 150 characters. |
| `email` | `EmailStr` | Yes | Valid RFC-compliant email address (unique in `member.user`). |
| `password` | `string` | Yes | Between 8 and 16 characters; must satisfy `REGEX_FOR_PASSWORD` (digit, lowercase, uppercase, special character, no spaces). |
| `accept_terms` | `boolean` | Yes | Explicit confirmation of terms acceptance (`true` required). |
| `term_code` | `string` | Yes | Identifier tag of the accepted terms document (1–50 characters). |
| `term_version` | `integer` | Yes | Version number of the accepted terms document (`>= 1`, must be active). |
| `born_date` | `PastDate` | Yes | User birth date (`YYYY-MM-DD`); validated against `MIN_AGE_FOR_ACCOUNT` and `MAX_AGE_FOR_ACCOUNT`. |

```json
{
  "nick_name": "sofia_reader",
  "email": "user@example.com",
  "password": "Secure@123",
  "accept_terms": true,
  "term_code": "TERMS_OF_USE",
  "term_version": 1,
  "born_date": "1995-05-15"
}
```

### 3.2 HTTP Responses

#### Success Response (`201 Created`)
```json
{
  "message": "User registered successfully.",
  "data": null,
  "status": "SUCESS"
}
```

#### Business Validation Error (`400 Bad Request`)
```json
{
  "message": "Email or username invalid",
  "data": null,
  "status": "ERROR",
  "errors": [1]
}
```

##### Domain Error Code Catalog (`EResponseAuth`)
| Error ID | Enum Member | Message |
| :---: | :--- | :--- |
| `1` | `SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS` | `"Email or username invalid"` |
| `2` | `SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID` | `"The password must contain a single digit from 0 to 9, lowercase letter, no space,uppercase letter, special character and a size between 8 and 16"` |
| `3` | `SIGNUP_400_SIGNUP_USER_TERM_INVALID` | `"Invalid term code or version"` |
| `3` | `SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER` | `"Sorry! that user could not be created, please try again later"` |
| `3` | `SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS` | `"Sorry! that user could not be created, please try again later"` |
| `4` | `SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED` | `"You must accept the terms and conditions to continue"` |
| `5` | `SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND` | `"The client IP address could not be determined"` |
| `6` | `SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND` | `"The user agent could not be determined"` |
| `7` | `SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND` | `"The device ID could not be determined"` |
| `8` | `SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE` | `"Sorry! that user could not be created, please try again later"` |
| `9` | `SIGNUP_201_SIGNUP_USER_CREATED` | `"User registered successfully."` |
| `10` | `SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS` | `"Sorry! that user could not be created, please try again later"` |
| `11` | `SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE` | `"Please validate the born date"` |

#### Schema Validation Error (`422 Unprocessable Entity`)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```

#### Internal Server Error (`500 Internal Server Error`)
```json
{
  "message": "Ops! Something went wrong. Try again later.",
  "data": {
    "details": {},
    "method": "POST",
    "url": "http://localhost:8000/api/v1/signup/user"
  },
  "status": "ERROR",
  "errors": ["Internal Server Error"]
}
```

---

## 4. Related Implementation Files
- [`main.py`](../../../../../Code/Back-end/Auth/src/main.py)
- [`router.py`](../../../../../Code/Back-end/Auth/src/api/router.py)
- [`controller.py`](../../../../../Code/Back-end/Auth/src/service/signup/controller.py)
- [`service.py`](../../../../../Code/Back-end/Auth/src/service/signup/service.py)
- [`signup_user_validator.py`](../../../../../Code/Back-end/Auth/src/service/signup/validator/signup_user_validator.py)
- [`request.py`](../../../../../Code/Back-end/Auth/src/service/signup/request.py)
- [`encryption.py`](../../../../../Code/Back-end/Auth/src/core/encryption.py)
- [`Eresponse_auth.py`](../../../../../Code/Back-end/Auth/src/core/enum/Eresponse_auth.py)
- [`Estatus_base_api.py`](../../../../../Code/Back-end/Auth/src/core/enum/Estatus_base_api.py)
- [`session_manager.py`](../../../../../Code/Back-end/Auth/src/core/database/session_manager.py)
- [`user.py` (Entity)](../../../../../Code/Back-end/Auth/src/contracts/entities/user.py)
- [`user_details.py` (Entity)](../../../../../Code/Back-end/Auth/src/contracts/entities/user_details.py)
- [`user.py` (Repository)](../../../../../Code/Back-end/Auth/src/repositories/user.py)
- [`user_details.py` (Repository)](../../../../../Code/Back-end/Auth/src/repositories/user_details.py)
- [`terms.py` (Repository)](../../../../../Code/Back-end/Auth/src/repositories/terms.py)
- [`user_agreements.py` (Repository)](../../../../../Code/Back-end/Auth/src/repositories/user_agreements.py)
- [`device.py` (Repository)](../../../../../Code/Back-end/Auth/src/repositories/device.py)
- [`base_api_sucess.py`](../../../../../Code/Back-end/Auth/src/schema/default/base_api_sucess.py)
- [`base_api_error.py`](../../../../../Code/Back-end/Auth/src/schema/default/base_api_error.py)
- [`server_exception_handler.py`](../../../../../Code/Back-end/Auth/src/core/middleware/server_exception_handler.py)
