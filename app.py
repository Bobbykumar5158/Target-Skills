from flask import Flask, request, url_for, redirect, render_template, flash
from genai import bot
import json
import threading
import time
from DB import read_data, write_data

app = Flask(__name__)
app.secret_key = "secrect_key"
user_file = "data/user.json"
roles_file = "data/roles.json"

def generate_roadmap(role_title,attempt = 3):

    roadmaps = read_data(user_file)
    if attempt != 0 :
        response = json.loads(bot(role_title))
        if response["status_code"] == 200:
            roadmap = response["response"]
            title_key = role_title.lower().replace(" ", "_")
            roadmaps[title_key]["status"] = "True"
            roadmaps[title_key]["roadmap"] = roadmap

        else:
            time.sleep(10)
            generate_roadmap(role_title,attempt-1)
    else :
        roadmaps[title_key]["status"] = "None"
        
        
            

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/explore",methods = ['GET','POST'])
def explore():
    company_name = request.args.get('company', '')
    if request.method == "POST":
        company_name = request.form.get('company_name').strip()

        roles_data = read_data(roles_file)

        if roles_data.get("company", "").lower() == company_name.lower():
            fetched_data = roles_data.get("response", [])
        else:
            bot_data = json.loads(bot(company_name))
            if bot_data["status_code"] == 200:
                bot_data["company"] = company_name
                fetched_data = bot_data["response"]
                write_data(roles_file,bot_data)
                
            else:
                return render_template('error.html',response = bot_data)

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

        roadmaps = read_data()
        title_key = role.lower().replace(" ", "_")
        roadmaps[title_key] = {
            "status" : "False",
            "roadmap" : {}
        }
        
        return redirect(url_for("explore",company = company_name))
        
    return redirect(url_for("explore"))

@app.route("/dashboard")
def dashboard():
    roadmaps = read_data(user_file)
    return render_template("dashboard.html",user_tracks = roadmaps)

@app.route("/delete-roadmap", methods = ['POST'])
def delete_roadmap():
    track_to_pop = request.form.get("track_id")
    
    if not track_to_pop:
        flash("Could not resolve track identity identifier.", "error")
        return redirect(url_for("dashboard"))
    
    user_data = read_data(user_file)
    user_data.pop(track_to_pop)

    # Write back the updated data clean to disk
    write_data(user_file,user_data)
    flash("Track removed successfully from your tracking dashboard profile.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)