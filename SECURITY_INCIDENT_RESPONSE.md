# Mirenelle Ops Security Incident Response Plan

Last updated: 2026-06-16

## Purpose

This document defines the incident response procedure for Mirenelle Ops when
handling Amazon Information, Seller Central reports, Selling Partner API
data, order data, inventory data, accounting data, and related credentials.

Mirenelle Ops is a private internal operations and accounting application. It
is used only by authorized company operators for Amazon accounting, inventory,
order reconciliation, and business analytics.

## Scope

This plan applies to:

- Amazon Selling Partner API credentials and tokens.
- Seller Central reports imported into Mirenelle Ops.
- Amazon order, payment, inventory, fulfillment, and accounting data.
- Local application configuration and environment files.
- The local database used by Mirenelle Ops.
- Operator devices or accounts that can access the application or credentials.

Amazon Information is not sold, disclosed, or shared with external third
parties. Data is stored for internal business operations only.

## Roles

Incident Owner:

- The company account administrator or designated operator responsible for the
  Amazon Seller Central account and Mirenelle Ops deployment.
- Owns triage, containment, notification, remediation, and review.

Technical Responder:

- The operator or developer responsible for the Mirenelle Ops application and
  local infrastructure.
- Investigates application logs, configuration, credentials, database access,
  and code changes.

Business Owner:

- The business owner or authorized manager responsible for deciding business
  impact, operational continuity, and external communications where required.

For a small private deployment, one person may hold more than one role. The
responsibilities still apply.

## Incident Categories

The following events must be treated as security incidents when they involve or
may involve Amazon Information:

- Lost, leaked, exposed, or suspected compromised SP-API credentials, LWA
  client secrets, refresh tokens, access keys, passwords, or environment files.
- Unauthorized access to the Mirenelle Ops application, database, server,
  source repository, operator device, or Seller Central account.
- Accidental disclosure or transmission of Amazon Information to an
  unauthorized person or third party.
- Malware, phishing, account takeover, suspicious login, or suspicious API
  activity involving systems that can access Amazon Information.
- Unexpected changes to application code, configuration, database contents, or
  Amazon connector behavior.
- Loss of control over a device, account, repository, backup, or storage
  location that contains Amazon Information.

## Response Procedure

1. Identify and triage

   - Record the date and time of detection.
   - Identify affected systems, accounts, credentials, files, data categories,
     and time period.
   - Determine whether Amazon Information is involved or may be involved.

2. Contain

   - Disable affected accounts, tokens, secrets, or access paths.
   - Stop or pause affected import jobs, connector syncs, or application
     services if needed.
   - Restrict database, repository, and file access to authorized responders.

3. Investigate

   - Review application logs, connector logs, database access, source control
     history, configuration changes, and operator actions.
   - Determine the cause, scope, data affected, and whether credentials or
     Amazon Information were accessed, disclosed, modified, or lost.

4. Notify

   - If a security incident involves or may involve Amazon Information, notify
     Amazon at `security@amazon.com` within 24 hours of detection.
   - Include the known incident summary, detection time, affected systems,
     Amazon Information categories involved, containment actions, and current
     remediation status.
   - Follow any additional instructions received from Amazon.

5. Remediate and recover

   - Rotate affected credentials and tokens.
   - Patch code, configuration, infrastructure, or access controls.
   - Restore trusted service operation only after containment and remediation
     are complete.
   - Validate that imports, reports, and connector jobs are operating as
     expected before returning to normal operations.

6. Post-incident review

   - Document root cause, impact, timeline, actions taken, and preventive
     measures.
   - Update this plan, credentials handling, access controls, or application
     behavior when needed.

## Amazon Notification Requirement

Any security incident involving or potentially involving Amazon Information
must be reported to Amazon at `security@amazon.com` within 24 hours of
detection.

This notification requirement applies even if the investigation is not yet
complete. The initial notice should contain the best available information and
can be followed by updates as more facts become known.

## Credential Handling

- Secrets must not be committed to public or private source repositories.
- SP-API credentials, LWA secrets, refresh tokens, passwords, and access keys
  must be stored in local environment configuration or a secure secret store.
- Credentials must not be shared over chat, email, screenshots, or documents
  unless there is a specific operational need and the destination is approved.
- Credentials must be rotated after suspected exposure, unauthorized access, or
  personnel/access changes.
- Application logs must not intentionally print secrets, refresh tokens, access
  tokens, or authorization headers.

## Access Controls

- Access to Mirenelle Ops, the local database, repository, environment files,
  and Amazon connector configuration is limited to authorized operators.
- Access is granted based on operational need.
- Access should be removed when it is no longer required.
- Operator accounts should use strong passwords and multi-factor
  authentication where supported.

## Data Handling

- Amazon Information is used only for internal accounting, inventory,
  reconciliation, forecasting, and business analytics.
- Amazon Information is not sold or disclosed to third parties.
- Amazon Information is combined only with internal business records such as
  supplier invoices, product costs, inventory records, and internal operations
  settings.
- Data exports should be limited to the minimum data required for the business
  purpose.

## Review Cycle

This incident response plan must be reviewed at least every 6 months.

The plan must also be reviewed and updated when:

- Amazon SP-API roles or data access change.
- The application architecture or deployment model changes.
- New operators receive access.
- A security incident or near miss occurs.
- Amazon policy or security requirements change.

## Developer Profile Statement

Mirenelle Ops maintains an incident response plan with defined roles, 6-month
reviews, and 24-hour incident notification procedures. Security incidents
involving or potentially involving Amazon Information are reported to
`security@amazon.com` within 24 hours of detection.
