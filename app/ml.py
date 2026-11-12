"""Experimental ML baseline on labeled synthetic events; not validated for real threats."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

def make_data(n=300,seed=42):
    rng=np.random.default_rng(seed)
    X=np.column_stack([rng.integers(0,12,n),rng.integers(0,2,n),rng.integers(0,2,n),rng.integers(0,101,n)])
    y=((X[:,0]>=6)|((X[:,1]==1)&(X[:,2]==1))|((X[:,3]>80)&(X[:,2]==1))).astype(int)
    return X,y

def train(seed=42):
    X,y=make_data(seed=seed)
    xtr,xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=seed,stratify=y)
    model=LogisticRegression(max_iter=500,random_state=seed).fit(xtr,ytr)
    pred=model.predict(xte)
    return model,{'precision':round(float(precision_score(yte,pred,zero_division=0)),3),
                  'recall':round(float(recall_score(yte,pred,zero_division=0)),3),
                  'f1':round(float(f1_score(yte,pred,zero_division=0)),3),
                  'test_samples':len(yte),'dataset':'synthetic rule-generated labels; illustrative only'}
