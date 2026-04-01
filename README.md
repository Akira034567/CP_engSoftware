# FIAP StudySpace

## 📌 Descrição do Problema

Alunos da FIAP enfrentam dificuldades para encontrar espaços de estudo disponíveis, especialmente em horários de maior movimento. Muitas salas aparentam estar ocupadas, mas não estão sendo utilizadas de forma eficiente, enquanto outros alunos perdem tempo procurando um local adequado para estudar ou realizar trabalhos em grupo.

Além disso, a ausência de um sistema centralizado para visualização e reserva de espaços gera conflitos entre usuários e dificulta o controle por parte da administração.

---

## 🚀 Solução Proposta

O **FIAP StudySpace** é um sistema web que permite aos alunos visualizar espaços de estudo disponíveis em tempo real, realizar reservas de forma rápida e efetuar check-in ao chegar no local.

A plataforma também oferece funcionalidades administrativas, permitindo o gerenciamento dos espaços e o monitoramento de sua utilização, garantindo melhor organização e aproveitamento dos ambientes.

Com isso, o sistema reduz o tempo perdido na busca por salas, evita conflitos entre usuários e torna o uso dos espaços mais eficiente e inteligente.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|-----------|
| **Python 3** | Linguagem principal do backend |
| **Flask** | Framework web leve e modular |
| **SQLite** | Banco de dados relacional (persistência em arquivo) |
| **SQLAlchemy** | ORM para modelagem e consultas ao banco |
| **Flask-Login** | Gerenciamento de autenticação e sessões |
| **Werkzeug** | Hash seguro de senhas (segurança) |
| **APScheduler** | Agendamento de tarefas automáticas (auto-cancelamento) |
| **Jinja2** | Template engine para renderização de páginas HTML |
| **HTML5 / CSS3 / JavaScript** | Frontend com design responsivo e moderno |
| **Lucide Icons** | Biblioteca de ícones via CDN |
| **Google Fonts (Inter)** | Tipografia premium |

---

## ⚙️ Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/akira034567/CP_engSoftware.git
cd CP_engSoftware

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
python app.py
```

### Acesso
- **URL**: http://localhost:5000
- **Admin**: `admin` / `admin123` (gerencia espaços e relatórios)
- **Estudante**: Cadastre-se pela tela de registro

---

## 📂 Estrutura do Projeto

```
CP_engSoftware/
├── app.py                          # Ponto de entrada da aplicação
├── config.py                       # Configurações (DB, segurança, regras de negócio)
├── requirements.txt                # Dependências do projeto
│
├── models/                         # Modelos de dados (ORM)
│   ├── __init__.py                 # Instância do SQLAlchemy
│   ├── user.py                     # Modelo de Usuário (admin/student)
│   ├── space.py                    # Modelo de Espaço de Estudo
│   ├── reservation.py              # Modelo de Reserva
│   └── notification.py             # Modelo de Notificação
│
├── services/                       # Lógica de negócio
│   ├── reservation_service.py      # Criação, validação, check-in, cancelamento
│   ├── scheduler_service.py        # Auto-cancelamento de reservas (RF10)
│   └── notification_service.py     # Envio de notificações no sistema
│
├── routes/                         # Rotas (controllers)
│   ├── auth.py                     # Login, registro, logout
│   ├── spaces.py                   # Visualização de espaços + API tempo real
│   ├── reservations.py             # CRUD de reservas + check-in
│   ├── notifications.py            # Listagem e leitura de notificações
│   └── admin.py                    # Gerenciamento de espaços + relatórios
│
├── templates/                      # Templates HTML (Jinja2)
│   ├── base.html                   # Layout base com navbar
│   ├── auth/                       # Login e registro
│   ├── spaces/                     # Visualização de espaços
│   ├── reservations/               # Formulário e listagem de reservas
│   ├── notifications/              # Página de notificações
│   └── admin/                      # Gerenciamento e relatórios
│
├── static/                         # Arquivos estáticos
│   ├── css/style.css               # Design premium (dark theme, glassmorphism)
│   └── js/main.js                  # Polling tempo real e interatividade
│
└── instance/
    └── reservas.db                 # Banco de dados SQLite (gerado automaticamente)
```

---

## 🧩 Funcionalidades Implementadas

### Requisitos Funcionais

| ID   | Descrição                                                | Status |
|------|----------------------------------------------------------|--------|
| RF01 | Visualizar espaços disponíveis em tempo real             | ✅ Implementado (polling a cada 5s) |
| RF02 | Reservar espaço de estudo                                | ✅ Implementado (com validações) |
| RF03 | Cancelar reserva                                         | ✅ Implementado (com confirmação) |
| RF04 | Realizar check-in no espaço reservado                    | ✅ Implementado (janela de 2 min) |
| RF05 | Validar reserva antes do check-in                        | ✅ Implementado (verifica status, horário e propriedade) |
| RF06 | Registrar histórico de reservas                          | ✅ Implementado (com filtros por status) |
| RF07 | Enviar notificações dentro do sistema                    | ✅ Implementado (badge + listagem) |
| RF08 | Gerenciar espaços (criar, editar, remover)               | ✅ Implementado (CRUD completo - admin) |
| RF09 | Visualizar relatórios de uso                             | ✅ Implementado (dashboard com estatísticas) |
| RF10 | Cancelar automaticamente reservas por não comparecimento | ✅ Implementado (APScheduler a cada 60s) |

### Requisitos Não-Funcionais

| ID    | Descrição                                            | Status |
|-------|------------------------------------------------------|--------|
| RNF01 | Tempo de resposta inferior a 2 segundos              | ✅ SQLite local + queries otimizadas |
| RNF02 | Interface intuitiva e fácil de usar                  | ✅ Design moderno com glassmorphism |
| RNF03 | Garantir segurança dos dados (autenticação)          | ✅ Flask-Login + hash de senhas |
| RNF04 | Disponibilidade mínima de 99%                        | ✅ Arquitetura simples e robusta |
| RNF05 | Compatibilidade com navegadores modernos             | ✅ HTML5 + CSS3 padrão |

---

## 📸 Demonstração

[![Demonstração do Sistema](https://img.youtube.com/vi/KJ6R-ZuvPI0/maxresdefault.jpg)](https://youtu.be/KJ6R-ZuvPI0)

*Clique na imagem ou no link acima para assistir à demonstração.*

---

## 👨‍💻 Integrantes do Grupo

|                Nome                |    RM    | Turma |
|------------------------------------|----------|-------|
| Davi da Silva Biaggioli            |  552581  |  3ECR |
| Jean Lucas Loureiro Depieri        |  555797  |  3ECR |
| João Gabriel De Bortoli Ribeiro    |  554601  |  3ECR |
| Lucas Akira Watanabe               |  554875  |  3ECR |
| Luiz Guilherme de Souza Varischi   |  559028  |  3ECR |
| Pedro Alvarez Certo                |  554603  |  3ECR |
| Gustavo Demeis Peres               |  555143  |  3ECR |

---

## 🔗 Links

- **Repositório GitHub**: [https://github.com/Akira034567/CP_engSoftware](https://github.com/Akira034567/CP_engSoftware)
- **Board (Miro)**: [https://miro.com/welcomeonboard/T0ExRGtOWjR1K0FWNXJxRzFHWDRMNWxmOGJ3M1hlK0dLOTNCZTBUblNQR1hPOWp6OGZCWTVEUlROYVhtWmhrZlZ3MCtzU2dZeEs3VTdTYVdYUXZYeDhnNjNGZDgwRDEyOVdoVXFrYUZIRUtQeGhLZ1NuaXRjSlVuWEkvYllwUW1BS2NFMDFkcUNFSnM0d3FEN050ekl3PT0hdjE=?share_link_id=777295586836](https://miro.com/welcomeonboard/T0ExRGtOWjR1K0FWNXJxRzFHWDRMNWxmOGJ3M1hlK0dLOTNCZTBUblNQR1hPOWp6OGZCWTVEUlROYVhtWmhrZlZ3MCtzU2dZeEs3VTdTYVdYUXZYeDhnNjNGZDgwRDEyOVdoVXFrYUZIRUtQeGhLZ1NuaXRjSlVuWEkvYllwUW1BS2NFMDFkcUNFSnM0d3FEN050ekl3PT0hdjE=?share_link_id=777295586836)
