from dataclasses import dataclass

from globals import aliases


@dataclass
class ModelEvaluationMetrics:
    confusion_matrix: aliases.ConfusionMatrix
    precision_score: float
    accuracy_score: float
    specificity_score: float
    sensitivity_score: float
    f1_score: float
