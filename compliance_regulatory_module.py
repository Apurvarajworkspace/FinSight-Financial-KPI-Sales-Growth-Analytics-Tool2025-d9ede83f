"""
Compliance & Regulatory Reporting Module
Handles GDPR, SOX, regulatory compliance tracking and automated reports
"""

import pandas as pd
from datetime import datetime, timedelta
import json


class ComplianceFramework:
    """Framework for managing compliance requirements"""
    
    def __init__(self):
        self.requirements = {}
        self.audit_trail = []
        self.compliance_status = {}
    
    def register_requirement(self, req_id, name, framework, description, deadline=None):
        """Register a compliance requirement"""
        self.requirements[req_id] = {
            'name': name,
            'framework': framework,  # GDPR, SOX, HIPAA, etc.
            'description': description,
            'deadline': deadline,
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        self.compliance_status[req_id] = 'not_started'
        return {'status': 'registered', 'requirement_id': req_id}
    
    def log_audit_event(self, event_type, description, user, changes=None):
        """Log audit event for compliance trail"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'description': description,
            'user': user,
            'changes': changes or {},
            'event_id': len(self.audit_trail) + 1
        }
        self.audit_trail.append(event)
        return event
    
    def get_audit_trail(self, days=30):
        """Retrieve audit trail for specified period"""
        cutoff = datetime.now() - timedelta(days=days)
        relevant_events = [e for e in self.audit_trail 
                          if datetime.fromisoformat(e['timestamp']) > cutoff]
        return {
            'period_days': days,
            'total_events': len(relevant_events),
            'events': relevant_events
        }
    
    def update_compliance_status(self, req_id, status):
        """Update compliance status for requirement"""
        if req_id in self.requirements:
            self.compliance_status[req_id] = status
            self.requirements[req_id]['status'] = status
            return {'requirement_id': req_id, 'new_status': status}
        return None


class GDPRCompliance:
    """GDPR-specific compliance management"""
    
    def __init__(self):
        self.data_processing_agreements = {}
        self.data_breaches = []
        self.consent_records = {}
        self.data_retention_policies = {}
    
    def create_data_processing_agreement(self, agreement_id, parties, data_types, purpose):
        """Create and track data processing agreements"""
        self.data_processing_agreements[agreement_id] = {
            'parties': parties,
            'data_types': data_types,
            'purpose': purpose,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        return {'status': 'agreement_created', 'agreement_id': agreement_id}
    
    def record_consent(self, user_id, consent_type, status, timestamp=None):
        """Record user consent for data processing"""
        if user_id not in self.consent_records:
            self.consent_records[user_id] = []
        
        record = {
            'user_id': user_id,
            'consent_type': consent_type,
            'status': status,
            'timestamp': timestamp or datetime.now().isoformat(),
            'record_id': len(self.consent_records[user_id])
        }
        self.consent_records[user_id].append(record)
        return record
    
    def report_data_breach(self, breach_id, description, affected_records, severity):
        """Report and track data breach incidents"""
        breach = {
            'breach_id': breach_id,
            'description': description,
            'affected_records': affected_records,
            'severity': severity,  # low, medium, high, critical
            'reported_at': datetime.now().isoformat(),
            'status': 'reported'
        }
        self.data_breaches.append(breach)
        return breach
    
    def set_retention_policy(self, data_type, retention_days):
        """Set data retention policy"""
        self.data_retention_policies[data_type] = {
            'retention_days': retention_days,
            'effective_date': datetime.now().isoformat()
        }
        return {'status': 'policy_set', 'data_type': data_type, 'retention_days': retention_days}
    
    def get_gdpr_compliance_report(self):
        """Generate GDPR compliance report"""
        return {
            'report_date': datetime.now().isoformat(),
            'data_processing_agreements': len(self.data_processing_agreements),
            'consent_records': len(self.consent_records),
            'data_breaches': len(self.data_breaches),
            'retention_policies': len(self.data_retention_policies),
            'breach_summary': self._get_breach_summary()
        }
    
    def _get_breach_summary(self):
        """Summarize data breaches by severity"""
        summary = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        for breach in self.data_breaches:
            summary[breach['severity']] += 1
        return summary


class SOXCompliance:
    """SOX (Sarbanes-Oxley) compliance management"""
    
    def __init__(self):
        self.internal_controls = {}
        self.risk_assessments = {}
        self.attestations = {}
        self.internal_audits = []
    
    def define_internal_control(self, control_id, objective, responsibility, frequency):
        """Define and track internal controls"""
        self.internal_controls[control_id] = {
            'objective': objective,
            'responsibility': responsibility,
            'frequency': frequency,
            'last_tested': None,
            'status': 'active'
        }
        return {'status': 'control_defined', 'control_id': control_id}
    
    def assess_risk(self, risk_id, category, description, likelihood, impact):
        """Perform risk assessment"""
        risk_score = (likelihood * 10) * (impact * 10) / 100
        self.risk_assessments[risk_id] = {
            'category': category,
            'description': description,
            'likelihood': likelihood,  # 1-5
            'impact': impact,  # 1-5
            'risk_score': risk_score,
            'assessment_date': datetime.now().isoformat()
        }
        return {'status': 'risk_assessed', 'risk_id': risk_id, 'risk_score': risk_score}
    
    def record_attestation(self, attestation_id, control_id, effectiveness, evidence):
        """Record management attestation"""
        self.attestations[attestation_id] = {
            'control_id': control_id,
            'effectiveness': effectiveness,  # effective/ineffective
            'evidence': evidence,
            'attested_at': datetime.now().isoformat(),
            'status': 'recorded'
        }
        return {'status': 'attestation_recorded', 'attestation_id': attestation_id}
    
    def conduct_internal_audit(self, audit_id, scope, findings, remediation):
        """Conduct and record internal audit"""
        audit = {
            'audit_id': audit_id,
            'scope': scope,
            'findings': findings,
            'remediation': remediation,
            'conducted_at': datetime.now().isoformat(),
            'status': 'completed'
        }
        self.internal_audits.append(audit)
        return audit
    
    def get_sox_compliance_report(self):
        """Generate SOX compliance report"""
        effective_controls = sum(1 for a in self.attestations.values() 
                                if a['effectiveness'] == 'effective')
        return {
            'report_date': datetime.now().isoformat(),
            'internal_controls': len(self.internal_controls),
            'risk_assessments': len(self.risk_assessments),
            'attestations': len(self.attestations),
            'effective_controls': effective_controls,
            'internal_audits': len(self.internal_audits),
            'avg_risk_score': self._avg_risk_score()
        }
    
    def _avg_risk_score(self):
        """Calculate average risk score"""
        if not self.risk_assessments:
            return 0
        scores = [r['risk_score'] for r in self.risk_assessments.values()]
        return sum(scores) / len(scores)


class RegulatoryReportGenerator:
    """Generate regulatory compliance reports"""
    
    def __init__(self, gdpr, sox, framework):
        self.gdpr = gdpr
        self.sox = sox
        self.framework = framework
    
    def generate_compliance_dashboard(self):
        """Generate comprehensive compliance dashboard"""
        gdpr_report = self.gdpr.get_gdpr_compliance_report()
        sox_report = self.sox.get_sox_compliance_report()
        
        total_requirements = len(self.framework.requirements)
        compliant = sum(1 for s in self.framework.compliance_status.values() if s == 'compliant')
        
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_compliance_rate': (compliant / total_requirements * 100) if total_requirements else 0,
            'gdpr': gdpr_report,
            'sox': sox_report,
            'audit_trail_events': len(self.framework.audit_trail),
            'outstanding_requirements': total_requirements - compliant
        }
    
    def generate_audit_report(self, days=90):
        """Generate audit report for specified period"""
        audit_data = self.framework.get_audit_trail(days=days)
        return {
            'report_date': datetime.now().isoformat(),
            'audit_period_days': days,
            'total_events': audit_data['total_events'],
            'events_by_type': self._group_events_by_type(audit_data['events']),
            'events_by_user': self._group_events_by_user(audit_data['events'])
        }
    
    def _group_events_by_type(self, events):
        """Group audit events by type"""
        grouped = {}
        for event in events:
            event_type = event['type']
            grouped[event_type] = grouped.get(event_type, 0) + 1
        return grouped
    
    def _group_events_by_user(self, events):
        """Group audit events by user"""
        grouped = {}
        for event in events:
            user = event['user']
            grouped[user] = grouped.get(user, 0) + 1
        return grouped


def run_compliance_demo():
    """Demo function for compliance & regulatory reporting"""
    print("\n" + "="*70)
    print("COMPLIANCE & REGULATORY REPORTING DEMO")
    print("="*70)
    
    # Initialize compliance systems
    framework = ComplianceFramework()
    gdpr = GDPRCompliance()
    sox = SOXCompliance()
    reporter = RegulatoryReportGenerator(gdpr, sox, framework)
    
    # 1. Register compliance requirements
    print("\n[1] Registering Compliance Requirements...")
    print("-" * 70)
    framework.register_requirement('REQ-001', 'Customer Data Protection', 'GDPR', 'Protect customer PII')
    framework.register_requirement('REQ-002', 'Financial Controls', 'SOX', 'Internal control testing')
    framework.register_requirement('REQ-003', 'Audit Trail', 'GDPR', 'Maintain 6-year audit trail')
    print("[DONE] Requirements registered: 3")
    print("[DONE] Frameworks: GDPR (2), SOX (1)")
    
    # 2. GDPR compliance tracking
    print("\n[2] GDPR Compliance Tracking...")
    print("-" * 70)
    gdpr.create_data_processing_agreement('DPA-001', ['Company', 'Processor'], ['Customer Names', 'Email'], 'Marketing')
    gdpr.record_consent('USER-001', 'marketing', 'given')
    gdpr.record_consent('USER-002', 'marketing', 'withdrawn')
    gdpr.set_retention_policy('customer_data', 365)
    print("[DONE] Data Processing Agreements: 1")
    print("[DONE] Consent Records: 2")
    print("[DONE] Retention Policies: 1")
    
    # 3. SOX compliance tracking
    print("\n[3] SOX Compliance Tracking...")
    print("-" * 70)
    sox.define_internal_control('IC-001', 'Revenue Recognition', 'Finance', 'monthly')
    sox.assess_risk('RISK-001', 'Financial', 'Inaccurate revenue', 4, 5)
    sox.record_attestation('ATT-001', 'IC-001', 'effective', 'Tested and verified')
    print("[DONE] Internal Controls Defined: 1")
    print("[DONE] Risk Assessments: 1")
    print("[DONE] Attestations Recorded: 1")
    
    # 4. Audit trail logging
    print("\n[4] Audit Trail & Logging...")
    print("-" * 70)
    framework.log_audit_event('data_access', 'Customer report accessed', 'john.doe@company.com')
    framework.log_audit_event('data_modification', 'Customer record updated', 'jane.smith@company.com')
    framework.update_compliance_status('REQ-001', 'compliant')
    print("[DONE] Audit Events Logged: 2")
    print("[DONE] Compliance Status Updated")
    
    # 5. Generate compliance dashboard
    print("\n[5] Compliance Dashboard...")
    print("-" * 70)
    dashboard = reporter.generate_compliance_dashboard()
    print(f"[DONE] Overall Compliance Rate: {dashboard['overall_compliance_rate']:.1f}%")
    print(f"[DONE] Outstanding Requirements: {dashboard['outstanding_requirements']}")
    print(f"[DONE] GDPR: {dashboard['gdpr']['consent_records']} consent records, {dashboard['gdpr']['data_processing_agreements']} agreements")
    print(f"[DONE] SOX: {dashboard['sox']['internal_controls']} controls, {dashboard['sox']['attestations']} attestations")
    
    print("\n" + "="*70)
    print("[DONE] COMPLIANCE & REGULATORY DEMO COMPLETED")
    print("="*70)
