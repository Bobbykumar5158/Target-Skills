from flask import Flask, request, url_for, redirect, render_template, flash
from genai import bot
import json
import os
import threading
import time

app = Flask(__name__)
app.secret_key = "secrect_key"

def generate_roadmap(role_title):

    filepath = "data/user.json"
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        try:
            with open(filepath, "r") as file:
                roadmaps = json.load(file)
        except json.JSONDecodeError:
            roadmaps = []
    else:
        roadmaps = []

    roadmap = bot(role_title)

    with open("data/user.json","w") as file:
        if roadmaps:
            roadmaps.append(roadmap)
            json.dump(roadmaps,file,indent=4)
        else:
            json.dump([roadmap],file,indent=4)
        print("done")
        
            

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/explore",methods = ['GET','POST'])
def explore():
    company_name = request.args.get('company', '')
    if request.method == "POST":
        company_name = request.form.get('company_name').strip()

        try:
            with open('data/roles.json', 'r') as file:
                roles_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            roles_data = {"company": "", "response": []}

        if roles_data.get("company", "").lower() == company_name.lower():
            fetched_data = roles_data.get("response", [])
        else:
            # will call bot here
            fetched_data = {} # genai data
            # NOTE when fetching bot data add company name to it before writing it to file
            time.sleep(1) # time taken by bot to response
            with open('data/roles.json','w') as file:
                json.dump(fetched_data,file)



        return render_template("explore.html",data = fetched_data,company = company_name)
        
    if company_name :
        try:
            with open('data/roles.json', 'r') as file:
                roles_data = json.load(file)
                fetched_data = roles_data.get("response", [])
        except:
            fetched_data = []
        return render_template("explore.html", data=fetched_data, company=company_name)
    
    return render_template("explore.html")

@app.route("/roadmap", methods=['GET', 'POST'])
def roadmap():
    if request.method == 'POST':
        role = request.form.get("role_title")
        company_name = request.form.get("company_name")

        flash("Target Added! Your roadmap will be available on your dashboard .", "success")
        
        task = threading.Thread(
            target=generate_roadmap, 
            args=(role,)
            )
        task.start()
        
        return redirect(url_for("explore",company = company_name))
        
    return redirect(url_for("explore"))



if __name__ == "__main__":
    app.run(debug=True)