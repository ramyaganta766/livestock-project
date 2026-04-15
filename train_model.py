import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import matplotlib.pyplot as plt

# LOAD DATA
data = pd.read_csv("livestock_dataset_with_symptoms.csv")

# 🔥 CLEAN DATA

# Remove missing values
data = data.dropna()

# Remove duplicates
data = data.drop_duplicates()

# Fix text formatting
data['Animal_Type'] = data['Animal_Type'].str.strip().str.title()
data['Vaccination_Status'] = data['Vaccination_Status'].str.strip().str.title()

# Convert categorical → numbers
animal_map = {'Cow':0,'Goat':1,'Sheep':2,'Buffalo':3,'Hen':4}
data['Animal_Type'] = data['Animal_Type'].map(animal_map)

data['Vaccination_Status'] = data['Vaccination_Status'].map({'Yes':1,'No':0})

# FEATURES
X = data[[
    'Animal_Type',
    'Age_years',
    'Fever_Detected',
    'Appetite_Loss',
    'Physical_Weakness',
    'Vaccination_Status',
    'Core_Temperature_C',
    'Surrounding_Humidity_%'
]]

# TARGET
y = data['Disease']

# SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# TRAIN MODEL
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# PREDICT
y_pred = model.predict(X_test)

# ACCURACY
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
# 📊 GRAPH
labels = ['Accuracy']
values = [accuracy * 100]

plt.bar(labels, values)
plt.title("Model Accuracy")
plt.ylabel("Percentage")
plt.ylim(0, 100)

plt.savefig("accuracy.png")
plt.show()
# SAVE MODEL
pickle.dump(model, open("model.pkl", "wb"))