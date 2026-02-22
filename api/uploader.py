PROBLEMS_SECTIONS = ['Easy' , 'Medium' , "Harder" , "Dsa_interview"]

import subprocess
import os
import uuid

os.makedirs("temp_code" , exist_ok=True)



def Run_Code(code):

    file_name = f"{uuid.uuid4().hex}.py"
    file_path = os.path.join("temp_code", file_name)
    
    with open(file_path, "w") as f:
              f.write(code)

    try:
        
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=5 
        )

        output = result.stdout
        error = result.stderr

        return {
            "output": output,
            "error": error
        }

    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}, 500

    finally:
        os.remove(file_path)






