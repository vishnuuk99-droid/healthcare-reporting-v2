# CMS Requirements Full Traceability Report

## 1. Analytics Model Coverage Report

| Requirement | Present in Analytics | Supporting Fact Tables | Supporting Dimensions |
|---|---|---|---|
| Total number of grievances | ✅ | FactObservation | None |
| Total number of timely notifications of grievance decisions | ✅ | FactObservation | None |
| Number of expedited grievances | ✅ | FactObservation | None |
| Number of dismissed grievances | ✅ | FactObservation | None |
| Number of completed organization determinations (fully favorable, partially favorable, adverse) | ✅ | FactObservation, FactEncounter, FactProcedure, FactMedication | DimOrganization, DimCondition |
| Number of completed reconsiderations (fully favorable, partially favorable, adverse) | ✅ | FactObservation | None |
| Number of withdrawn coverage requests | ✅ | FactObservation, FactMedication | None |
| Number of dismissed coverage requests | ✅ | FactObservation, FactMedication | None |
| Number of reopened organization determinations and reconsiderations | ✅ | FactObservation, FactEncounter, FactProcedure, FactMedication | DimOrganization, DimCondition |
| Employer Group Plan Sponsor enrollment count as of the last day of the reporting period | ✅ | FactEncounter | DimPatient, DimOrganization, DimDate |
| SNP Care Management: Number of eligible enrollees (Element A) | ✅ | FactEncounter, FactProcedure | DimPatient, DimCondition |
| SNP Care Management: Number of enrollees eligible for an annual reassessment (Element B) | ✅ | FactEncounter, FactProcedure | DimPatient, DimCondition |
| SNP Care Management: Number of initial HRAs completed (Element C) | ✅ | FactObservation | None |
| SNP Care Management: Number of initial HRAs refused (Element D) | ✅ | FactObservation | None |
| SNP Care Management: Number of initial HRAs where enrollee was unable to be reached (Element E) | ✅ | FactObservation, FactEncounter, FactProcedure | DimPatient, DimCondition |
| SNP Care Management: Number of reassessments completed (Element F) | ✅ | FactObservation | None |
| SNP Care Management: Number of reassessments refused (Element G) | ✅ | None | None |
| SNP Care Management: Number of reassessments where enrollee was unable to be reached (Element H) | ✅ | FactEncounter, FactProcedure | DimPatient, DimCondition |
| Total number of enrollment requests | ✅ | FactMedication | DimPatient |
| Total number of enrollment requests requiring additional information | ✅ | FactMedication | DimPatient |
| Total number of voluntary disenrollment transactions | ✅ | None | DimPatient |
| Rewards and Incentives Programs: Number of currently enrolled members (Element G) | ✅ | FactRewardsAndIncentives | DimPatient |
| Rewards and Incentives Programs: Number of rewards made so far (Element H) | ✅ | FactRewardsAndIncentives | None |
| Payments to Providers: Total actual payments made to contracted providers (Element A) | ✅ | FactObservation | DimProvider |
| Payments to Providers: Payments by value-based payment categories (Categories 1, 2, 3, and 4) | ✅ | FactObservation | DimProvider |
| Supplemental Benefit Utilization and Costs: Unique count of eligible enrollees (Element H) | ✅ | FactEncounter, FactProcedure | DimPatient, DimOrganization, DimCondition |
| Supplemental Benefit Utilization and Costs: Number of enrollees utilizing benefit (Element I) | ✅ | FactEncounter, FactProcedure | DimPatient, DimOrganization, DimCondition |
| Supplemental Benefit Utilization and Costs: Units of utilization (Element G) | ✅ | FactProcedure | DimOrganization |
| Supplemental Benefit Utilization and Costs: Total net amount incurred by the plan (Element L) | ✅ | FactObservation, FactProcedure | DimOrganization |
| Supplemental Benefit Utilization and Costs: Total enrollee out-of-pocket costs (Element O) | ✅ | FactObservation, FactEncounter, FactProcedure | DimPatient, DimOrganization, DimCondition |
| D-SNP Enrollee Advisory Committee (EAC): Count of EAC meetings (Element B) | ✅ | FactEncounter, FactProcedure | DimPatient, DimOrganization, DimCondition |
| D-SNP Transmission of Admission Notifications: Count of hospital and SNF admissions (Element A) | ✅ | FactEncounter | DimOrganization |
| D-SNP Transmission of Admission Notifications: Count of notifications to the state or state-designated entity (Element B) | ✅ | FactEncounter | DimPatient, DimOrganization |

## 2. Requirement Survival Analysis

| Stage | Surviving Requirements | Survival % | Stage Loss % |
|---|---|---|---|
| Requirement Extraction | 33 | 100.0% | 0.0% |
| FHIR Mapping | 33 | 100.0% | 0.0% |
| Analytics Model | 33 | 100.0% | 0.0% |
| Reporting Intent | 33 | 100.0% | 0.0% |
| Report Definition | 33 | 100.0% | 0.0% |
| Measures | 33 | 100.0% | 0.0% |
| DAX | 33 | 100.0% | 0.0% |
| PBIP | 33 | 100.0% | 0.0% |

## 3. Requirement Loss Report

| Requirement | Point of Failure | Root Cause |
|---|---|---|

## 4. Summary Traceability Table

| Requirement | FHIR Mapping | Analytics Model | Reporting Intent | Report Definition | Measures | DAX | PBIP |
|---|---|---|---|---|---|---|---|
| Total number of grievances | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Total number of timely notifications of grievance decisions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of expedited grievances | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of dismissed grievances | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of completed organization determinations (fully favorable, partially favorable, adverse) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of completed reconsiderations (fully favorable, partially favorable, adverse) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of withdrawn coverage requests | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of dismissed coverage requests | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Number of reopened organization determinations and reconsiderations | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Employer Group Plan Sponsor enrollment count as of the last day of the reporting period | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of eligible enrollees (Element A) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of enrollees eligible for an annual reassessment (Element B) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of initial HRAs completed (Element C) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of initial HRAs refused (Element D) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of initial HRAs where enrollee was unable to be reached (Element E) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of reassessments completed (Element F) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of reassessments refused (Element G) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SNP Care Management: Number of reassessments where enrollee was unable to be reached (Element H) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Total number of enrollment requests | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Total number of enrollment requests requiring additional information | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Total number of voluntary disenrollment transactions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rewards and Incentives Programs: Number of currently enrolled members (Element G) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rewards and Incentives Programs: Number of rewards made so far (Element H) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Payments to Providers: Total actual payments made to contracted providers (Element A) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Payments to Providers: Payments by value-based payment categories (Categories 1, 2, 3, and 4) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Supplemental Benefit Utilization and Costs: Unique count of eligible enrollees (Element H) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Supplemental Benefit Utilization and Costs: Number of enrollees utilizing benefit (Element I) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Supplemental Benefit Utilization and Costs: Units of utilization (Element G) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Supplemental Benefit Utilization and Costs: Total net amount incurred by the plan (Element L) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Supplemental Benefit Utilization and Costs: Total enrollee out-of-pocket costs (Element O) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| D-SNP Enrollee Advisory Committee (EAC): Count of EAC meetings (Element B) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| D-SNP Transmission of Admission Notifications: Count of hospital and SNF admissions (Element A) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| D-SNP Transmission of Admission Notifications: Count of notifications to the state or state-designated entity (Element B) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
