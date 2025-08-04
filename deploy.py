from pathlib import Path
import shutil
import tomllib as toml
from typing import List


def deploy(exclude: List[str]):
    here = Path(__file__).resolve().parent
    target = (
        Path.home() / 'Documents' / 'typst-pck' / 'typst-packages'
        / 'packages' / 'preview'
    )
    print(here.exists(), here)
    print(target.exists(), target)

    # Lecture toml --> nom et version
    with open(here / 'typst.toml', 'rb') as fp:
        metadata = toml.load(fp)

    name = metadata['package']['name']
    version = metadata['package']['version']
    # exclude = metadata['package'].get('exclude', [])
    print(name, version, exclude)

    # Si le dossier <name>/<version> existe déjà, on le supprime complètement
    # (permet de virer des fichiers qui auraient préalablement été ajoutées)
    target = target / name / version
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    # Copie
    for filedir in here.rglob('*'):
        for direc in exclude:
            if filedir.is_relative_to(here / direc):
                break

        else:
            # Dans la boucle de rglob('*'), un dossier est toujours donné avant
            # les fichiers qui en dépendent. On profite donc de cela
            target_file = target / filedir.relative_to(here)
            if filedir.is_dir():
                target_file.mkdir(parents=True, exist_ok=True)
            else:
                shutil.copy(filedir, target_file)

            print('->', target_file)


if __name__ == '__main__':
    exclude = ('.git', '.ruff_cache', 'examples/main.pdf', 'deploy.py')
    deploy(exclude)
