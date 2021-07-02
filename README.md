[![MIT License][license-shield]][license-url]


<br />
<p align="center">

  <h3 align="center">PresenteBot</h3>

  <p align="center">
    Um bot que não gosta de aulas on-line
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Tabela de conteúdos</summary>
  <ol>
    <li>
      <a href="#Sobre">Sobre</a>
    </li>
    <li>
      <a href="#Pré-requisitos">Pré-requisitos</a>
    </li>
    <li>
      <a href="#Uso">Uso</a>
    </li>
    <li>
      <a href="#Observações">Observações</a>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Sobre

PresenteBot é uma automação para quem não gosta de assistir aulas on-line mas precisa marcar presença, executa funções simples de entrar na sala, digitar "presente" após verificar que já foi digitado pelo menos 2 vezes, e sai da reunião após metade da sala ter saído. Atualmente funciona apenas no Google Meet.

Todos parâmetros são facilmente customizados para cumprir oque você precisa 😉

### Pré-requisitos

* Python
* Selenium
* Google Chrome
* [Chromedriver](https://chromedriver.chromium.org/downloads)

<!-- USAGE EXAMPLES -->
## Uso

Coloque o arquivo "chromedriver.exe" na mesma pasta do script.

Execute o script.
```python
python presenteBot.py
```

Insira suas informações (não se preocupe, essas informações só são usadas localmente, fique à vontade para verificar o código fonte).

Não feche a janela, deixe o bot trabalhando 😊.

## Observações

* Esse bot foi baseado no [google_meet_bot](https://github.com/basil-b2s/Google_meet_bot), créditos à eles.
* Caso queira usar com outro navegador, acredito que seja relativamente fácil, basta apenas alterar o driver carregado, fique à vontade para tentar.
* Não me responsabilizo pelo uso desse bot, se seu professor te reprovou, sinto muito 🤷‍♂️.

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
