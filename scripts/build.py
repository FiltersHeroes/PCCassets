#!/usr/bin/env python3
# coding=utf-8
# pylint: disable=C0103
# pylint: disable=no-member
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
#
import os
import re
import shutil
import importlib.util
import filecmp
import git


pj = os.path.join
pn = os.path.normpath
script_path = os.path.dirname(os.path.realpath(__file__))
main_path = pn(script_path+"/..")
config_path = pj(main_path, ".SFLB.config")
backup_path = pj(main_path, "backup")

SFLB_path = pn(main_path+"/../ScriptsPlayground/scripts/SFLB.py")
if "CI" in os.environ:
    SFLB_path = "/usr/bin/SFLB.py"
spec = importlib.util.spec_from_file_location(
    "SFLB", SFLB_path)
SFLB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SFLB)


if os.path.exists(backup_path):
    shutil.rmtree(backup_path)
os.mkdir(backup_path)

# Copy file to compare later with newer version to check if updating in another repo is neeeded
shutil.copy2(pn(pj(main_path, "plCDB.txt")),
             pn(pj(backup_path, "plCDB.txt")))


SFLB.main([pj(main_path, "euCDB.txt"),
           pj(main_path, "plCDB.txt")
           ], "", "")
SFLB.push([pj(main_path, "euCDB.txt")])


plCDB_mod = filecmp.cmp(pn(pj(main_path, "plCDB.txt")), pn(pj(backup_path, "plCDB.txt")))


if plCDB_mod is False:
    os.chdir(pn(main_path+"/.."))

    if "CI" in os.environ:
        git_repo = git.Repo(os.path.dirname(os.path.realpath(config_path)), search_parent_directories=True)
        with git_repo.config_reader() as cr:
            url = cr.get_value('remote "origin"', 'url')
            if url.startswith('http'):
                git.Repo.clone_from("https://github.com/FiltersHeroes/PolishCookieConsent.git", pj(os.getcwd(), "PolishCookieConsent"))
            else:
                git.Repo.clone_from("git@github.com:FiltersHeroes/PolishCookieConsent.git", pj(os.getcwd(), "PolishCookieConsent"))

    os.remove(pn(os.getcwd()+"/PolishCookieConsent/src/cookieBase/PCB.txt"))
    shutil.copy(pn(os.getcwd()+"/PCCassets/plCDB.txt"), pn(os.getcwd()+"/PolishCookieConsent/src/cookieBase/PCB.txt"))

    os.chdir(pn(os.getcwd()+"/PolishCookieConsent"))

    git_repo = git.Repo(pn(os.getcwd()), search_parent_directories=True)

    class conf():
        def __init__(self):
            if os.path.isfile(config_path):
                with open(config_path, "r", encoding="utf8") as cf:
                    for lineConf in cf:
                        cfProperty = lineConf.strip().split()[
                            0].replace("@", "")
                        if matchC := re.search(r'@'+cfProperty+' (.*)$', lineConf):
                            self[cfProperty] = matchC.group(1)
        def __setitem__(self, key, value):
            setattr(self, key, value)
        def __getitem__(self, key):
            return getattr(self, key)

    if "CI" in os.environ:
        with git_repo.config_writer() as cw:
            if hasattr(conf(), 'CIusername'):
                cw.set_value("user", "name", conf().CIusername).release()
            if hasattr(conf(), 'CIemail'):
                cw.set_value("user", "email", conf().CIemail).release()

    git_repo.index.add(pn(os.getcwd()+"/src/cookieBase/PCB.txt"))
    git_repo.index.commit("Update Polish Cookie Database to latest version")
    SFLB.push([pn(os.getcwd()+"/src/cookieBase/PCB.txt")])
