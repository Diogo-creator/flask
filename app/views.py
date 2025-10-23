from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from app.models import Contato
from app.forms import ContatoForm, UserForm, LoginForm

@app.route('/', methods=['GET', 'POST'])
def homepage():

    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    
    context = {'form': form}

    return render_template('index.html', context=context, form=form)


@app.route('/cadastro/', methods = ['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        user = form.save()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('homepage'))
        else:
            return render_template('cadastro.html', form=form)

        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/contato/lista/')
def lista_contatos():
    
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')


    dados = Contato.query.order_by(Contato.nome).all()
    if pesquisa != '':
        dados = Contato.query.filter_by(nome=pesquisa).all()

    context = {'dados': dados}

    return render_template('lista_contatos.html', context=context)

@app.route('/contato/<int:id>/')
def contato_id(id):
    contato = Contato.query.get(id)
    context = {'contato': contato}
    return render_template('contato_id.html', context=context)







#Formato não recomendado
@app.route('/contato_old/', methods=['GET', 'POST'])
def contato_old():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        print('GET: ', pesquisa)
        context.update({"pesquisa": pesquisa})

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
            )
        
        db.session.add(contato)
        db.session.commit()

    return render_template('contato_old.html', context=context)

# Formato recomendado
@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template('contato.html', context=context, form=form)

