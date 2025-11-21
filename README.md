# Gluttonous Boy 🎮

Um jogo educacional desenvolvido em Pygame onde você controla um menino que precisa coletar alimentos saudáveis e evitar junk food! Sobreviva por 60 segundos enquanto a dificuldade aumenta progressivamente e enfrente eventos especiais de "Chuva de Comida Lixo"!

## 📋 Descrição

Neste jogo, você controla um personagem que se move pela tela coletando alimentos que caem do céu. Seu objetivo é:

- ✅ Coletar alimentos saudáveis (+10 pontos, +30 HP)
- ❌ Evitar junk food (-5 pontos, -10 HP)
- ⚡ Sobreviver aos eventos especiais de "Chuva de Comida Lixo"
- ⏱️ Durar 60 segundos sem perder toda sua saúde

### Características

- Sistema de pontuação com pontos positivos e negativos
- Barra de vida com regeneração ao coletar comida saudável
- Dificuldade progressiva que aumenta ao longo do tempo
- Eventos especiais "Junk Food Rain" ativados por marcos de pontuação
- Bônus de sobrevivência para eventos bem-sucedidos
- Mecânica de pulo para facilitar o movimento

## 🎯 Alimentos

### Saudáveis (🥗)
- Alface
- Banana
- Maçã
- Pêra

### Junk Food (🍔)
- Chocolate
- Hambúrguer
- Refrigerante
- Sorvete

## 🎮 Controles

- **Setas Esquerda/Direita**: Mover o personagem
- **Espaço**: Pular
- **Qualquer tecla**: Iniciar/Reiniciar jogo

## 💻 Requisitos

- Python 3.7 ou superior
- Pygame

## 🚀 Instalação

### 1. Clone ou baixe o repositório

```bash
git clone https://github.com/seu-usuario/gluttonous-boy.git
cd gluttonous-boy
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install pygame
```

Ou usando o arquivo requirements.txt (se disponível):

```bash
pip install -r requirements.txt
```

## 🎮 Como Jogar

1. Execute o jogo:

```bash
python main.py
```

2. Leia as instruções na tela inicial
3. Pressione qualquer tecla para começar
4. Use as setas para mover o personagem
5. Colete comida saudável e evite junk food!
6. Fique atento aos avisos de "JUNK FOOD RAIN INCOMING!"
7. Tente sobreviver 60 segundos com a maior pontuação possível

## 📁 Estrutura do Projeto

```
joguinho/
│
├── main.py           # Loop principal do jogo e lógica
├── sprites.py        # Classes dos sprites (Player, Food, FloatingText)
├── settings.py       # Configurações e constantes
├── CLAUDE.md         # Documentação para desenvolvimento
├── README.md         # Este arquivo
│
└── assets/           # Recursos gráficos
    ├── Boneco_Gordinho_A1.png
    ├── Alface.png
    ├── Banana.png
    ├── Maçã.png
    ├── Pêra.png
    ├── Chocolate.png
    ├── Hamburguer.png
    ├── Refrigerante.png
    ├── Sorvete.png
    ├── Terreno_01.png
    ├── Terreno_02.png
    └── Terreno_03.png
```

## 🎲 Mecânicas do Jogo

### Sistema de Pontuação
- Comida saudável: +10 pontos
- Junk food: -5 pontos
- Bônus de sobrevivência (evento): +50 pontos

### Sistema de Vida
- Vida máxima: 100 HP
- Cura (comida saudável): +30 HP
- Dano (junk food normal): -10 HP
- Dano (junk food no evento): -15 HP

### Dificuldade Progressiva
- A velocidade de spawn aumenta gradualmente ao longo dos 60 segundos
- Multiplicador de dificuldade: 1.0x → 3.0x
- A velocidade dos alimentos também aumenta

### Eventos Especiais
- Ativados ao atingir 50, 120 e 200 pontos
- Fase de aviso de 3 segundos
- Duração do evento: 10 segundos
- Apenas junk food cai durante o evento
- Sobreviver levando ≤2 hits concede +50 pontos

## 🛠️ Desenvolvimento

Para modificar o jogo, edite os seguintes arquivos:

- **[settings.py](settings.py)**: Ajuste valores como velocidade, pontuação, duração
- **[sprites.py](sprites.py)**: Modifique comportamento dos sprites
- **[main.py](main.py)**: Altere lógica do jogo e eventos

Consulte [CLAUDE.md](CLAUDE.md) para documentação detalhada da arquitetura.

## 🐛 Solução de Problemas

### Erro: "No module named 'pygame'"
```bash
pip install pygame
```

### Erro: "Cannot load image"
Verifique se a pasta `assets/` está no mesmo diretório que `main.py` e contém todas as imagens necessárias.

### O jogo está muito lento
Certifique-se de que seu computador atende aos requisitos mínimos e que não há outros programas pesados rodando.

## 📝 Licença

Este é um projeto educacional desenvolvido para fins de aprendizado.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou enviar pull requests.

---

**Divirta-se jogando Gluttonous Boy!** 🎮🍎
