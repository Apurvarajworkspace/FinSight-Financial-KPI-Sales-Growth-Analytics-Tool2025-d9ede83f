"""
Automation & Job Scheduling Module
Schedule and manage automated tasks and workflows
"""

import pandas as pd
from datetime import datetime, timedelta
import json


class JobScheduler:
    """Schedule automated jobs and tasks"""
    
    def __init__(self):
        self.jobs = {}
        self.job_history = []
        self.execution_log = []
    
    def schedule_job(self, job_name, job_type, schedule, parameters=None):
        """Schedule a new job"""
        job_id = f"job_{int(datetime.now().timestamp())}"
        self.jobs[job_id] = {
            'job_id': job_id,
            'name': job_name,
            'type': job_type,  # data_export, report_generation, model_training, etc.
            'schedule': schedule,  # cron expression or interval
            'parameters': parameters or {},
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'next_run': self._calculate_next_run(schedule),
            'last_run': None,
            'execution_count': 0
        }
        return {'status': 'scheduled', 'job_id': job_id}
    
    def _calculate_next_run(self, schedule):
        """Calculate next run time from schedule"""
        # Simple implementation - in production would use APScheduler or similar
        return (datetime.now() + timedelta(hours=1)).isoformat()
    
    def execute_job(self, job_id):
        """Execute a scheduled job"""
        if job_id not in self.jobs:
            return {'status': 'error', 'message': 'Job not found'}
        
        job = self.jobs[job_id]
        execution = {
            'job_id': job_id,
            'execution_id': f"exec_{int(datetime.now().timestamp())}",
            'started_at': datetime.now().isoformat(),
            'status': 'running',
            'result': None,
            'duration_ms': 0
        }
        
        # Simulate job execution
        result = f"Job {job['name']} executed successfully"
        execution['status'] = 'completed'
        execution['result'] = result
        execution['duration_ms'] = int(np.random.normal(500, 100))
        execution['completed_at'] = datetime.now().isoformat()
        
        job['last_run'] = datetime.now().isoformat()
        job['execution_count'] += 1
        job['next_run'] = self._calculate_next_run(job['schedule'])
        
        self.execution_log.append(execution)
        return execution
    
    def get_job_status(self, job_id):
        """Get status of a job"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        return {
            'job_id': job_id,
            'name': job['name'],
            'status': job['status'],
            'next_run': job['next_run'],
            'last_run': job['last_run'],
            'execution_count': job['execution_count']
        }
    
    def disable_job(self, job_id):
        """Disable a scheduled job"""
        if job_id in self.jobs:
            self.jobs[job_id]['status'] = 'disabled'
            return {'status': 'disabled', 'job_id': job_id}
        return None
    
    def get_job_execution_history(self, job_id, limit=10):
        """Get execution history for a job"""
        executions = [e for e in self.execution_log if e['job_id'] == job_id]
        return sorted(executions, key=lambda x: x['started_at'], reverse=True)[:limit]


class WorkflowOrchestrator:
    """Orchestrate complex multi-step workflows"""
    
    def __init__(self):
        self.workflows = {}
        self.workflow_executions = {}
    
    def create_workflow(self, workflow_name, description, steps):
        """Create a workflow with multiple steps"""
        workflow_id = f"wf_{int(datetime.now().timestamp())}"
        self.workflows[workflow_id] = {
            'workflow_id': workflow_id,
            'name': workflow_name,
            'description': description,
            'steps': steps,  # List of step definitions
            'created_at': datetime.now().isoformat(),
            'total_runs': 0,
            'successful_runs': 0
        }
        return {'status': 'created', 'workflow_id': workflow_id}
    
    def execute_workflow(self, workflow_id):
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        execution_id = f"wf_exec_{int(datetime.now().timestamp())}"
        
        execution = {
            'execution_id': execution_id,
            'workflow_id': workflow_id,
            'started_at': datetime.now().isoformat(),
            'status': 'running',
            'steps_completed': 0,
            'total_steps': len(workflow['steps']),
            'step_results': []
        }
        
        # Execute each step
        success = True
        for step_index, step in enumerate(workflow['steps']):
            step_result = {
                'step_index': step_index,
                'step_name': step.get('name'),
                'status': 'completed',
                'started_at': datetime.now().isoformat(),
                'completed_at': datetime.now().isoformat()
            }
            execution['step_results'].append(step_result)
            execution['steps_completed'] += 1
            
            # Check for failure
            if not success:
                execution['status'] = 'failed'
                break
        
        execution['completed_at'] = datetime.now().isoformat()
        if execution['status'] != 'failed':
            execution['status'] = 'completed'
            workflow['successful_runs'] += 1
        
        workflow['total_runs'] += 1
        self.workflow_executions[execution_id] = execution
        
        return execution
    
    def get_workflow_status(self, workflow_id):
        """Get workflow status"""
        if workflow_id not in self.workflows:
            return None
        
        workflow = self.workflows[workflow_id]
        return {
            'workflow_id': workflow_id,
            'name': workflow['name'],
            'total_runs': workflow['total_runs'],
            'successful_runs': workflow['successful_runs'],
            'success_rate': (workflow['successful_runs'] / workflow['total_runs'] * 100) if workflow['total_runs'] else 0
        }


class AlertingRules:
    """Define and manage alerting rules for automated actions"""
    
    def __init__(self):
        self.rules = {}
        self.triggered_alerts = []
    
    def create_rule(self, rule_name, condition, action, threshold):
        """Create an alerting rule"""
        rule_id = f"rule_{int(datetime.now().timestamp())}"
        self.rules[rule_id] = {
            'rule_id': rule_id,
            'name': rule_name,
            'condition': condition,  # metric, comparison operator, threshold
            'action': action,  # send_email, trigger_job, create_ticket
            'threshold': threshold,
            'created_at': datetime.now().isoformat(),
            'enabled': True,
            'times_triggered': 0
        }
        return {'status': 'created', 'rule_id': rule_id}
    
    def evaluate_rules(self, metric_name, metric_value):
        """Evaluate all rules against a metric"""
        triggered = []
        for rule_id, rule in self.rules.items():
            if not rule['enabled']:
                continue
            
            # Simple evaluation
            if rule['condition'] == 'greater_than' and metric_value > rule['threshold']:
                triggered.append(self._trigger_rule(rule_id, metric_name, metric_value))
            elif rule['condition'] == 'less_than' and metric_value < rule['threshold']:
                triggered.append(self._trigger_rule(rule_id, metric_name, metric_value))
        
        return triggered
    
    def _trigger_rule(self, rule_id, metric_name, metric_value):
        """Execute rule action"""
        rule = self.rules[rule_id]
        alert = {
            'rule_id': rule_id,
            'triggered_at': datetime.now().isoformat(),
            'metric': metric_name,
            'metric_value': metric_value,
            'action': rule['action'],
            'status': 'triggered'
        }
        self.triggered_alerts.append(alert)
        rule['times_triggered'] += 1
        return alert
    
    def get_alert_history(self):
        """Get alert history"""
        return {
            'total_alerts': len(self.triggered_alerts),
            'alerts': self.triggered_alerts
        }


import numpy as np

def run_automation_scheduling_demo():
    """Demo function for automation and scheduling"""
    print("\n" + "="*70)
    print("AUTOMATION & JOB SCHEDULING DEMO")
    print("="*70)
    
    # Initialize automation systems
    scheduler = JobScheduler()
    orchestrator = WorkflowOrchestrator()
    alerts = AlertingRules()
    
    # 1. Job scheduling
    print("\n[1] Job Scheduling...")
    print("-" * 70)
    job1 = scheduler.schedule_job('daily_report', 'report_generation', 'daily_08:00')
    job2 = scheduler.schedule_job('hourly_export', 'data_export', 'hourly')
    job3 = scheduler.schedule_job('weekly_model_train', 'model_training', 'weekly_sunday')
    print(f"[DONE] Jobs Scheduled: 3")
    print(f"[DONE] Types: report_generation, data_export, model_training")
    
    # 2. Job execution
    print("\n[2] Job Execution...")
    print("-" * 70)
    job_ids = ['job_' + str(int(datetime.now().timestamp())) for _ in range(3)]
    # Recreate jobs with proper IDs
    scheduler.jobs.clear()
    j1 = scheduler.schedule_job('daily_report', 'report_generation', 'daily')
    j2 = scheduler.schedule_job('hourly_export', 'data_export', 'hourly')
    
    job_ids = list(scheduler.jobs.keys())
    for job_id in job_ids[:2]:
        result = scheduler.execute_job(job_id)
        if result:
            print(f"[DONE] Job Executed: {result['execution_id']}")
    
    # 3. Workflow orchestration
    print("\n[3] Workflow Orchestration...")
    print("-" * 70)
    steps = [
        {'name': 'Data Extraction', 'type': 'extract'},
        {'name': 'Data Transformation', 'type': 'transform'},
        {'name': 'Data Loading', 'type': 'load'},
        {'name': 'Report Generation', 'type': 'report'}
    ]
    workflow = orchestrator.create_workflow('ETL_Pipeline', 'Extract-Transform-Load', steps)
    workflow_id = workflow['workflow_id']
    
    execution = orchestrator.execute_workflow(workflow_id)
    print(f"[DONE] Workflow Executed: {execution['execution_id']}")
    print(f"[DONE] Steps Completed: {execution['steps_completed']}/{execution['total_steps']}")
    print(f"[DONE] Status: {execution['status']}")
    
    # 4. Alerting rules
    print("\n[4] Alerting Rules...")
    print("-" * 70)
    alerts.create_rule('high_error_rate', 'greater_than', 'send_email', 0.05)
    alerts.create_rule('low_revenue', 'less_than', 'trigger_job', 50000)
    alerts.create_rule('cpu_high', 'greater_than', 'scale_up', 80)
    print(f"[DONE] Rules Created: 3")
    
    # Evaluate rules
    triggered = alerts.evaluate_rules('error_rate', 0.08)
    triggered += alerts.evaluate_rules('revenue', 40000)
    alert_hist = alerts.get_alert_history()
    print(f"[DONE] Alerts Triggered: {alert_hist['total_alerts']}")
    
    # 5. Scheduler dashboard
    print("\n[5] Scheduler Dashboard...")
    print("-" * 70)
    print(f"[DONE] Active Jobs: {len([j for j in scheduler.jobs.values() if j['status'] == 'active'])}")
    print(f"[DONE] Total Executions: {len(scheduler.execution_log)}")
    print(f"[DONE] Active Workflows: {len(orchestrator.workflows)}")
    print(f"[DONE] Enabled Rules: {len([r for r in alerts.rules.values() if r['enabled']])}")
    
    print("\n" + "="*70)
    print("[DONE] AUTOMATION & SCHEDULING DEMO COMPLETED")
    print("="*70)
