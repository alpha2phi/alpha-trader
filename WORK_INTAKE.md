## **1. Request Submission**
- **Requestor** submits a work request with **clear requirements and defined scope**.
- **Requestor** makes sure the submitted requirements **must align** with the following standards and guidelines:  
  - **AIA Standards** – including details from **CPP** with **ITSR** document number.  
  - **GIS Guidelines** – such as **PaaS Hardening** or other security guidelines. 
  - **Group Architecture Standards** - including details from the related documents.
  - **Regular Maintenance Requirements**, including:  
    - Policy updates related to **Azure service EOL**, such as Kubernetes version upgrade, App Service Python version EOL.
    - Data refresh such as Cost Center, WBSCode, etc.
  - **Other Considerations**, such as:  
    - **Cost optimization**,  
    - **Service EOL tracking**

---

## **2. Requirement Assessment**
- **Engineering Team** reviews the submitted request for completeness, alignment, and feasibility.  Incomplete or unclear requirements will be rejected and requestor needs to submit a new new request.
- The team seeks clarification where needed and confirms whether to **proceed** or **stop** the request 

---

## **3. Effort Estimation & Planning**
- Once the request is approved to proceed, **Engineering Team**:  
  - Provides **effort estimation** and a **delivery timeline**,  
  - Identifies dependencies (e.g., Automation or GIS teams),  
  - Documents key **assumptions and risks**.  

---

## **4. Implementation & Collaboration**
- **Engineering Team** implements the approved requirements.  
- If the request involves **automation**, the team must align with the **Automation Team** to ensure consistency with existing automation.
- **Engineering Team** to align with **GIS Team** if this is a security requirement.

---

## **5. Testing & Defect Resolution**
- The **Requestor** performs **testing (UAT)** to validate that requirements are met.  
- The **Engineering Team** reviews and fixes any reported defects.

---

## **6. Change Request Handling**
- If the **Requestor** introduces new or changed requirements outside the original scope:  
  - The **Engineering Team** reassesses the impact,  
  - Provides updated **effort and timeline estimates**,  
  - Seeks confirmation from the Requestor before proceeding with additional work.  

---

## **7. Closure**
- Upon successful testing and validation:  
  - The **Requestor** confirms **acceptance and closure**,  
  - The **Engineering Team** completes final documentation, such as
    - Updates to the policy tracker. 
    - Updates in GitHub project dashboard and issue tracker.


```mermaid

flowchart LR
%% ===================== STYLING =====================
classDef req fill:#e8f2ff,stroke:#1d4ed8,stroke-width:1px,rx:6,ry:6;
classDef eng fill:#fff3e0,stroke:#f97316,stroke-width:1px,rx:6,ry:6;
classDef auto fill:#ecfdf5,stroke:#16a34a,stroke-width:1px,rx:6,ry:6;
classDef gis fill:#f3e8ff,stroke:#7e22ce,stroke-width:1px,rx:6,ry:6;
classDef gate fill:#ffffff,stroke:#111827,stroke-dasharray:3 3,rx:8,ry:8;

%% ===================== SWIMLANES =====================
subgraph R[Requestor]
direction TB
  R1[Submit work request<br/>with clear requirements & scope]:::req
  R1a[Ensure alignment:<br/>• AIA (CPP + ITSR #)<br/>• GIS (PaaS Hardening / security)<br/>• Group Architecture Standards<br/>• Regular Maintenance:<br/>&nbsp;&nbsp;– Azure EOL policy updates<br/>&nbsp;&nbsp;&nbsp;&nbsp;(e.g., K8s, AppSvc Python)<br/>&nbsp;&nbsp;– Data refresh (Cost Center, WBSCode)<br/>• Cost optimization & EOL tracking]:::req
  R2[Provide clarifications / resubmit<br/>if rejected or unclear]:::req
  R3[Perform UAT testing]:::req
  R4[Propose scope changes (if any)]:::req
  R5[Confirm acceptance & closure]:::req
end

subgraph E[Engineering Team]
direction TB
  E1[Review for completeness,<br/>alignment & feasibility]:::eng
  G1{Complete & clear?}:::gate
  E2[Decision to proceed or stop]:::eng
  G2{Proceed?}:::gate
  E3[Effort estimate &<br/>delivery timeline]:::eng
  E4[Identify dependencies<br/>(Automation/GIS/etc.)]:::eng
  E5[Document assumptions & risks]:::eng
  E6[Implement approved requirements]:::eng
  E7[Fix defects from UAT]:::eng
  E8[Reassess change impact,<br/>update effort & timeline]:::eng
  E9[Finalize & handover docs:<br/>• Update policy tracker<br/>• Update GitHub project & issues]:::eng
end

subgraph A[Automation Team]
direction TB
  A1[Align on automation needs:<br/>policy-as-code, pipelines,<br/>rollout consistency]:::auto
end

subgraph G[GIS / Security Team]
direction TB
  S1[Align on security requirements:<br/>GIS guidelines / hardening]:::gis
end

%% ===================== FLOW =====================

%% 1) Request Submission
R1 --> R1a --> E1

%% 2) Requirement Assessment
E1 --> G1
G1 -- "No (incomplete/unclear)" --> R2 --> E1
G1 -- "Yes" --> E2
E2 --> G2
G2 -- "Stop" --> R2
G2 -- "Proceed" --> E3 --> E4 --> E5 --> E6

%% 4) Implementation & Collaboration (alignments as needed)
E6 -->|If automation involved| A1 --> E6
E6 -->|If security requirement| S1 --> E6

%% 5) Testing & Defect Resolution
E6 --> R3
R3 -->|Defects found| E7 --> R3
R3 -->|Pass| R4

%% 6) Change Request Handling
R4 -->|New/changed scope?| E8 --> R3
R4 -->|No changes| E9 --> R5


```