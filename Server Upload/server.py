from flask import Flask, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)


# method for finding elements in array whose IDs match
def find_data_by_id(array, id):
    for i in range(len(array)):
        if array[i]['id']==id:
            del(array[i])
            return array[i]
    return None

# method for updating elements in array whose IDs match
def update_data_by_id(array, id, data):
    for i in range(len(array)):
        if array[i]['id']==id:
            array[i] = data
            return
    return

# method for deleting elements in array whose IDs match
def delete_data_by_id(array, id):
    for i in range(len(array)):
        if array[i]['id']==id:
            del(array[i])
            return 
    return


# the data structure used for API return values
def response(code : int, message : str, data : any = None):
    body = {'code' : code, 'message' : message, 'data' : {}}
    if data is not None:
        if hasattr(data, '__dict__'):
            body['data'] = data.__dict__
        else:
            body['data'] = data
    return make_response(json.dumps(body, sort_keys=True, ensure_ascii=False), 200)


# the API for the login page
# param: {"name":"admin", "password":"1234"}
@app.route('/login', methods = ['POST'])
def login():
    data = json.loads(request.data)
    if "password" not in data:
        return response(1000, "Password is required!")
        #return "Password is required!"
    if "name" not in data:
        return response(1001, "Account is required")
        #return "Account is required!"
    if data["name"] == "admin" and data["password"] == "1234":
        return response(0, "LOGIN SUCCESS!")
        #return "LOGIN SUCCESS!"
    return response(1002, "Wrong account or password")
    #return "LOGIN FAILURE!"



# temporary storage for student list before we connect the backend to a database
# data structure: {"id":, "name" : , "english" : , "chinese" : , "math" : }
STUDENTS = []
STUDENTNO = 0


# API for getting the student list
@app.route('/student_list', methods = ['GET'])
def student_list():
    return response(0, "ok", STUDENTS)


# API for adding students to the list
# param {"name" : , "english" : , "chinese" : , "math" :, }
@app.route('/student_add', methods = ['POST'])
def student_add():
    global STUDENTS, STUDENTNO
    if str(request.data) == '':
        return response(1, "Invalid input")
    newStu = {"id":0, "name":'', "english":0,"chinese":0,"math":0}
    param = json.loads(request.data)
    if "name" in param:
        newStu["name"] = param["name"]
    if "english" in param:
        newStu["english"] = param["english"]
    if "chinese" in param:
        newStu["chinese"] = param["chinese"]
    if "math" in param:
        newStu["math"] = param["math"]
    STUDENTNO += 1
    newStu["id"] = STUDENTNO
    STUDENTS.append(newStu)
    return response(0, "add successful")



# API for deleting students from the list
# para {}
@app.route('/student_del', methods = ['POST'])
def student_del():
    global STUDENTS
    if str(request.data) == '':
        return response(1, "Invalid input")
    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Invalid input")
    delete_data_by_id(STUDENTS, param['id'])
    return response(0, "Deletion Successful!")



# API for modifying student information on the list
# param {"id" : , "name" : , "english" : , "chinese" : , "math" :, }
@app.route('/student_modify', methods = ['POST'])
def student_mod():
    global STUDENTS
    if str(request.data)=='':
        return response(1, "Invalid input")
    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Invalid input")
    if "name" not in param:
        return response(1, "Name required")
    stu = find_data_by_id(STUDENTS, param["id"])
    if stu is None:
        return response(1, "Student doesn't exist")
    if "name" in param:
        stu["name"] = param["name"]
    if "english" in param:
        stu["english"] = param["english"]
    if "chinese" in param:
        stu["chinese"] = param["chinese"]
    if "math" in param:
        stu["math"] = param["math"]
    update_data_by_id(STUDENTS, param["id"], stu)
    return response(0, "Successfully Modified!")




# temporary storage for teacher accounts before we connect the backend to a database
# data structure: {"id" : , "name" : , "password" : }
TEACHERS = []
TEACHERNO = 0


# API for getting the teacher accounts
@app.route('/teacher_list', methods = ['GET'])
def teacher_list():
    return response(0, "ok", TEACHERS)


# API for deleting teachers from the teachers account list 
# para {}
@app.route('/teacher_del', methods = ['POST'])
def teacher_del():
    global TEACHERS
    if str(request.data) == '':
        return response(1, "Invalid input")
    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Invalid input")
    delete_data_by_id(TEACHERS, param['id'])
    return response(0, "Deletion Successful!")


# API for adding students to the list
# param {"name" : , "password" : , }
@app.route('/teacher_add', methods = ['POST'])
def teacher_add():
    global TEACHERS, TEACHERNO
    if str(request.data) == '':
        return response(1, "Invalid input")
    newTeach = {"id" : 0, "name" : '', "password" : ''}
    param = json.loads(request.data)
    if "password" not in param:
        return response(1, "password is required")
    if "name" not in param:
        return response(1, "name is required!")

    if "name" in param:
        newTeach["name"] = param["name"]
    if "password" in param:
        newTeach["password"] = param["password"]
    TEACHERNO += 1
    TEACHERS["id"] = TEACHERNO
    TEACHERS.append(newTeach)
    return response(0, "add successful")


# API for modifying student information on the list
# param {"id" : , "name" : , "password" : }
@app.route('/teacher_modify', methods = ['POST'])
def teacher_mod():
    global TEACHERS
    if str(request.data)=='':
        return response(1, "Invalid input")
    param = json.loads(request.data)
    if "id" not in param:
        return response(1, "Invalid input")
    if "name" in param:
        if param["name"] ==  '':
            return response(1, "Name is required")
    
    tea = find_data_by_id(TEACHERS, param["id"])
    if tea is None:
        return response(1, "Student doesn't exist")
    if "name" in param:
        if param["name"] ==  '':
            return response(1, "Name is required")
        tea['name'] = param['name']
    if "password" in param:
        if param['password'] == '':
            return response(1, "Password is required")
        tea['password'] = param['password']
    update_data_by_id(STUDENTS, param["id"], tea)
    return response(0, "Successfully Modified!")


if __name__ == '__main__':
    app.run(port=9000)