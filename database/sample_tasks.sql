 INSERT INTO assistant_task
(
task_code,
customer_request,
intent,
extracted_entities,
risk_score,
employee_assignment,
generated_steps,
whatsapp_message,
email_message,
sms_message,
status,
created_at
)

VALUES

(
'VNH-2026-001',
'I need to send KES 15,000 to my mother in Kisumu urgently',
'send_money',
'{"amount":15000,"recipient":"mother","location":"Kisumu","urgency":"high"}',
75,
'Finance',
'["Verify sender identity","Confirm recipient","Initiate transfer","Send confirmation"]',
'Hi 👋 We received your money transfer request. Task: VNH-2026-001',
'Dear Customer, your transfer request VNH-2026-001 has been received.',
'VNH-2026-001 received.',
'Pending',
CURRENT_TIMESTAMP
),

(
'VNH-2026-002',
'Please verify my land title deed in Karen',
'verify_document',
'{"document_type":"land title","location":"Karen"}',
85,
'Legal',
'["Receive document","Verify ownership","Legal review","Notify customer"]',
'Hi 👋 Your verification request was received.',
'Dear Customer, your land title verification request was received.',
'VNH-2026-002 received.',
'In Progress',
CURRENT_TIMESTAMP
),

(
'VNH-2026-003',
'Please clean my apartment in Westlands',
'hire_service',
'{"service_type":"cleaning","location":"Westlands"}',
30,
'Operations',
'["Assign cleaner","Schedule appointment","Confirm completion"]',
'Hi 👋 Cleaning request received.',
'Dear Customer, your service request has been received.',
'VNH-2026-003 received.',
'Completed',
CURRENT_TIMESTAMP
),

(
'VNH-2026-004',
'I need airport pickup at JKIA',
'airport_transfer',
'{"location":"JKIA"}',
20,
'Logistics',
'["Assign driver","Schedule pickup","Confirm arrival"]',
'Hi 👋 Airport transfer received.',
'Dear Customer, airport transfer scheduled.',
'VNH-2026-004 received.',
'Pending',
CURRENT_TIMESTAMP
),

(
'VNH-2026-005',
'Check status for task VNH-2026-001',
'check_status',
'{"task_code":"VNH-2026-001"}',
10,
'Customer Support',
'["Find task","Return status"]',
'Hi 👋 Status request received.',
'Dear Customer, your status request has been received.',
'VNH-2026-005 received.',
'Completed',
CURRENT_TIMESTAMP
);