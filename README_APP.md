# Personal Trainer (Django) — Protótipo navegável (Web Admin)

Este repositório entrega um **protótipo navegável** em Django, com módulos separados (apps) e um tema “Fitness Premium”
(energia visual, destaque em métricas, tipografia robusta).

## Stack
- Python + Django
- Templates (Django) + Bootstrap 5 (CDN) + CSS do tema

## Como rodar (local)
1) Crie e ative um virtualenv
2) Instale dependências:
```bash
pip install -r requirements.txt
```
3) Rode migrações e crie um superusuário:
```bash
python manage.py migrate
python manage.py createsuperuser
```
4) Suba o servidor:
```bash
python manage.py seed_demo   # opcional: cria dados de exemplo
python manage.py runserver
```

Acesse:
- Home/Dashboard: http://127.0.0.1:8000/
- Admin Django: http://127.0.0.1:8000/admin/

## Organização por módulos (apps)
- `crm` (clientes/planos)
- `library` (biblioteca de exercícios e alimentos)
- `workouts` (treinos e aplicação para cliente)
- `diets` (dietas, refeições e aplicação para cliente)
- `anamnesis` (builder de anamnese)
- `logbook` (progresso / avaliações / registros)
- `agenda` (agenda / feedbacks)
- `core` (layout, dashboard, navegação, componentes)

> Observação: a parte **App Mobile** não foi implementada (conforme combinado). O foco é o **Web Admin**.

## Próximos passos sugeridos
- Substituir/ajustar o HTML dos templates para bater 100% com o protótipo final.
- Adicionar permissões/grupos (personal, nutricionista, admin).
- Evoluir o CRUD para todos os módulos (hoje o protótipo prioriza navegação + funcionalidades base).
