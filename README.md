# 🏥 Patient Billing Module (`hms_insurance_billing`)

## Overview

This standalone Odoo module handles patient invoicing and insurance-based payments. It provides a service-oriented billing API that can be used by other hospital modules (like Reception, Pharmacy, and Lab) to automatically generate invoice lines.

---

## ✅ Features

- **Centralized Billing Logic**: All invoice creation and line additions are managed by a dedicated abstract service model.
- **Insurance Coverage Handling**: Automatically posts payments on behalf of insurance companies based on their coverage percentage.
- **Avoids Duplicate Billing**: Each service line (e.g., lab test or drug) is marked as invoiced to prevent repeated charges.
- **Modular Integration**: Easily callable from other apps without tight coupling.

---

## 📦 Module Structure

- `insurance.company`: Holds insurance provider info and their coverage percentage.
- `hms.billing.service`: A shared abstract model providing billing methods:
  - `bill_static_item(...)`: For one-off service charges like consultation.
  - `bill_dynamic_lines(...)`: For dynamic records like lab tests or drug lines.
  - `bill_item(...)`: General method that routes to the right billing function.

- Extension of `account.move` to handle auto-insurance payments on invoice post.
- `res.partner`: Extended to hold `national_id`, `is_patient`, and `insurance_company_id`.

---

## 🔌 How to Use the Module in Other Apps

### Step 1: Add it as a dependency

In your module’s `__manifest__.py`:

```python
'depends': ['hms_insurance_billing']
```

### Step 2: Call the billing service

In your model (e.g., `lab.line`, `pharmacy.line`, or `reception`), use:

```python
self.env['hms.billing.service'].bill_item(
    record=record,  # any record with 'price' and optionally 'quantity'
    patient_name=patient.name,
    national_id=patient.national_id,
    line_name=record.test_name or drug_name
)
```

Or for fixed charges (like consultation):

```python
self.env['hms.billing.service'].bill_item(
    patient_name=patient.name,
    national_id=patient.national_id,
    description='Consultation Fee',
    amount=record.consultation_fee
)
```

> **Note:** The record will be added to an open draft invoice if available, or a new one will be created. Insurance payment is handled when the invoice is posted.

---

## 🧾 Insurance Payment Logic

When the invoice is posted (`action_post`):
- If the patient has an insurance company,
- And the company has a coverage percentage > 0,
- A payment is automatically registered with amount: `coverage% * invoice total`.

---

## 🛡️ Security & Access

- Define access rules for `insurance.company` as needed in `ir.model.access.csv`.
- Only authorized users should create/update insurance settings.

---

## 📂 Menu Entries

- **Invoices** – Shows all outgoing invoices (`move_type = 'out_invoice'`).
- **Insurance Companies** – Manage list of insurance providers.
