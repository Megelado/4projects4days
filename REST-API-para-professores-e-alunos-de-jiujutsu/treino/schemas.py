from ninja import ModelSchema, Schema
from .models import Alunos
from typing import Optional
from datetime import date

class AlunoSchema(ModelSchema):
    class Meta:
        model = Alunos
        fields = ['id', 'nome', 'email', 'faixa', 'data_nascimento']

class UpdateAlunoSchema(ModelSchema):
    data_nascimento: Optional[date] = None
    class Meta:
        model = Alunos
        fields = ['id','nome', 'email', 'faixa', 'data_nascimento']

class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa: str
    total_aulas: int
    aulas_necessarias_para_proxima_faixa: int
 
class AulaRealizadaSchema(Schema):
    qtd: Optional[int] = 1
    email_aluno: str