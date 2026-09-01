Workflow Steps
User Authentication
Users securely sign up or log in to the application.
Product Image Upload
The user uploads or captures an image of a packaged commodity.
OCR Processing
The uploaded image is processed using OCR to extract relevant text such as MRP, net quantity, manufacturing date, expiry date, and other mandatory details.
Data Processing & Validation
Extracted information is structured and checked against the required packaging and labeling criteria.
Error Detection
Missing, unreadable, or potentially incorrect information is identified and highlighted.
Database Storage
Processed product information and validation results are stored securely in Supabase.
Results & Report
The user receives a clear summary of the extracted information, detected issues, and compliance status through the dashboard.
🏗️ High-Level Architecture
React Frontend
      │
      ▼
Backend / API
      │
      ├──────────────► OCR Engine
      │                    │
      │                    ▼
      │              Extracted Data
      │                    │
      ▼                    ▼
Supabase ◄──────── Data Validation
      │
      ▼
Dashboard & Reports