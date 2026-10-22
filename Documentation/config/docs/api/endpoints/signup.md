# User Signup Endpoint (`POST /v1/auth/`)

## 1. Overview
The **User Signup Endpoint** provides initial onboarding and account registration for users within the Sofia platform. It receives client registration payloads, validates email formatting, password length boundaries, and terms acceptance before delegating processing to the signup domain service.

---

## 2. Architecture & Sequence Diagram

The following Mermaid sequence diagram details the complete request lifecycle, including Pydantic input validation, service processing, and error interception:

```mermaid
sequenceDiagram
    autonumber
    actor Client
    box Application Layer
        participant App as FastAPI App
        participant Controller as SignupController
        participant Service as SignupService
        participant Handler as ServerExceptionHandler
    end

    Client ->>+ App: POST /v1/auth/ (SignupRequest)
    App ->> App: Validate SignupRequest via Pydantic
    alt Invalid Request Payload
        App -->> Client: 422 Unprocessable Entity (Validation Errors)
    else Valid Payload
        App ->>+ Controller: signup(request)
        Controller ->>+ Service: signup(request)
        alt Unhandled Exception
            Service -->> Handler: Exception raised
            Handler ->> Handler: Log error & construct BaseApiError
            Handler -->>- App: 500 Internal Server Error JSONResponse
            App -->> Client: 500 Internal Server Error
        else Success Flow
            Service ->> Service: Construct BaseApiSuccess envelope
            Service -->>- Controller: 202 Accepted JSONResponse
            Controller -->>- App: JSONResponse
            App -->>- Client: 202 Accepted {"status": "success", "message": "User registered successfully.", "data": null}
        end
    end
```

---

## 3. Specifications & Contracts

### 3.1 HTTP Request
- **Method**: `POST`
- **Path**: `/v1/auth/`
- **Headers**: `Content-Type: application/json`

#### Request Body (`SignupRequest`)
| Field | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `email` | `EmailStr` | Yes | Valid email address according to RFC standards. |
| `password` | `string` | Yes | Password between 6 and 20 characters. |
| `accept_terms` | `boolean` | Yes | Confirmation of terms of service acceptance. |

```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "accept_terms": true
}
```

### 3.2 HTTP Responses

#### Success Response (`202 Accepted`)
```json
{
  "message": "User registered successfully.",
  "data": null,
  "status": "success"
}
```

#### Validation Error (`422 Unprocessable Entity`)
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
  "status": "error",
  "message": "Ops! Something went wrong. Try again later.",
  "data": {
    "details": "<exception details>",
    "method": "POST",
    "url": "http://localhost:8000/v1/auth/"
  },
  "errors": ["Internal Server Error"]
}
```

---

## 4. Related Implementation Files
- [`router.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/api/router.py)
- [`controller.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/controller.py)
- [`service.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/service.py)
- [`request.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/service/signup/request.py)
- [`base_api_sucess.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_sucess.py)
- [`base_api_error.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/schema/default/base_api_error.py)
- [`server_exception_handler.py`](file:///home/pedrovotf/Desktop/Projects/Nievo-Sofia/Code/Back-end/Auth/src/core/middleware/server_exception_handler.py)
