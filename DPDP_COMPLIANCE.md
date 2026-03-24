# DPDP Act 2023 Compliance
1. **Notice & Consent**: IVR prompt and frontend checkbox for affirmative consent.
2. **Minimisation**: No Aadhaar. Phone numbers hashed for lookup and AES-256-GCM encrypted.
3. **Limitation**: 90-day retention for sessions and audio via Celery Beat and R2 lifecycle.
4. **Erasure**: DELETE endpoint to anonymize beneficiary records.
5. **Security**: RBAC and Supabase RLS policies.
