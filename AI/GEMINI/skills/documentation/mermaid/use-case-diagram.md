---
name: mermaid-use-case-diagram
description: Guidelines, syntax standards, and specifications for creating and updating UML Use Case diagrams using Mermaid for business capabilities and user interactions.
---

# Mermaid Use Case Diagram Skill

## 1. Overview & Purpose

Whenever new business features, user roles, permission policies, or functional capabilities are introduced or modified, you must generate or update the corresponding UML Use Case diagram.

Use Case diagrams establish the functional perimeter of the system, illustrating how different types of actors (humans, external systems, automated services) interact with bounded business use cases.

---

## 2. Branch Inspection & Selective Update Protocol

Always orchestrate documentation changes through the master index at [documentation.md](../documentation.md):

1. **Inspect Branch Changes First**:
   Analyze `git diff HEAD` (or compare against base branch) to identify new business capabilities, permission changes, route additions, or domain services that represent user-facing or actor-driven interactions.
2. **Search Existing References**:
   Query `Documentation/config/docs/business-rules/` for mentions of the actor, module, or use case name (e.g., `grep -rn "Checkout" Documentation/config/docs/business-rules/`).
3. **Selective Diagram Update**:
   - If a use case diagram already exists for that domain, update **strictly the affected use cases, actors, associations, or include/extend relationships**. Do not disturb unrelated use cases.
4. **Auto-Create Missing Documentation Files**:
   - If no use case documentation exists for the feature, create a new `.md` file under `Documentation/config/docs/business-rules/<feature>-use-cases.md`.
   - Embed the new Mermaid use case diagram.
   - Register the new page in `Documentation/config/mkdocs.yml` under `nav:`.

---

## 3. Storage & Location Conventions

- Store use case documentation in:
  `Documentation/config/docs/business-rules/<domain>-use-cases.md` or `Documentation/config/docs/business-rules/use-cases/`
- Embed the diagram in Markdown using fenced code blocks with the `mermaid` language tag:
  ```markdown
  ```mermaid
  flowchart LR
      ...
  ```
  ```

---

## 4. Syntax Standards & Modeling Conventions

Because Mermaid models UML Use Cases with high fidelity using its `flowchart` engine, follow these strict styling and shape conventions:

### 4.1 Actors
- Declare actors outside system boundary subgraphs.
- Represent actors using descriptive identifiers and human/system icons:
  ```text
  actor_customer["👤 Customer"]
  actor_admin["👤 System Administrator"]
  actor_payment_gateway["🤖 Payment Gateway (External)"]
  ```

### 4.2 System Boundary (`subgraph`)
- Always encapsulate use cases within a named `subgraph` that defines the system perimeter:
  ```text
  subgraph SofiaSystem ["System: Sofia Platform"]
      ...
  ```

### 4.3 Use Cases (Stadium / Capsule Nodes)
- Always represent use cases using the stadium shape `(["Use Case Name"])`:
  ```text
  uc_register(["Register Account"])
  uc_order(["Place New Order"])
  ```

### 4.4 Standard UML Relationships
| UML Relationship | Mermaid Syntax | Description |
| :--- | :---: | :--- |
| **Actor Association** | `actor --- uc_order` | Solid line connecting actor to use case |
| **Direct Association** | `uc_order --> actor_gateway` | Directed interaction with secondary/external actor |
| **`<<include>>`** | `uc_order -.->\|"<<include>>"\| uc_pay` | Dotted line with open arrow; base use case always requires the included case |
| **`<<extend>>`** | `uc_coupon -.->\|"<<extend>>"\| uc_order` | Dotted line with open arrow; optional behavior added under certain conditions |
| **Actor Generalization** | `actor_admin ---\|> actor_user` | Solid line with triangular arrowhead; Admin inherits User capabilities |

---

## 5. Complete Use Case Reference Example

```mermaid
flowchart LR
    %% Actors
    actor_guest["👤 Guest User"]
    actor_user["👤 Authenticated Member"]
    actor_admin["👤 Platform Admin"]
    actor_gateway["🏦 Payment Gateway (External)"]

    %% Actor Generalization
    actor_admin --|> actor_user
    actor_user --|> actor_guest

    %% System Boundary
    subgraph SystemPerimeter ["System: Sofia Platform"]
        uc_browse(["Browse Public Catalog"])
        uc_login(["Sign In / Authenticate"])
        uc_checkout(["Checkout & Place Order"])
        uc_process_pay(["Process Card Payment"])
        uc_apply_voucher(["Apply Discount Coupon"])
        uc_track(["Track Order Status"])
        uc_manage_catalog(["Manage Product Catalog"])
        uc_view_audit(["View System Audit Logs"])

        %% Include relationships
        uc_checkout -.->|"<<include>>"| uc_login
        uc_checkout -.->|"<<include>>"| uc_process_pay

        %% Extend relationships
        uc_apply_voucher -.->|"<<extend>>"| uc_checkout
    end

    %% Actor Associations
    actor_guest --- uc_browse
    actor_guest --- uc_login

    actor_user --- uc_checkout
    actor_user --- uc_track

    uc_process_pay --> actor_gateway

    actor_admin --- uc_manage_catalog
    actor_admin --- uc_view_audit
```

---

## 6. Best Practices & Guidelines

1. **Focus on User Goals, Not Technical Steps**:
   - Good: `(["Checkout & Place Order"])`, `(["Reset Password"])`.
   - Bad: `(["Execute SQL Transaction"])`, `(["Hash Password with Bcrypt"])`. Technical steps belong to sequence diagrams.
2. **Direction**: Use `flowchart LR` (Left to Right) for clear visual separation: primary actors on the left, system boundary in the center, secondary/external systems on the right.
3. **MkDocs Safety**:
   - Always quote labels containing brackets, quotes, or special characters: `uc_ext -.->|"<<extend>>"| uc_base`.

## 7. Verification Checklist

- [ ] Starts with `flowchart LR`.
- [ ] System boundary is clearly enclosed in a named `subgraph`.
- [ ] Use cases use stadium syntax `(["..."])`.
- [ ] Actors are placed outside the system boundary.
- [ ] `<<include>>` and `<<extend>>` labels use quoted syntax `|"<<include>>"|` or `|"<<extend>>"|`.
- [ ] Relationships reflect business value and goals rather than implementation code details.
