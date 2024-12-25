# Charger le modèle XGBoost enregistré
import joblib
xgb_model = joblib.load('xgb_model.joblib')
# Trois nouveaux tweets à tester
new_tweets = ["The flight was amazing and the service was excellent!",
              "Bad flight, it was delayed for hours and the staff was rude.",
              "The flight was okay, nothing special."]
# Prédire les labels des nouveaux tweets
predictions = xgb_model.predict(new_tweets)
# Afficher les prédictions
for tweet, prediction in zip(new_tweets, predictions):
    print(f"Tweet: {tweet}\nPrediction: {prediction}\n")
