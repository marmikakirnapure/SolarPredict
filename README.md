# SolarPredict

A simple Flask website that compares Linear Regression, KNN, Decision Tree and Random Forest for solar energy predictions. It shows both dataset test metrics (MAE, RMSE and R²) and predictions/savings for the user's inputs.

## Run locally

1. Install Python.
2. Open a terminal in this folder.
3. Run `python -m pip install -r requirements.txt`.
4. Run `python train_model.py`.
5. Run `python app.py`.
6. Open http://127.0.0.1:5000.

## Push to GitHub

Create an empty GitHub repository, then run these commands in this folder. Replace YOUR-USERNAME with your GitHub username.

```bash
git init
git add .
git commit -m "Add SolarPredict project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/SolarPredict.git
git push -u origin main
```

## Deploy on Render

Connect the GitHub repository to Render as a Web Service. The included `render.yaml` installs the dependencies and trains the model from the Excel dataset during build. Start command: `gunicorn app:app`.

The Nagpur area field is shown in the result but is not a model feature. The dataset is simulated educational data, so results are not a guarantee of real-world solar output.
