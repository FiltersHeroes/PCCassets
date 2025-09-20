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
