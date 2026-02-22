from flask import Flask , Blueprint , request , jsonify , render_template


router = Blueprint("Router" , __name__)

@router.route("/")
def Home_Page():
    try:
        return render_template("index.html")
    except:
        return "Error" ,500
    

@router.route("/<p_type>")
def Problems_Page(p_type):
    try:
        return render_template("problems.html" , p_type=p_type)
    except:
        return "Error" , 500
    


@router.route("/<p_type>/<p_id>")
def Solution_Page(p_type , p_id):
    try:
        return render_template("solution.html" , p_type=p_type , p_id=p_id)
    except:
        return "Error" , 500
    



