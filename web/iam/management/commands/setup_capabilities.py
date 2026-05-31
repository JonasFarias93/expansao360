# web/iam/management/commands/setup_capabilities.py
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from iam.models import Capability, GroupCapability


CAPABILITIES = [
    ("execucao.chamado.visualizar",  "Ver fila operacional e histórico de chamados"),
    ("execucao.chamado.criar",       "Abrir novo chamado e fazer setup inicial"),
    ("execucao.chamado.abrir",       "Iniciar sessão de execução em um chamado"),
    ("execucao.chamado.editar_itens","Atualizar itens do chamado (ativo, série, confirmação)"),
    ("execucao.chamado_editar",      "Salvar execução, editar IP, marcar item configurado"),
    ("execucao.chamado.finalizar",   "Finalizar chamado com gates cumpridos"),
    ("execucao.chamado.cancelar",    "Cancelar chamado com motivo obrigatório"),
    ("execucao.evidencia.upload",    "Anexar evidências ao chamado"),
    ("execucao.sessao_tomar",        "Tomar sessão ativa de outro usuário"),
    ("cadastro.loja.view",           "Ver listagem e detalhes de lojas"),
    ("cadastro.admin",               "Acesso completo ao cadastro mestre"),
    ("historico.visualizar",         "Ver histórico e auditoria"),
    ("users.admin",                  "Gerenciar usuários e capabilities"),
]

GRUPOS = {
    "tecnico": [
        "execucao.chamado.visualizar",
        "execucao.chamado.criar",
        "execucao.chamado.abrir",
        "execucao.chamado.editar_itens",
        "execucao.chamado_editar",
        "execucao.chamado.finalizar",
        "execucao.chamado.cancelar",
        "execucao.evidencia.upload",
        "cadastro.loja.view",
        "historico.visualizar",
    ],
    "administrador": [
        "execucao.chamado.visualizar",
        "execucao.chamado.criar",
        "execucao.chamado.abrir",
        "execucao.chamado.editar_itens",
        "execucao.chamado_editar",
        "execucao.chamado.finalizar",
        "execucao.chamado.cancelar",
        "execucao.evidencia.upload",
        "execucao.sessao_tomar",
        "cadastro.loja.view",
        "cadastro.admin",
        "historico.visualizar",
        "users.admin",
    ],
}


class Command(BaseCommand):
    help = "Cria/atualiza capabilities e grupos padrão do sistema"

    def handle(self, *args, **options):
        # 1. capabilities
        self.stdout.write("Capabilities:")
        for code, description in CAPABILITIES:
            _, created = Capability.objects.update_or_create(
                code=code,
                defaults={"description": description},
            )
            self.stdout.write(f"  {'+'if created else '~'} {code}")

        # 2. grupos + GroupCapability
        self.stdout.write("Grupos:")
        for grupo_nome, cap_codes in GRUPOS.items():
            group, created = Group.objects.get_or_create(name=grupo_nome)
            self.stdout.write(f"  {'+'if created else '~'} {grupo_nome}")

            for code in cap_codes:
                cap = Capability.objects.get(code=code)
                gc, created = GroupCapability.objects.get_or_create(
                    group=group,
                    capability=cap,
                )
                self.stdout.write(f"    {'+'if created else '~'} {code}")

        self.stdout.write(self.style.SUCCESS("✅ setup_capabilities concluído"))