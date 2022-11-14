import os
import shutil

from django.core.management import BaseCommand, call_command

from django.conf import settings


class Command(BaseCommand):
    help = "Copy static from application to static folder with given a project version"

    def handle(self, *args, **options) -> None:
        call_command("collectstatic", *args, interactive=False, **options)

        _, raw_static_dir_names, _ = list(os.walk(settings.STATIC_ROOT))[0]
        raw_static_dir_paths = tuple(map(lambda name: (name,
                                                       os.path.join(settings.STATIC_ROOT, name)), raw_static_dir_names))
        versioned_dir_prefixes = tuple(map(str, range(1000)))
        relocatable_static_dirs = tuple(filter(lambda dir_data: not dir_data[0].startswith(versioned_dir_prefixes),
                                               raw_static_dir_paths))
        versioned_dir_path = os.path.join(settings.STATIC_ROOT, settings.VERSION)
        for name, static_path in relocatable_static_dirs:
            shutil.copytree(src=static_path, dst=os.path.join(versioned_dir_path, name), dirs_exist_ok=True)
            shutil.rmtree(path=static_path)
            print(f"Static folder ({static_path}) has been moved to '{settings.VERSION}' folder")
