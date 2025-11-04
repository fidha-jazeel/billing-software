# billing-software

travel_billing/
│
├── main.py               # Entry point
├── ui/                   # PyQt .ui files
│   ├── dashboard.ui
│   ├── billing_form.ui
│   └── reports.ui
│
├── database/
│   └── db.py             # SQLite setup + CRUD
│
├── models/
│   └── transaction.py    # Dataclasses or Pydantic models
│
├── controllers/
│   ├── billing_controller.py
│   └── report_controller.py
│
└── utils/
    ├── pdf_generator.py  # for bill print/export
    └── charts.py         # analytics helper