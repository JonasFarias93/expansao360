# web/cadastro/management/commands/seed_dev.py
"""
Popula dados mínimos para ambiente de desenvolvimento.
Idempotente: pode ser executado múltiplas vezes sem duplicar dados.

Uso:
    python web/manage.py seed_dev
    python web/manage.py seed_dev --reset   # apaga e recria tudo
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from cadastro.models import (
    Categoria,
    Equipamento,
    ItemKit,
    Kit,
    Loja,
    Projeto,
    Subprojeto,
    TipoEquipamento,
)
from iam.models import Capability, UserCapability

User = get_user_model()

CAPABILITIES = [
    "execucao.chamado.abrir",
    "execucao.chamado.executar",
    "execucao.chamado.finalizar",
    "execucao.evidencia.upload",
    "cadastro.loja.view",
]

LOJAS = [
    {"codigo": "001", "nome": "Loja Centro", "cidade": "São Paulo", "uf": "SP"},
    {"codigo": "002", "nome": "Loja Sul",    "cidade": "Curitiba",  "uf": "PR"},
    {"codigo": "003", "nome": "Loja Norte",  "cidade": "Manaus",    "uf": "AM"},
]


class Command(BaseCommand):
    help = "Popula dados mínimos para dev (idempotente)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Apaga dados de seed antes de recriar",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self._reset()

        with transaction.atomic():
            categoria    = self._seed_categoria()
            tipo         = self._seed_tipo(categoria)
            equipamento  = self._seed_equipamento(categoria)
            projeto      = self._seed_projeto()
            _            = self._seed_subprojeto(projeto)
            kit          = self._seed_kit()
            self._seed_item_kit(kit, equipamento, tipo)
            self._seed_lojas()
            self._seed_user()

        self.stdout.write(self.style.SUCCESS("✅ seed_dev concluído"))

    # ------------------------------------------------------------------ #

    def _seed_categoria(self):
        cat, created = Categoria.objects.get_or_create(
            nome="Informática",
            defaults={"disponivel": True},
        )
        self._log(created, "Categoria", cat.nome)
        return cat

    def _seed_tipo(self, categoria):
        tipo, created = TipoEquipamento.objects.get_or_create(
            categoria=categoria,
            nome="Padrão",
        )
        self._log(created, "TipoEquipamento", tipo.nome)
        return tipo

    def _seed_equipamento(self, categoria):
        eqp, created = Equipamento.objects.get_or_create(
            nome="Micro",
            defaults={"categoria": categoria, "tem_ativo": True},
        )
        self._log(created, "Equipamento", eqp.nome)
        return eqp

    def _seed_projeto(self):
        proj, created = Projeto.objects.get_or_create(
            nome="Projeto Dev",
            defaults={"cor_slug": "BLUE"},
        )
        self._log(created, "Projeto", proj.nome)
        return proj

    def _seed_subprojeto(self, projeto):
        sub, created = Subprojeto.objects.get_or_create(
            nome="Subprojeto Dev",
            defaults={"projeto": projeto},
        )
        self._log(created, "Subprojeto", sub.nome)
        return sub

    def _seed_kit(self):
        kit, created = Kit.objects.get_or_create(nome="Kit Dev")
        self._log(created, "Kit", kit.nome)
        return kit

    def _seed_item_kit(self, kit, equipamento, tipo):
        item, created = ItemKit.objects.get_or_create(
            kit=kit,
            equipamento=equipamento,
            tipo=tipo,
            defaults={"quantidade": 1},
        )
        self._log(created, "ItemKit", str(item))
        return item

    def _seed_lojas(self):
        for data in LOJAS:
            loja, created = Loja.objects.get_or_create(
                codigo=data["codigo"],
                defaults={k: v for k, v in data.items() if k != "codigo"},
            )
            self._log(created, "Loja", str(loja))

    def _seed_user(self):
        user, created = User.objects.get_or_create(
            username="dev",
            defaults={"is_staff": True},
        )
        if created:
            user.set_password("dev123")
            user.save()
        self._log(created, "User", "dev / dev123")

        for code in CAPABILITIES:
            cap, _ = Capability.objects.get_or_create(code=code)
            uc, created = UserCapability.objects.get_or_create(
                user=user, capability=cap
            )
            self._log(created, "Capability", code)

    # ------------------------------------------------------------------ #

    def _reset(self):
        self.stdout.write(self.style.WARNING("⚠️  resetando dados de seed..."))
        ItemKit.objects.filter(kit__nome="Kit Dev").delete()
        Kit.objects.filter(nome="Kit Dev").delete()
        Subprojeto.objects.filter(nome="Subprojeto Dev").delete()
        Projeto.objects.filter(nome="Projeto Dev").delete()
        Loja.objects.filter(codigo__in=[l["codigo"] for l in LOJAS]).delete()
        User.objects.filter(username="dev").delete()

    def _log(self, created: bool, model: str, label: str):
        if created:
            self.stdout.write(f"  + {model}: {label}")
        else:
            self.stdout.write(f"  ~ {model}: {label} (já existe)")