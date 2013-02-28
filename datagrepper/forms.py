from flask.ext import wtf


class NullForm(wtf.Form):
    pass


class InformationForm(wtf.Form):
    email = wtf.TextField("Email", validators=[wtf.validators.Email()])
