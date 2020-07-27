# COVID 
> Website para compartilhar informações, do principais órgãos de saúde brasileiro, e evitar a disseminação de fake news sobre o coronavírus. Com gráficos interativos para o acompanhamento da evolução do COVID-19 no Brasil.

## Instalação

```
python3 -m venv env
source env/bin/activate

pip install -r requeriments.txt
```

## Uso

Para executar o sevidor de teste:
```
python3 manage.py runserver
```

Para atualizar os gráficos:
```
cd website/plots
python plot.py
```
Por padrão plot.py cria três arquivos de cache 

O servidor por padrão pode ser acessado por http://127.0.0.1:8000 ou https://covid.fredbr.com
