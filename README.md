# Safe Entry Demo App in Python

This is a demo application from GovTech where they wrote it in nodeJS to allow you to integrate your application with Safe Entry.
I have converted it into Python for users that uses Python/Django app.

Original code: https://github.com/singpass/safeentry-demo-app

## Contents

- [0. Original GovTech Safe Entry Demo Git](https://github.com/singpass/safeentry-demo-app)
- [1. Conversion Principal](#principal)
- [2. How To Use](#how-to-use)
- [3. Things To Note](#notes)
<br/>

## <a name="principal"></a>1. Conversion Principal
While converting the nodeJS application to python. I have kept the syntax and variable and line number to be as similar as possible so that you can see what code converts to what. 

It is easier to update my code when there is any update in the original code. 

## <a name="how-to-use"></a>1. How To Use

### 1.0 Python Language

Please use Python v3.x and up. If you are using Python v2.x some syntax would not work and need to be refactored again. 

To check your python version run:
```
python --version
```

### 1.1 Install pre-requisite library

Run the following command in your virtual environment where the app reside:
```
pip install -r requirement.txt
```

### 1.2 Running the Application

Execute the following command to call the Entry API:

To test with payload encryption and signing.
```
python index.js test entry
```

To test the code in production with payload encryption and signing.
```
python index.js production entry
```

To test without payload encryption and signing.
```
python index.js sandbox entry
```

## <a name="notes"></a>2. Things To Note

### 2.1 Configuration
Note the following files to change configuration to live data

| File |Configs|
|---|---|
|`index.py`| Sample checkin or checkout data |
|`config.py`| Application ID (AppId) and certificates|

### 2.2 Substantial Differences with original code 
Note that the following files have significant differences with the original code. I may update them in the future.

| File |Major Difference|
|---|---|
|`requestHandler.py`| original code uses Promise which makes the request call asynchronous. This python code uses a synchronous request call. |