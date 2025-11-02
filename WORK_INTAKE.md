## **1. Request Submission**

- **Requestor** submits a work request with **clear requirements and scope**.
- Requirements must align with at least one of the following:
  - **AIA Standards** – referencing details from **CPP** and an **ITSR** document number.
  - **GIS Guidelines** – such as **PaaS Hardening** or other security guidelines.
  - **Group Architecture Standards** – with supporting documents.
  - **Regular Maintenance** – e.g.,
    - Policy updates for **Azure service EOL**, such as Kubernetes version upgrade, App Service Python version EOL.
    - Data refresh such as Cost Center, WBSCode, etc.
  - **Other Considerations** – e.g., **cost optimization**, **service EOL tracking**.

---

## **2. Requirement Assessment**

- **Engineering Team** reviews the submitted request for completeness, alignment, and feasibility. Incomplete or unclear requirements will be rejected and requestor needs to submit a new request.
- The team seeks clarification where needed and confirms whether to **proceed** or **stop** the request.

---

## **3. Effort Estimation & Planning**

- Once the request is approved to proceed, **Engineering Team**:
  - Identifies dependencies (e.g., Automation or GIS teams),
  - Documents key **assumptions and risks**,
  - Provides **effort estimation** and a **delivery timeline**.

---

## **4. Implementation & Collaboration**

- **Engineering Team** implements the approved requirements.
- If the request involves **automation**, the team must align with the **Automation Team** to ensure consistency with existing automation.
- **Engineering Team** to align with **GIS Team** if this is a security requirement.

---

## **5. Testing & Defect Resolution**

- **Requestor** performs **testing (UAT)** to validate that requirements are met.
- **Engineering Team** reviews and fixes any reported defects.

---

## **6. Change Request Handling**

- If **Requestor** introduces new or changed requirements outside the original scope:
  - **Engineering Team** reassesses the impact,
  - Provides updated **effort and timeline estimates**,
  - Seeks confirmation from the **Requestor** before proceeding with additional work.

---

## **7. Closure**

- Upon successful testing and validation:
  - **Requestor** confirms **acceptance and closure**,
  - **Engineering Team** completes final documentation, such as
    - Updates to the policy tracker.
    - Updates in GitHub project dashboard and issue tracker.

---

## Process Flow

```mermaid

flowchart TD
%% ===== STYLES =====
classDef req fill:#e8f2ff,stroke:#1d4ed8,stroke-width:1px,rx:6,ry:6;
classDef eng fill:#fff3e0,stroke:#f97316,stroke-width:1px,rx:6,ry:6;
classDef auto fill:#ecfdf5,stroke:#16a34a,stroke-width:1px,rx:6,ry:6;
classDef gis fill:#f3e8ff,stroke:#7e22ce,stroke-width:1px,rx:6,ry:6;
classDef gate fill:#ffffff,stroke:#111827,stroke-dasharray:3 3,rx:8,ry:8;

%% ===== SWIMLANES =====
subgraph R[Requestor]
direction TB
  R1[Submit work request]:::req
  R1a[Ensure alignment]:::req
  R2[Provide clarifications or<br/>resubmit if<br/>rejected or unclear]:::req
  R3[Perform UAT testing]:::req
  R4[Request scope changes<br/>if any]:::req
  R5[Confirm acceptance <br/>and closure]:::req
end

subgraph E[Engineering Team]
direction TB
  E1[Review for completeness <br/> and alignment]:::eng
  G1{Complete and clear}:::gate
  E2[Confirm proceed or stop]:::eng
  G2{Proceed}:::gate
  E3[Identify dependencies]:::eng
  E4[Document assumptions<br/>and risks]:::eng
  E5[Provide estimate]:::eng
  E6[Implement approved<br/>requirements]:::eng
  E7[Fix defects from UAT]:::eng
  E8[Reassess and update<br/>estimate and timeline]:::eng
  E9[Finalize and handover]:::eng
end

subgraph A[Automation Team]
direction TB
  A1[Align on automation<br/>needs]:::auto
end

subgraph G[GIS Team]
direction TB
  S1[Align on security<br/>requirements]:::gis
end

%% ===== FLOW TOP DOWN =====
R1 --> R1a --> E1
E1 --> G1
G1 -- "No" --> R2 --> E1
G1 -- "Yes" --> E2
E2 --> G2
G2 -- "No" --> R2
G2 -- "Yes" --> E3 --> E4 --> E5 --> E6

E6 -->|If automation involved| A1 --> E6
E6 -->|If security requirement| S1 --> E6

E6 --> R3
R3 -->|Defects found| E7 --> R3
R3 -->|Pass| R4

R4 -->|New/changed requirements| E8 --> R3
R4 -->|No changes| E9 --> R5

```
