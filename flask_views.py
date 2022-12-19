from flask import render_template, redirect, request, current_app, session, \
    flash, url_for
from flask import session
from flask_login import login_required

from sqlalchemy_models import argument_table,argument_by_expert_opinion,register_table, argument_by_popular_scheme, argument_by_action_scheme
from flask_apps import app, db
from grounded_algorithm import grounded

ROWS_PER_PAGE = 4
@app.route('/index')
@app.route('/')
def index():
    # Setting the pagination configuration
    page = request.args.get('page', 1, type=int)
    args = argument_table.query.paginate(page=page, per_page=ROWS_PER_PAGE)

    # if not args:
    #    return
    # full_tree = []
    # for root in args:
    #    full_tree.append(root.drilldown_tree()[0])

    return render_template('index.html', args = args)

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/vote')
def vote():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    username = request.form['user_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    print("success")
    if(password !=  confirm_password):
        print("confirm password not the same as password. Enter data again")
        return render_template('register.html')

    data = register_table(firstname, lastname, username, email, password, confirm_password)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index', page=1))

@app.route('/login_page')

def login_page():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']

        query = db.session.query(register_table).filter(register_table.username.like(username), register_table.password.like(password)).all()
        print(query)
        if(query):
            print("Account exists! Login successful")
            return redirect(url_for('index'))
        else:
            print("Account not found! Please register")
            return redirect('/register_page')

@app.route('/createArgument',methods=['GET','POST'])
def createArgument():
    topic = request.form['topic']
    scheme = request.form['scheme']

    if scheme == 'expert':
        return render_template('expert_scheme.html', topic=topic)
    if scheme=='action':
        return render_template('action_scheme.html', topic=topic)
    if scheme=='popular':
        return render_template('popular_opinion.html', topic=topic)

@app.route('/createExpertPost',methods=['GET','POST'])
def createExpertPost():
    topic = request.form['topic']
    expertAssumption = request.form['expertAssumption']
    premise = request.form['premise']
    conclusion = request.form['conclusion']
    argumentDesciption = str(premise) + ".Therefore," + str(conclusion)
    db.session.add(argument_table(topic, conclusion, argumentDesciption))
    db.session.commit()
    #flash('Record added successfully ')
    db.session.add(argument_by_expert_opinion(topic = topic, expert = expertAssumption, domain=premise, proposition= conclusion))
    db.session.commit()
    #flash('Record added successfully ')
    return redirect(url_for('index'))


@app.route('/createPopularPost',methods=['GET','POST'])
def createPopularPost():
    topic = request.form['topic']
    premise = request.form['premise']
    conclusion = request.form['conclusion']
    argumentDesciption = str(premise) + ".Therefore," + str(conclusion)
    db.session.add(argument_table(topic, conclusion, argumentDesciption))
    db.session.commit()
    #flash('Record added successfully ')
    db.session.add(argument_by_popular_scheme(topic = topic, premise = premise, conclusion=conclusion))
    db.session.commit()
    #flash('Record added successfully ')
    return redirect(url_for('index'))


@app.route('/createActionPost',methods=['GET','POST'])
def createActionPost():
    topic = request.form['topic']
    circumstance = request.form['circumstance']
    action = request.form['action']
    goal = request.form['goal']
    value = request.form['value']
    argumentDesciption = str(circumstance) + ", performing action, " + str(action) + ", achieves " + str(goal)
    db.session.add(argument_table(topic, goal, argumentDesciption))
    db.session.commit()
    #flash('Record added successfully ')
    db.session.add(argument_by_action_scheme(topic = topic, circumstance = circumstance, action=action, goal= goal, value=value))
    db.session.commit()
    #flash('Record added successfully ')
    return redirect(url_for('index'))

@app.route('/attackButton',methods=['GET','POST'])
def attackButton():
    return render_template('attack_post.html')


@app.route('/create_debate',methods=['GET','POST'])
def create_debate():
    return render_template('create_debate.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/groundedgraph')
def groundedgraph():
    query = argument_table.query.all()
    node = ['Lockdown is not demanded as wearing masks is sufficient', 'Lockdown should be necessary to control virus', '70% citizens think lockdown is ineffective to control virus','Lockdown should be mandatory to reduce cases', 'New batman movie was dope']
    links = [(
            'Lockdown is not demanded as wearing masks is sufficient',
            'Lockdown should be necessary to control virus'
    ),
        ('70% citizens think lockdown is ineffective to control virus',
            'Lockdown should be necessary to control virus'
        ),

        ( '70% citizens think lockdown is ineffective to control virus',
            'Lockdown should be mandatory to reduce cases'
        ),
        ( 'Lockdown should be mandatory to reduce cases' ,
            '70% citizens think lockdown is ineffective to control virus'
        )
    ]
    grounded_labelling = grounded(node, links)
    print(grounded_labelling)
    return render_template('grounded_graph.html', args = grounded_labelling)


@app.route('/logout')
def logout():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)