# Security and Governance

## Authentication
- Integrate with SSO (Azure AD / Okta)
- Use user identity for access control

## Authorization
- Enforce project-level permissions
- Filter data at query time

## Access Control Model
user → allowed_projects → retrieval_filter

## Encryption
- At rest (KMS)
- In transit (TLS)

## PII Handling
- Detect and tag sensitive data
- Mask or restrict responses if needed

## Audit Logging
- Log queries
- Log retrieved documents
- Track user access

## Data Retention
- Support deletion requests
- Remove indexed data on demand

## Safety Controls
- Confidentiality labels
- Block sensitive data exposure