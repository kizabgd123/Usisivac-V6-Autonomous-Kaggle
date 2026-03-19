#!/usr/bin/env python3
"""
Hill Climbing Ensemble Module
Optimizes ensemble weights using iterative search to maximize ROC-AUC.
Source: Chris Deotte's GNN Starter Notebook
"""

import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
from typing import Tuple, List, Optional
import warnings

warnings.filterwarnings('ignore')


def hill_climbing_ensemble(
    oof_predictions: np.ndarray,
    y_true: np.ndarray,
    n_iterations: int = 1000,
    seed: int = 42
) -> Tuple[np.ndarray, float]:
    """
    Optimize ensemble weights using hill climbing algorithm.
    
    Args:
        oof_predictions: Out-of-fold predictions from multiple models (n_samples, n_models)
        y_true: True target values
        n_iterations: Number of optimization iterations
        seed: Random seed for reproducibility
    
    Returns:
        best_weights: Optimized weights for each model
        best_score: Best ROC-AUC score achieved
    """
    np.random.seed(seed)
    
    n_models = oof_predictions.shape[1]
    
    # Initialize with equal weights
    best_weights = np.ones(n_models) / n_models
    best_score = roc_auc_score(y_true, oof_predictions @ best_weights)
    
    for i in range(n_iterations):
        # Generate candidate weights with Gaussian perturbation
        weights = best_weights + np.random.normal(0, 0.1, n_models)
        
        # Ensure non-negative weights
        weights[weights < 0] = 0
        
        # Normalize to sum to 1
        if weights.sum() > 0:
            weights = weights / weights.sum()
        else:
            # If all weights became zero, reinitialize
            weights = np.ones(n_models) / n_models
        
        # Evaluate candidate
        score = roc_auc_score(y_true, oof_predictions @ weights)
        
        # Accept if better
        if score > best_score:
            best_score = score
            best_weights = weights
            
            if (i + 1) % 100 == 0:
                print(f"  Hill Climbing: Iteration {i+1}/{n_iterations}, Score: {best_score:.6f}")
    
    return best_weights, best_score


def rank_based_ensemble(
    oof_predictions: np.ndarray,
    y_true: np.ndarray,
    model_names: Optional[List[str]] = None
) -> Tuple[np.ndarray, float, dict]:
    """
    Create ensemble using rank-based weighting with hill climbing refinement.
    
    Args:
        oof_predictions: Out-of-fold predictions (n_samples, n_models)
        y_true: True target values
        model_names: Optional list of model names
    
    Returns:
        final_weights: Final optimized weights
        final_score: Final ROC-AUC score
        ranking_info: Dictionary with model rankings and scores
    """
    n_models = oof_predictions.shape[1]
    
    # Calculate individual model scores
    individual_scores = []
    for i in range(n_models):
        score = roc_auc_score(y_true, oof_predictions[:, i])
        individual_scores.append(score)
    
    # Rank models (higher score = better rank)
    ranks = np.argsort(np.argsort(-np.array(individual_scores))) + 1  # 1 is best
    
    # Initial rank-based weights (inverse rank)
    rank_weights = 1.0 / ranks
    rank_weights = rank_weights / rank_weights.sum()
    
    rank_score = roc_auc_score(y_true, oof_predictions @ rank_weights)
    
    # Refine with hill climbing
    final_weights, final_score = hill_climbing_ensemble(
        oof_predictions, y_true, n_iterations=1000
    )
    
    # Build ranking info
    ranking_info = {
        'individual_scores': dict(
            zip(model_names or [f'Model_{i}' for i in range(n_models)], individual_scores)
        ),
        'ranks': dict(
            zip(model_names or [f'Model_{i}' for i in range(n_models)], ranks)
        ),
        'rank_weights': dict(
            zip(model_names or [f'Model_{i}' for i in range(n_models)], rank_weights)
        ),
        'final_weights': dict(
            zip(model_names or [f'Model_{i}' for i in range(n_models)], final_weights)
        ),
        'rank_score': rank_score,
        'final_score': final_score,
        'improvement': final_score - rank_score
    }
    
    return final_weights, final_score, ranking_info


def create_oof_predictions(
    models: List,
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    seed: int = 42
) -> np.ndarray:
    """
    Generate out-of-fold predictions for ensemble optimization.
    
    Args:
        models: List of trained model instances with predict_proba method
        X: Feature matrix
        y: Target vector
        n_splits: Number of CV folds
        seed: Random seed
    
    Returns:
        oof_predictions: Out-of-fold predictions (n_samples, n_models)
    """
    n_samples = X.shape[0]
    n_models = len(models)
    
    oof_predictions = np.zeros((n_samples, n_models))
    kfold = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    
    for model_idx, model in enumerate(models):
        print(f"  Generating OOF predictions for Model {model_idx + 1}/{n_models}...")
        
        for train_idx, val_idx in kfold.split(X):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train = y[train_idx]
            
            # Fit on train, predict on validation
            model.fit(X_train, y_train)
            
            if hasattr(model, 'predict_proba'):
                oof_predictions[val_idx, model_idx] = model.predict_proba(X_val)[:, 1]
            else:
                oof_predictions[val_idx, model_idx] = model.predict(X_val)
    
    return oof_predictions
