from sqlalchemy import create_engine, ForeignKey
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_mptt.mixins import BaseNestedSets
from flask_apps import app,db


# noinspection PyUnresolvedReferences
class argument_table(db.Model, BaseNestedSets):
    __tablename__ = 'argument_table'

    topic = db.Column(db.TEXT(10), primary_key=True)
    username = db.Column(db.TEXT(10))
    parent = db.Column(db.Integer)
    id = db.Column(db.Integer)
    argumentTitle = db.Column(db.TEXT(200))
    argumentDescription = db.Column(db.TEXT(200))
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    dateOfCreation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateOfModification = db.Column(db.DateTime)
    #scheme = db.Column(db.TEXT(100), db.ForeignKey('schemes.scheme'))
    #criticalQuestion = db.Column(db.TEXT(100), db.ForeignKey('critical_questions.criticalQues'))

    #scheme = db.relationship('schemes')
   #criticalQuestion = db.relationship('critical_questions')

    def __init__(self, *args):

        if(len(args) == 3):
            self.topic = args[0]
            self.argumentTitle = args[1]
            self.argumentDescription = args[2]

        if(len(args) == 4):
            self.topic = args[0]
            self.username = args[1]
            self.argumentTitle = args[2]
            self.argumentDescription = args[3]

        if (len(args) == 5):
            self.topic = args[0]
            self.username = args[1]
            self.argumentTitle = args[2]
            self.argumentDescription = args[3]
            self.upvotes = args[4]

    def __repr__(self):
        return '<argument_table {}>'.format(self.username)

    #def getAttackers(self):
    #    argument_attackers = set()
    #    if (self.parent != None):
    #       if self.criticalQuestion.attackOnConclusion != False:
    #            argument_attackers.add(parent)
    #    if(len(self.get_children().exists()) != 0):
    #        for attacker in self.get_children().exists():
    #            argument_attackers.add(attacker)
    #    return argument_attackers

    def totalvotes(self):
    #    return self.upvotes - self.downvotes
        return 0

    def getGoal(self):
        try:
            argument = str(self.argumentDescription)
            return argument.split("in order to", 1)[1]
        except:
            return None

    def getAction(self):
        try:
            argument = str(self.argumentDescription)
            return argument.split("in order to", 1)[0]
        except:
            return None

    def getArgumentTitle(self):
        return str(self.argumentTitle)

    def getArgumentDescription(self):
        return str(self.argumentDescription)


# noinspection PyUnresolvedReferences
class register_table(db.Model):
    __tablename__ = 'register_table'

    firstname = db.Column(db.TEXT(100))
    lastname = db.Column(db.TEXT(100))
    username = db.Column('username', db.TEXT(10), primary_key=True)
    email = db.Column(db.TEXT(100))
    password = db.Column(db.TEXT(100))
    confirmpassword = db.Column(db.TEXT(100))

    def __init__(self, firstname, lastname, username, email, password, confirmpassword):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.confirmpassword = confirmpassword

# noinspection PyUnresolvedReferences
class schemes(db.Model):
    __tablename__ = 'schemes'
    # expert, popular , action
    scheme =  db.Column(db.TEXT(10), primary_key=True )
    schemeID = db.Column(db.TEXT(10))

# noinspection PyUnresolvedReferences
class critical_questions(db.Model):
    __tablename__ = 'critical_questions'
    criticalQues = db.Column(db.TEXT(10), primary_key=True)
    attackOnConclusion =  db.Column(db.Integer)
    scheme = db.Column(db.TEXT(100), db.ForeignKey('schemes.scheme'))


# noinspection PyUnresolvedReferences
class argument_by_action_scheme(db.Model):
    __tablename__ = 'argument_by_action_scheme'

    topic = db.Column(db.TEXT(10), primary_key=True)
    circumstance = db.Column(db.TEXT(100))
    action = db.Column(db.TEXT(100))
    goal = db.Column(db.TEXT(100))
    value = db.Column(db.TEXT(100))

# noinspection PyUnresolvedReferences
class argument_by_expert_opinion(db.Model):
    __tablename__ = 'argument_by_expert_opinion'

    topic = db.Column(db.TEXT(10), primary_key=True)
    expert = db.Column(db.TEXT(100))
    domain = db.Column(db.TEXT(100))
    proposition = db.Column(db.TEXT(100))

# noinspection PyUnresolvedReferences
class argument_by_popular_scheme(db.Model):
    __tablename__ = 'argument_by_popular_scheme'

    topic = db.Column(db.TEXT(10), primary_key=True)
    premise = db.Column(db.TEXT(100))
    conclusion = db.Column(db.TEXT(100))



# representing tree data
db.session.add(argument_table(
    "virus", "priya", "Lockdown should be necessary in order to control the spread of Coronavirus", "To reduce the risk of spread of the virus, lockdown must be mandatory"),
)  # root node
db.session.add_all(  # first branch of tree
    [
        #argument attacked by user 1, user 2, user 3
        argument_table("pandemic", "user1", "There is a reason to think that lockdown may not be necessary to lead to no pandemic.", "In a survey conducted by IPSOS, it is revealed that more and more citizens, (70%) regard the lockdown as a non-effective measure to control the pandemic.", 5),
        argument_table("lockdown", "user2", "Lockdown is mandatory to result in no pandemic", "Lockdown should be mandatory in order to flatten the curve and reduce the number of cases, leading to no pandemic.", 3),
        argument_table("batman", "user3", "The new Batman movie was dope. Definitely a must watch!!", "RP is a great actor"),
    ]
)
db.session.add_all(  # second branch of tree
    [
        # argument attacked by user12, user13, user 14
        argument_table("isolation","user12", "Lockdown is not demanded", "Lockdown is not demanded as wearing masks and social distancing is sufficient."),
        argument_table("fashion", "user13", "Fashion Model Giga's new look" , "Giga wears a black v neck outline dress to the met gala"),
        argument_table("python3", "user14", "Are there any libraries for implementing python tests?" , "I am trying to do unit tests, are there any libraries in python?"),
    ]
)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.commit()
    app.run(debug=True)


