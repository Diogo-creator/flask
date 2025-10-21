from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Contato
from app.forms import ContatoForm

@app.route('/')
def homepage():
    return render_template('index.html')

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

