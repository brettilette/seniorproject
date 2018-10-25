from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/mainPage.html')
def mainPage():
        return render_template('mainPage.html')
@app.route('/about.html')
def about():
        return render_template('about.html')
@app.route('/createProject.html')
def createProjectPage():
        return render_template('createProject.html')
@app.route('/editProject.html')
def editProjectPage():
        return render_template('editProject.html')
@app.route('/viewProject.html')
def viewProjectPage():
        return render_template('viewProject.html')
@app.route('/dashboard.html')
def dashboard():
        return render_template('dashboard.html')



if __name__ == '__main__':
    app.run()