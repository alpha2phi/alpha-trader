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

---

<div style="zoom: 150%">

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
  R1[Submit work request<br/>with clear requirements and scope]:::req
  R1a[Ensure alignment<br/>AIA CPP and ITSR document number<br/>GIS PaaS Hardening or security guidelines<br/>Group Architecture Standards<br/>Regular Maintenance Azure service EOL policy updates Kubernetes version App Service Python<br/>Regular Maintenance Data refresh Cost Center WBSCode<br/>Other considerations Cost optimization and Service EOL tracking]:::req
  R2[Provide clarifications or resubmit<br/>if rejected or unclear]:::req
  R3[Perform UAT testing]:::req
  R4[Request scope changes if any]:::req
  R5[Confirm acceptance and closure]:::req
end

subgraph E[Engineering Team]
direction TB
  E1[Review for completeness alignment and feasibility]:::eng
  G1{Complete and clear}:::gate
  E2[Confirm proceed or stop]:::eng
  G2{Proceed}:::gate
  E3[Effort estimate and delivery timeline]:::eng
  E4[Identify dependencies Automation or GIS]:::eng
  E5[Document assumptions and risks]:::eng
  E6[Implement approved requirements]:::eng
  E7[Fix defects reported in UAT]:::eng
  E8[Reassess change impact and update estimate and timeline]:::eng
  E9[Finalize and handover documentation<br/>Update policy tracker<br/>Update GitHub project dashboard and issue tracker]:::eng
end

subgraph A[Automation Team]
direction TB
  A1[Align on automation needs policy as code pipelines rollout consistency]:::auto
end

subgraph G[GIS or Security Team]
direction TB
  S1[Align on security requirements GIS guidelines and hardening]:::gis
end

%% ===================== FLOW =====================
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

R4 -->|New or changed scope| E8 --> R3
R4 -->|No changes| E9 --> R5

```
</div>