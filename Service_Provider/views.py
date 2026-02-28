
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import CountVectorizer


from sklearn.tree import DecisionTreeClassifier
#model selection
from sklearn.metrics import confusion_matrix, accuracy_score,classification_report

# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_water_type,detection_ratio,detection_accuracy


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "admin" and password =="admin":
            detection_accuracy.objects.all().delete()
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def View_Prediction_Of_WasteWater_Pollution_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    rratio = ""
    kword = 'High Wastewater Pollution'
    print(kword)
    obj = predict_water_type.objects.all().filter(Q(Prediction=kword))
    obj1 = predict_water_type.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'No Wastewater Pollution'
    print(kword1)
    obj1 = predict_water_type.objects.all().filter(Q(Prediction=kword1))
    obj11 = predict_water_type.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)


    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_WasteWater_Pollution_Type_Ratio.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = predict_water_type.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_Of_WasteWater_Pollution_Type(request):
    obj =predict_water_type.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_WasteWater_Pollution_Type.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Predicted_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Data.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = predict_water_type.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.Name_of_Monitoring_Location, font_style)
        ws.write(row_num, 2, my_row.Type_Water_Body, font_style)
        ws.write(row_num, 3, my_row.State_Name, font_style)
        ws.write(row_num, 4, my_row.Temperature, font_style)
        ws.write(row_num, 5, my_row.Dissolved_Oxygen_mgperL, font_style)
        ws.write(row_num, 6, my_row.pH, font_style)
        ws.write(row_num, 7, my_row.Conductivity_mhospercm, font_style)
        ws.write(row_num, 8, my_row.BOD_mgperL, font_style)
        ws.write(row_num, 9, my_row.NitrateN_NitriteN_mgperL, font_style)
        ws.write(row_num, 10, my_row.Fecal_Coliform_MPNper100ml, font_style)
        ws.write(row_num, 11, my_row.Total_Coliform_MPNper100ml, font_style)
        ws.write(row_num, 12, my_row.Prediction, font_style)


    wb.save(response)
    return response

def train_model(request):
    detection_accuracy.objects.all().delete()

    df = pd.read_csv('Datasets.csv',encoding='latin-1')

    def apply_response(Label):
        if (Label == 0):
            return 0  # No Wastewater Pollution
        elif (Label == 1):
            return 1  # High Wastewater Pollution

    df['results'] = df['Label'].apply(apply_response)


    X = df['Fid']
    y = df['results']

    cv = CountVectorizer()
    x = cv.fit_transform(X)


    models = []
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20)
    X_train.shape, X_test.shape, y_train.shape

    print("Random Forest Classifier")
    from sklearn.ensemble import RandomForestClassifier
    rf_clf = RandomForestClassifier()
    rf_clf.fit(X_train, y_train)
    rfpredict = rf_clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, rfpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, rfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, rfpredict))
    models.append(('RandomForestClassifier', rf_clf))
    detection_accuracy.objects.create(names="Random Forest Classifier", ratio=accuracy_score(y_test, rfpredict) * 100)

    print("Artificial Neural Networks--ANN")
    from sklearn.neural_network import MLPClassifier
    mlpc = MLPClassifier().fit(X_train, y_train)
    y_pred = mlpc.predict(X_test)
    testscore_mlpc = accuracy_score(y_test, y_pred)
    accuracy_score(y_test, y_pred)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('MLPClassifier', mlpc))
    detection_accuracy.objects.create(names="Artificial Neural Networks--ANN",
                                      ratio=accuracy_score(y_test, y_pred) * 100)

    # SVM Model
    print("SVM")
    from sklearn import svm

    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print("ACCURACY")
    print(svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)

    print("Decision Tree Classifier")
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    dtcpredict = dtc.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, dtcpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, dtcpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, dtcpredict))
    detection_accuracy.objects.create(names="Decision Tree Classifier", ratio=accuracy_score(y_test, dtcpredict) * 100)


    print("KNeighborsClassifier")
    from sklearn.neighbors import KNeighborsClassifier
    kn = KNeighborsClassifier()
    kn.fit(X_train, y_train)
    knpredict = kn.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, knpredict) * 100)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, knpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, knpredict))
    models.append(('KNeighborsClassifier', kn))
    detection_accuracy.objects.create(names="KNeighborsClassifier", ratio=accuracy_score(y_test, knpredict) * 100)


    labeled = 'Predicted_data.csv'
    df.to_csv(labeled, index=False)
    df.to_markdown

    obj = detection_accuracy.objects.all()
    return render(request,'SProvider/train_model.html', {'objs': obj})