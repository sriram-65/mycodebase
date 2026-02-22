from flask import Flask , Blueprint , request , jsonify
from api.uploader import PROBLEMS_SECTIONS , Run_Code
from db.db import PROBLMES


Api = Blueprint("Api" , __name__)


@Api.route("/" , defaults={"p_name":None})
@Api.route("/<p_name>")
def Show_Problem(p_name):
    try:
       if p_name is None:
           p = PROBLMES.find({} , {"_id":0 , "problems":0})
           data = []
           for i in p:
               data.append(i)
        
           return jsonify({"success":True , "data":data})
       
       p_name = p_name.capitalize()
       if p_name not in PROBLEMS_SECTIONS:
           return jsonify({"success":False , "error":"Invalid !"}) , 400
       
       All_problems = PROBLMES.find({"section_title":p_name})
       if not All_problems:
           return jsonify({"success":False , "error":"Unable to gather problems from DB"}) , 200
       
       data = []
       for i in All_problems:
           i['_id'] = str(i['_id'])
           data.append(i)
        
       return jsonify({"success":True , "data":data}) , 200
    except Exception as e:
        print(e)
        return jsonify({"success":False, "error":"Internal Server Error"}) , 500
        


@Api.route("/<p_name>" , methods=['POST'])
def Upload_Problem(p_name):
    try:

        if p_name.capitalize() not in PROBLEMS_SECTIONS:
           return jsonify({"success":False , "error":"Invalid !"}) , 400
        
        content = request.get_json()
        
        if not content:
            return jsonify({"success":False , "error":"Content was Not Provided"}) , 400
        
      
        for i , count in enumerate(content['problems']):
            count['problem_id'] = i+1
        

        PROBLMES.insert_one(content)
        return jsonify({"success":True , "data":f"Problem Uploaded at {p_name}"}) , 200
    except Exception as e:
        print(e)
        return jsonify({"success":False, "error":"Internal Server Error"}) , 500




@Api.route('/<p_name>/<int:id>')
def Find_one_Problem(p_name , id):
    try:
        p_name = p_name.capitalize()
        problem = PROBLMES.find_one({"section_title":p_name} , {
            "problems":{
                "$elemMatch":{"problem_id":id}
            }
        })
      
        if problem:
            if not problem.get('problems'):
                return jsonify({"success":False , "error":f"Problem ID : {id} was Not Found"}) ,400
            
            problem['_id'] = str(problem['_id'])
            return jsonify({"success":True , "data":problem})
        return jsonify({"success":False , "error":"Problem Section was Not Found"}) , 400
    except Exception as e:
        
        return jsonify({"success":False , "error":"Internal Server Error"}) , 500



@Api.route("/program/run" , methods=['POST'])
def program_run():
    try:
        code = request.json.get("code")

        if not code:
            return jsonify({"error": "Code not Provieded"}) , 400
        
        response = Run_Code(code)
        return jsonify(response) , 200
    except:
        return jsonify({"error":"Internal Server Error"}) , 500



@Api.route("/complete/<p_type>/<p_id>" , methods=['POST'])
def Complete_Problem(p_type , p_id):
    try:
        if p_type not in PROBLEMS_SECTIONS:
            return jsonify({"success":False , "error":"Invalid !"}) , 400
        
        PROBLMES.find_one_and_update({"section_title":p_type} , {
            "$set":{
                "problems.$[arr].completed":True
            }
        } , array_filters=[{"arr.problem_id":int(p_id)}])

        return jsonify({"success":True , "msg":"Document Updated"})
    except Exception as e:
        print(e)
        return jsonify({"success":False})


