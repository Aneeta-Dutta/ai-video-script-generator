"""
Quality Evaluation for AI Video Production System.

Provides validation and quality checks for research reports and production scripts.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class QualityLevel(Enum):
    """Quality level enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    FAILED = "failed"


@dataclass
class QualityCheck:
    """Individual quality check result."""
    name: str
    passed: bool
    score: float  # 0.0 to 1.0
    message: str
    severity: str = "info"  # info, warning, error


@dataclass
class QualityReport:
    """Comprehensive quality evaluation report."""
    overall_score: float
    overall_level: QualityLevel
    checks: List[QualityCheck]
    passed: bool
    recommendations: List[str]


class QualityEvaluator:
    """Evaluates quality of research and production outputs."""
    
    def __init__(self, min_acceptable_score: float = 0.6):
        self.min_acceptable_score = min_acceptable_score
    
    def evaluate_research_report(self, report: str) -> QualityReport:
        """
        Evaluate quality of a research report.
        
        Args:
            report: Research report content
        
        Returns:
            Quality evaluation report
        """
        checks = []
        
        # Check 1: Report is not empty
        checks.append(QualityCheck(
            name="Content Presence",
            passed=len(report.strip()) > 100,
            score=1.0 if len(report.strip()) > 100 else 0.0,
            message=f"Report length: {len(report)} characters",
            severity="error" if len(report.strip()) == 0 else "info"
        ))
        
        # Check 2: Contains data/statistics
        has_data = any(keyword in report.lower() for keyword in ["data", "statistics", "percent", "%", "number"])
        checks.append(QualityCheck(
            name="Data Presence",
            passed=has_data,
            score=1.0 if has_data else 0.3,
            message="Research contains data points" if has_data else "Missing concrete data",
            severity="warning" if not has_data else "info"
        ))
        
        # Check 3: Contains narrative elements
        has_narrative = any(keyword in report.lower() for keyword in ["story", "narrative", "scene", "concept"])
        checks.append(QualityCheck(
            name="Narrative Elements",
            passed=has_narrative,
            score=1.0 if has_narrative else 0.5,
            message="Contains narrative elements" if has_narrative else "Limited narrative structure",
            severity="warning" if not has_narrative else "info"
        ))
        
        # Check 4: Reasonable length
        is_reasonable_length = 500 <= len(report) <= 10000
        checks.append(QualityCheck(
            name="Report Length",
            passed=is_reasonable_length,
            score=1.0 if is_reasonable_length else 0.7,
            message=f"Report is {len(report)} characters (target: 500-10000)",
            severity="warning" if not is_reasonable_length else "info"
        ))
        
        return self._compile_report(checks)
    
    def evaluate_production_script(self, script: str) -> QualityReport:
        """
        Evaluate quality of a production script.
        
        Args:
            script: Production script content
        
        Returns:
            Quality evaluation report
        """
        checks = []
        
        # Check 1: Script is not empty
        checks.append(QualityCheck(
            name="Content Presence",
            passed=len(script.strip()) > 100,
            score=1.0 if len(script.strip()) > 100 else 0.0,
            message=f"Script length: {len(script)} characters",
            severity="error" if len(script.strip()) == 0 else "info"
        ))
        
        # Check 2: Contains VEO prompt elements
        has_veo_elements = any(keyword in script for keyword in ["SUBJECT", "CAMERA", "LIGHTING", "style"])
        checks.append(QualityCheck(
            name="VEO Prompt Structure",
            passed=has_veo_elements,
            score=1.0 if has_veo_elements else 0.2,
            message="Contains VEO prompt elements" if has_veo_elements else "Missing VEO prompt structure",
            severity="error" if not has_veo_elements else "info"
        ))
        
        # Check 3: Contains dialogue
        has_dialogue = "dialogue" in script.lower() or "\"" in script
        checks.append(QualityCheck(
            name="Dialogue Presence",
            passed=has_dialogue,
            score=1.0 if has_dialogue else 0.6,
            message="Contains dialogue" if has_dialogue else "Limited dialogue",
            severity="warning" if not has_dialogue else "info"
        ))
        
        # Check 4: Production details
        has_production_details = any(keyword in script.lower() for keyword in ["camera", "lighting", "shot", "frame"])
        checks.append(QualityCheck(
            name="Production Details",
            passed=has_production_details,
            score=1.0 if has_production_details else 0.5,
            message="Contains production details" if has_production_details else "Missing technical specifications",
            severity="warning" if not has_production_details else "info"
        ))
        
        return self._compile_report(checks)
    
    def _compile_report(self, checks: List[QualityCheck]) -> QualityReport:
        """Compile individual checks into overall quality report."""
        # Calculate overall score
        overall_score = sum(check.score for check in checks) / len(checks) if checks else 0.0
        
        # Determine quality level
        if overall_score >= 0.9:
            level = QualityLevel.EXCELLENT
        elif overall_score >= 0.75:
            level = QualityLevel.GOOD
        elif overall_score >= self.min_acceptable_score:
            level = QualityLevel.ACCEPTABLE
        elif overall_score >= 0.3:
            level = QualityLevel.POOR
        else:
            level = QualityLevel.FAILED
        
        # Determine if passed
        passed = overall_score >= self.min_acceptable_score
        
        # Generate recommendations
        recommendations = []
        for check in checks:
            if not check.passed and check.severity in ["warning", "error"]:
                recommendations.append(f"Address {check.name}: {check.message}")
        
        return QualityReport(
            overall_score=overall_score,
            overall_level=level,
            checks=checks,
            passed=passed,
            recommendations=recommendations
        )
