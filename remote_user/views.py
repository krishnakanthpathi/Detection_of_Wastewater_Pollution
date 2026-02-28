from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import VotingClassifier
#model selection
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
# Create your views here.
from remote_user.models import ClientRegister_Model,predict_water_type,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Predict_WasteWater_Pollution_Type(request):
    if request.method == "POST":

        if request.method == "POST":

            Fid= request.POST.get('Fid')
            Name_of_Monitoring_Location= request.POST.get('Name_of_Monitoring_Location')
            Type_Water_Body= request.POST.get('Type_Water_Body')
            State_Name= request.POST.get('State_Name')
            Temperature= request.POST.get('Temperature')
            Dissolved_Oxygen_mgperL= request.POST.get('Dissolved_Oxygen_mgperL')
            pH= request.POST.get('pH')
            Conductivity_mhospercm= request.POST.get('Conductivity_mhospercm')
            BOD_mgperL= request.POST.get('BOD_mgperL')
            NitrateN_NitriteN_mgperL= request.POST.get('NitrateN_NitriteN_mgperL')
            Fecal_Coliform_MPNper100ml= request.POST.get('Fecal_Coliform_MPNper100ml')
            Total_Coliform_MPNper100ml= request.POST.get('Total_Coliform_MPNper100ml')

        df = pd.read_csv('Datasets.csv', encoding='latin-1')


        def apply_results(results):
            if (results == 0):
                return 0
            elif (results ==1):
                return 1

        df['results'] = df['Label'].apply(apply_results)

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
        models.append(('SVM', lin_clf))

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
        models.append(('DecisionTreeClassifier', dtc))

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

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = str(pred.replace("]", ""))

        prediction = int(pred1)

        if (prediction == 0):
            val = 'No Wastewater Pollution'

        elif (prediction == 1):
            val = 'High Wastewater Pollution'


        print(prediction)
        print(val)

        predict_water_type.objects.create(
        Fid=Fid,
        Name_of_Monitoring_Location=Name_of_Monitoring_Location,
        Type_Water_Body=Type_Water_Body,
        State_Name=State_Name,
        Temperature=Temperature,
        Dissolved_Oxygen_mgperL=Dissolved_Oxygen_mgperL,
        pH=pH,
        Conductivity_mhospercm=Conductivity_mhospercm,
        BOD_mgperL=BOD_mgperL,
        NitrateN_NitriteN_mgperL=NitrateN_NitriteN_mgperL,
        Fecal_Coliform_MPNper100ml=Fecal_Coliform_MPNper100ml,
        Total_Coliform_MPNper100ml=Total_Coliform_MPNper100ml,
        Prediction=val)

        return render(request, 'RUser/Predict_WasteWater_Pollution_Type.html',{'objs': val})
    return render(request, 'RUser/Predict_WasteWater_Pollution_Type.html')



