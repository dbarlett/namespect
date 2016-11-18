from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from core import app

db = SQLAlchemy(app)


class USName(db.Model):
    """U.S. name.
    count_surname may not be equal to count_surname_male + count_surname_female
    due to unknown genders in source data.
    count_given may not be equal to count_given_male + count_given_female
    due to unknown genders in source data.
    """
    __tablename__ = "us_names"
    name = db.Column(db.String(30), primary_key=True)
    count_surname = db.Column(db.Integer)
    count_surname_male = db.Column(db.Integer)
    count_surname_female = db.Column(db.Integer)
    count_given = db.Column(db.Integer)
    count_given_male = db.Column(db.Integer)
    count_given_female = db.Column(db.Integer)

    def __init__(
        self,
        name,
        count_surname=0,
        count_surname_male=0,
        count_surname_female=0,
        count_given=0,
        count_given_male=0,
        count_given_female=0
    ):
        self.name = name
        self.count_surname = count_surname
        self.count_surname_male = count_surname_male
        self.count_surname_female = count_surname_female
        self.count_given = count_given
        self.count_given_male = count_given_male
        self.count_given_female = count_given_female

    def __repr__(self):
        return "<USName({}>".format(self.name)

    def p_given_male(self):
        """Return probability that a name is male given name, or None if the
        name is unknown.
        """
        if self.count_given_male == 0:
            return None
        else:
            return 1.0 * self.count_given_male / (
                self.count_given_male + self.count_given_female
            )
