# User Signup Validation & Persistence Decision Flow

## 1. Overview
This policy defines the deterministic sequence of validation gates, security checks, and persistence steps enforced by `SignupController` and `SignupService` during user onboarding (`POST /api/v1/signup/user`). Every registration request must pass client telemetry verification, explicit legal consent validation, email uniqueness checks, active terms verification, password complexity enforcement, and three-stage relational persistence (`member.user`, `signup.user_agreements`, and `member.device`).

---

## 2. Decision Flowchart

The following Mermaid decision flowchart maps all conditional gates, domain error codes (`EResponseAuth`), and terminal HTTP outcomes:

```mermaid
flowchart TD
    Start(["Start: POST /api/v1/signup/user"]) --> InputData[/"Receive Headers & JSON Body"/]
    InputData --> ValidateSchema{"Is Pydantic Schema Valid?"}
    ValidateSchema -->|"No"| Reject422(["End: 422 Unprocessable Entity"])

    ValidateSchema -->|"Yes"| ResolveHeaders["Resolve client_ip, user_agent, and x_device_id"]
    ResolveHeaders --> CheckIP{"Is client_ip Present?"}
    CheckIP -->|"No"| RejectIP(["End: 400 Bad Request - Error ID 5"])

    CheckIP -->|"Yes"| CheckUA{"Is User-Agent Present?"}
    CheckUA -->|"No"| RejectUA(["End: 400 Bad Request - Error ID 6"])

    CheckUA -->|"Yes"| CheckDeviceID{"Is X-Device-Id Present?"}
    CheckDeviceID -->|"No"| RejectDeviceID(["End: 400 Bad Request - Error ID 7"])

    CheckDeviceID -->|"Yes"| CheckConsent{"Is accept_terms == true?"}
    CheckConsent -->|"No"| RejectConsent(["End: 400 Bad Request - Error ID 4"])

    CheckConsent -->|"Yes"| QueryEmail[("Query member.user by email")]
    QueryEmail --> EmailExists{"Does Email Already Exist?"}
    EmailExists -->|"Yes"| RejectDuplicate(["End: 400 Bad Request - Error ID 1"])

    EmailExists -->|"No"| QueryTerm[("Query active signup.terms by tag & version")]
    QueryTerm --> TermValid{"Does Active Term Exist?"}
    TermValid -->|"No"| RejectTerm(["End: 400 Bad Request - Error ID 3"])

    TermValid -->|"Yes"| CheckPasswordPolicy[["Encryption.validate_password (Regex Policy)"]]
    CheckPasswordPolicy --> IsPasswordValid{"Meets Password Complexity?"}
    IsPasswordValid -->|"No"| RejectPassword(["End: 400 Bad Request - Error ID 2"])

    IsPasswordValid -->|"Yes"| HashPassword[["Encryption.encrypt_password (bcrypt)"]]
    HashPassword --> InsertUser[("Persist User in member.user")]
    InsertUser --> IsUserCreated{"Was User Created?"}
    IsUserCreated -->|"No"| RejectUserCreate(["End: 400 Bad Request - Error ID 3"])

    IsUserCreated -->|"Yes"| InsertAgreement[("Persist Agreement in signup.user_agreements")]
    InsertAgreement --> IsAgreementCreated{"Was Agreement Created?"}
    IsAgreementCreated -->|"No"| RejectAgreementCreate(["End: 400 Bad Request - Error ID 3"])

    IsAgreementCreated -->|"Yes"| InsertDevice[("Persist Device in member.device")]
    InsertDevice --> IsDeviceCreated{"Was Device Created?"}
    IsDeviceCreated -->|"No"| RejectDeviceCreate(["End: 400 Bad Request - Error ID 8"])

    IsDeviceCreated -->|"Yes"| BuildSuccess[/"Return BaseApiSuccess Envelope"/]
    BuildSuccess --> EndCreated(["End: 201 Created - User Registered"])
```

---

## 3. Specifications & Policy Gates

### 3.1 Client Telemetry & Legal Consent Gates
1. **Client IP Resolution & Gate (`Error ID 5`)**:
   - `SignupController` extracts the first IP from `X-Forwarded-For` when present, falling back to `request.client.host`.
   - If `client_ip` resolves to `None`, registration is rejected with `SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND` (`5`).
2. **User-Agent Gate (`Error ID 6`)**:
   - Requires a non-null `User-Agent` HTTP header; otherwise rejects with `SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND` (`6`).
3. **Device Identifier Gate (`Error ID 7`)**:
   - Requires a non-null `X-Device-Id` HTTP header; otherwise rejects with `SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND` (`7`).
4. **Terms Acceptance Gate (`Error ID 4`)**:
   - Requires `accept_terms is True`; otherwise rejects with `SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED` (`4`).

### 3.2 Domain & Credential Security Gates
5. **Email Uniqueness Gate (`Error ID 1`)**:
   - Queries `UserRepository.get_by_mail(email)`. If an existing user record is found, rejects with `SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS` (`1`) using a generic message (`"Email or username invalid"`) to prevent account enumeration.
6. **Active Terms Lookup Gate (`Error ID 3`)**:
   - Queries `TermsRepository.get_by_tag_and_version(term_code, term_version)` filtering `active == True`. If no active record matches, rejects with `SIGNUP_400_SIGNUP_USER_TERM_INVALID` (`3`).
7. **Password Complexity Gate (`Error ID 2`)**:
   - Evaluates `Encryption.validate_password(password)` against `REGEX_FOR_PASSWORD` (requiring at least one digit `0-9`, one lowercase letter, one uppercase letter, one special character, no whitespace, and length between 8 and 16 characters). On failure, rejects with `SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID` (`2`).

### 3.3 Persistence Gates
8. **User Creation Gate (`Error ID 3`)**:
   - Hashes the validated password via `Encryption.encrypt_password` (`bcrypt`) and persists `User` in `member.user`. Returns `SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER` (`3`) if no entity is returned.
9. **Terms Agreement Audit Gate (`Error ID 3`)**:
   - Persists `UserAgreements(user_id=new_user.id, term_id=term.id)` in `signup.user_agreements`. Returns `SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS` (`3`) if no entity is returned.
10. **Device Registration Gate (`Error ID 8`)**:
    - Persists `Device(user_id=new_user.id, x_device_id=request.x_device_id, ip_list=[request.client_ip], user_agent=request.user_agent)` in `member.device`. Returns `SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE` (`8`) if no entity is returned, or `201 Created` (`BaseApiSuccess`) on completion.

---

## 4. Related Implementation Files
- [`controller.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/controller.py)
- [`service.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/service.py)
- [`request.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/request.py)
- [`encryption.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/encryption.py)
- [`Eresponse_auth.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/enum/Eresponse_auth.py)
- [`user.py` (Repository)](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/repositories/user.py)
- [`terms.py` (Repository)](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/repositories/terms.py)
- [`user_agreements.py` (Repository)](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/repositories/user_agreements.py)
- [`device.py` (Repository)](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/repositories/device.py)
