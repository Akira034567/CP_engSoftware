# 🚀 FIAP StudySpace

## 📌 Descrição do Problema
Alunos enfrentam dificuldade para encontrar laboratórios adequados e realmente disponíveis para cada tipo de atividade acadêmica. A busca manual por sala gera perda de tempo, conflito de uso e baixa eficiência no aproveitamento da infraestrutura.

## 💡 Solução Proposta
O FIAP StudySpace centraliza a visualização de laboratórios, reservas e check-in em uma plataforma web. Além da disponibilidade em tempo real, o sistema recomenda automaticamente os melhores ambientes conforme o perfil de uso (programação, web, IA/ML, redes, etc.), cruzando a categoria selecionada com características dos laboratórios e prioridades por andar.

## 🆕 Evoluções do Checkpoint 1 para o Checkpoint 2
- Estrutura do projeto reorganizada em `models/`, `views/` e `data/`.
- Catálogo de laboratórios atualizado para a Unidade 2 com regras por andar/sala.
- Implementação de recomendação inteligente por categoria de uso.
- Clique direto na sala na tela inicial levando para a reserva com sala pré-selecionada.
- Ajustes de persistência para banco em `data/reservas.db`.
- Refinos no fluxo de reserva com visualização de agenda por sala/data.

## 🛠️ Tecnologias Utilizadas
- Python 3
- Flask
- SQLite
- SQLAlchemy
- Flask-Login
- APScheduler
- Jinja2
- HTML5
- CSS3
- JavaScript
- Lucide Icons

## ⚙️ Como Executar
### Pré-requisitos
- Python 3.8+
- pip

### Instalação
```bash
git clone https://github.com/akira034567/CP_engSoftware.git
cd CP_engSoftware
pip install -r requirements.txt
```

### Execução
```bash
python app.py
```
Acesse: `http://localhost:5000`

Credenciais padrão:
- Admin: `admin` / `admin123`

## 📁 Estrutura do Projeto
```text
CP_engSoftware/
├── app.py
├── config.py
├── requirements.txt
├── models/                    # classes do domínio
├── views/                     # interface (templates, rotas, assets)
│   ├── routes/
│   ├── templates/
│   └── static/
├── services/                  # regras de negócio
└── data/                      # dados persistidos
    └── reservas.db
```

## ✅ Funcionalidades Implementadas
### Cadastro e Login
- Registro de usuário estudante.
- Login e logout com controle de sessão.
- Perfil administrador com acesso a gestão e relatórios.

### Casos de Uso (com status: ✅ Implementado / 🚧 Parcial / ❌ Não implementado)
| ID | Caso de Uso | Status |
|---|---|---|
| RF01 | Visualizar laboratórios disponíveis em tempo real | ✅ Implementado |
| RF02 | Criar reserva de laboratório | ✅ Implementado |
| RF03 | Cancelar reserva | ✅ Implementado |
| RF04 | Realizar check-in | ✅ Implementado |
| RF05 | Validar janela de check-in | ✅ Implementado |
| RF06 | Consultar histórico de reservas | ✅ Implementado |
| RF07 | Receber notificações no sistema | ✅ Implementado |
| RF08 | Gerenciar laboratórios (admin) | ✅ Implementado |
| RF09 | Visualizar relatórios de uso | ✅ Implementado |
| RF10 | Auto-cancelamento por não comparecimento | ✅ Implementado |
| RF11 | Recomendação inteligente por categoria | ✅ Implementado |
| RF12 | Clique na sala inicial já abrir reserva da sala | ✅ Implementado |

## ⭐ Diferencial do Projeto
### Descrição
Sistema inteligente de filtragem e recomendação de laboratórios por categoria acadêmica, indicando os ambientes mais adequados com base em prioridade por andar e perfil de hardware (ex.: GPU para IA/ML e computação gráfica, MacBooks para iOS, maior capacidade para uso geral).

### Justificativa
Esse diferencial reduz o tempo de busca, melhora a assertividade da escolha da sala e alinha o uso da infraestrutura às demandas reais de cada atividade, elevando eficiência para alunos e gestão.

### Referências
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- APScheduler Documentation: https://apscheduler.readthedocs.io/

## 🎬 Demonstração (obrigatório — GIFs, prints ou vídeo de até 3 min)
- Vídeo: https://youtu.be/KJ6R-ZuvPI0
- Sugestão: incluir também GIF curto da recomendação por categoria + fluxo de clique direto para reserva.

## 👥 Integrantes do Grupo
| Nome | RM | Turma |
|---|---|---|
| Davi da Silva Biaggioli | 552581 | 3ECR |
| Jean Lucas Loureiro Depieri | 555797 | 3ECR |
| João Gabriel De Bortoli Ribeiro | 554601 | 3ECR |
| Lucas Akira Watanabe | 554875 | 3ECR |
| Luiz Guilherme de Souza Varischi | 559028 | 3ECR |
| Pedro Alvarez Certo | 554603 | 3ECR |
| Gustavo Demeis Peres | 555143 | 3ECR |

## 🔗 Links (Miro, repositório, vídeo)
- Repositório: https://github.com/Akira034567/CP_engSoftware
- Miro: https://miro.com/welcomeonboard/T0ExRGtOWjR1K0FWNXJxRzFHWDRMNWxmOGJ3M1hlK0dLOTNCZTBUblNQR1hPOWp6OGZCWTVEUlROYVhtWmhrZlZ3MCtzU2dZeEs3VTdTYVdYUXZYeDhnNjNGZDgwRDEyOVdoVXFrYUZIRUtQeGhLZ1NuaXRjSlVuWEkvYllwUW1BS2NFMDFkcUNFSnM0d3FEN050ekl3PT0hdjE=?share_link_id=777295586836
