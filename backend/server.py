from flask import Flask, request, render_template, url_for, flash, redirect
from wtforms import Form, TextAreaField, validators, StringField, SubmitField
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import sys,re

# internal library imports
sys.path.insert(1, './libs')
import errors
import connectors
import validators


app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d233f2b6176a'

bootstrap = Bootstrap5(app)
#csrf = CSRFProtect(app)

class TGInfoForm(FlaskForm):

    install_command = StringField('Connector Install Command', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TGInfoForm()
    message = ""
    if form.validate_on_submit():
        connector_install_cmd = form.install_command.data
        tenant_name,access_token,refresh_token = validators.get_info_from_install_cmd(connector_install_cmd)
        print("Form validated:"+tenant_name)
        
        if connectors.check_for_running_connector():
            return render_template('error.html',message = 'A Connector is already installed..')

        res = connectors.provision_install_script(access_token,refresh_token,tenant_name)
        hasError,resp = connectors.install_connector()
        if hasError:
            print(errors.rconnector_install_error(resp))
            return render_template('error.html',message = errors.rconnector_install_error(resp))
        else:
             print("Connector installed.")
             connectors.delete_install_script()
             return render_template('success.html')
        
    return render_template('index.html', form=form, message=message)
