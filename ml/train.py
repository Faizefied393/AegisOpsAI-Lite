import json
from pathlib import Path
import joblib
from app.ml import train
model,metrics=train()
Path('artifacts').mkdir(exist_ok=True)
joblib.dump(model,'artifacts/synthetic_classifier.joblib')
Path('artifacts/ml_metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
