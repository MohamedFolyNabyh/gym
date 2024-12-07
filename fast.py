# from fastapi import FastAPI,Query
# from pydantic import BaseModel

# app = FastAPI()

# # تعريف نموذج البيانات
# class BodyData(BaseModel):
#     weight: float = Query(..., gt=20, lt=200, description="الوزن بالكيلوجرام")
#     height: float = Query(..., gt=1.3, lt=2.5, description="الطول بالمتر")

# # تحديث الصف ليشمل الخطة والتركيز
# class Body(BaseModel):
#     bmi: float  # مؤشر كتلة الجسم
#     category: str  # التصنيف
#     plan: str  # الخطة
#     focus: str  # التركيز

# # تعريف المسار لحساب BMI
# @app.post("/calculate_bmi")
# async def calculate_bmi(data: BodyData):
#     bmi = data.weight / (data.height ** 2)
    
#     if bmi < 18.5:
#         category = "Underweight"
#         plan = "Weight Gain"
#         focus = "Muscular Fitness"
#     elif 18.5 <= bmi < 24.9:
#         category = "Normal weight"
#         plan = "Maintain Weight"
#         focus = "Overall Fitness"
#     elif 25 <= bmi < 29.9:
#         category = "Overweight"
#         plan = "Weight Loss"
#         focus = "Cardio Fitness"
#     else:
#         category = "Obesity"
#         plan = "Weight Loss"
#         focus = "Cardio Fitness"
    
#     return Body(bmi=round(bmi, 2), category=category, plan=plan, focus=focus)


# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the BMI Calculator API!"}
from fastapi import FastAPI
from pydantic import BaseModel
# إنشاء تطبيق FastAPI
# app = FastAPI()
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=["*"],  # يسمح بالوصول من أي مصدر. قم بتقييد هذا في الإنتاج
#   allow_credentials=True,
#   allow_methods=["*"],
#   allow_headers=["*"],
# )
# # تعريف نموذج البيانات باستخدام Pydantic
# class Student(BaseModel):
#   id: int
#   name: str
#   grade: int
# # قائمة لتخزين البيانات في الذاكرة
# students = [
#   Student(id=1,name="karim ali",grade=5),
#   Student(id=2,name="khadija ahmed",grade=3),
# ]
# # قراءة جميع العناصر
# @app.get("/students/")
# def read_students():
#   return students
# # إنشاء عنصر جديد
# @app.post("/students/")
# def create_student(New_Student: Student):
#   students.append(New_Student)
#   return New_Student
# # تحديث عنصر معين بناءً على معرفه (ID) باستخدام PUT method
# @app.put("/students/{student_id}")
# def update_student(student_id: int, updated_student: Student):
#   for index, student in enumerate(students):
#       if student.id == student_id:
#           students[index] = updated_student
#           return updated_student
#   return {"error": "Student not found"}
# # حذف عنصر معين بناءً على معرفه (ID) باستخدام DELETE method
# @app.delete("/students/{student_id}")
# def delete_student(student_id: int):
#   for index, student in enumerate(students):
#       if student.id == student_id:
#           del students[index]
#           return {"message": "Student deleted"}
#   return {"error": "Student not found"}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle

# تحميل النموذج المحفوظ
with open(r'multioutput_model.pkl', 'rb') as f:
    model = pickle.load(f)

# قواميس لفك ترميز التنبؤات

# قواميس النظام الغذائي والتمارين
diet_dict = {
    0: "Vegetables: (Broccoli, Carrots, Spinach, Lettuce, Onion); Protein Intake: (Cheese, Cottage cheese, Skim Milk, Low-fat Milk, and Baru Nuts); Juice: (Fruit Juice, Aloe vera juice, Cold-pressed juice, and Watermelon juice)",
    1: "Vegetables: (Carrots, Sweet Potato, Lettuce); Protein Intake: (Red meats, poultry, fish, eggs, dairy products, legumes, and nuts); Juice: (Fruit juice, watermelon juice, carrot juice, apple juice and mango juice)",
    2: "Vegetables: (Carrots, Sweet Potato, and Lettuce); Protein Intake: (Red meats, poultry, fish, eggs, dairy products, legumes, and nuts); Juice: (Fruit juice, watermelon juice, carrot juice, apple juice and mango juice)",
    3: "Vegetables: (Garlic, Mushroom, Green Papper, Iceberg Lettuce); Protein Intake: (Baru Nuts, Beech Nuts, Hemp Seeds, Cheese Sandwich); Juice: (Apple Juice, Mango juice, and Beetroot juice)",
    4: "Vegetables: (Garlic, Roma Tomatoes, Capers and Iceberg Lettuce); Protein Intake: (Cheese Sandwich, Baru Nuts, Beech Nuts, Squash Seeds, and Mixed Teff); Juice: (Apple juice, beetroot juice and mango juice)",
    5: "Vegetables: (Garlic, Roma Tomatoes, Capers, Green Papper, and Iceberg Lettuce); Protein Intake: (Cheese Sandwich, Baru Nuts, Beech Nuts, Squash Seeds, Mixed Teff, peanut butter, and jelly sandwich); Juice: (Apple juice, beetroot juice, and mango juice)",
    6: "Vegetables: (Garlic, Mushroom, Green Papper, and Water Chestnut); Protein Intake: (Baru Nuts, Beech Nuts, and Black Walnut); Juice: (Apple juice, Mango, and Beetroot Juice)",
    7: "Vegetables: (Garlic, Mushroom, Green Papper); Protein Intake: (Baru Nuts, Beech Nuts, and Hemp Seeds); Juice: (Apple juice, Mango, and Beetroot Juice)",
    8: "Vegetables: (Mixed greens, cherry tomatoes, cucumbers, bell peppers, carrots, celery, bell peppers); Protein Intake: (Chicken, fish, tofu, or legumes); Juice: (Green juice, kale, spinach, cucumber, celery, and apple)",
    9: "Vegetables: (Tomatoes, Garlic, leafy greens, broccoli, carrots, and bell peppers); Protein Intake: (Poultry, fish, tofu, legumes, and low-fat dairy products); Juice: (Apple juice, beetroot juice and mango juice)"
}

exercise_dict = {
    0: "Brisk walking, cycling, swimming, running, or dancing.",
    1: "Squats, deadlifts, bench presses, and overhead presses.",
    2: "Squats, yoga, deadlifts, bench presses, and overhead presses.",
    3: "Walking, Yoga, Swimming.",
    4: "Brisk walking, cycling, swimming, or dancing."}
# إنشاء تطبيق FastAPI
app = FastAPI()

# نموذج إدخال البيانات
class FitnessData(BaseModel):
    sex: str
    age: int
    height: float
    weight: float
    diabetes: str
    hypertension: str

# حساب BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# تحديد الحقول بناءً على BMI
def determine_fitness_plan(bmi):
    if bmi < 18.5:
        return "Underweight", "Weight Gain", "Muscular Fitness"
    elif 18.5 <= bmi < 24.9:
        return "Normal", "Weight Gain", "Muscular Fitness"
    elif 25 <= bmi < 29.9:
        return "Overweight", "Weight Loss", "Cardio Fitness"
    else:
        return "Obese", "Weight Loss", "Cardio Fitness"
@app.post("/predict/")
async def predict(data: FitnessData):
    # حساب BMI
    bmi = calculate_bmi(data.weight, data.height)
    level, fitness_goal, fitness_type = determine_fitness_plan(bmi)

    # إعداد بيانات الإدخال للنموذج
    input_data = {
        "Sex": [1 if data.sex.lower() == 'male' else 0],
        "Age": [data.age],
        "Height": [data.height],
        "Weight": [data.weight],
        "BMI": [bmi],
        "Diabetes": [1 if data.diabetes.lower() == "yes" else 0],
        "Hypertension": [1 if data.hypertension.lower() == "yes" else 0],
        "Fitness Goal": [fitness_goal],
        "Level": [level],
        "Fitness Type": [fitness_type]
    }
    df = pd.DataFrame(input_data)

    # تحويل النصوص إلى أرقام
    df["Level"] = df["Level"].astype("category").cat.codes
    df["Fitness Goal"] = df["Fitness Goal"].astype("category").cat.codes
    df["Fitness Type"] = df["Fitness Type"].astype("category").cat.codes

    try:
        # إجراء التنبؤ
        predictions = model.predict(df)

        # فك ترميز النتائج
        diet_prediction = diet_dict.get(predictions[0][0], "Unknown") 
        exercise_prediction = exercise_dict.get(predictions[0][1], "Unknown")

        # إرجاع القيم منفصلة في الاستجابة
        return {
            "BMI": bmi,
            "Predicted Level": level,
            "Predicted Goal": fitness_goal,
            "Predicted Type": fitness_type,
            "Predicted Diet": diet_prediction,
            "Predicted Exercise": exercise_prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
