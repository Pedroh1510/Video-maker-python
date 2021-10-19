# Video-maker

Projeto para automatizar a criação de videos em python

Projeto original
[Filipe Deschamps Git](https://github.com/filipedeschamps/video-maker)

## Sem docker

```shell
# instale as dependencias
pip install -r requirements.txt
# rodando a aplicação
python3 index.js
```

## Com docker

```shell
# Build da imagem
docker build -t video-maker-python .
# rodando o conteiner
docker run -it --rm -v ${pwd}/content:/content  -e language='' -e searchTerm='' -e prefix='' -e template=1 video-maker-python
```

- language: escolha do idioma, aceito, en, pt e pt-br
- searchTerm: alvo da pesquisa
- prefix: prefixo do video
- template: reservado para criação de escolha de templates
