#!/bin/bash

# MAIN_PATH is place, where you find root directory of repository
MAIN_PATH=$(git -C "$(dirname "$(realpath -s "$0")")" rev-parse --show-toplevel)

cd "$MAIN_PATH" || exit

VICHS.sh ./euCDB.txt ./plCDB.txt

cd "$MAIN_PATH"/.. || exit

if [[ "$CI" = "true" ]] && [[ -z "$CIRCLECI" ]] ; then
    git clone https://github.com/FiltersHeroes/PolishCookieConsent.git
fi
if [[ "$CI" = "true" ]] && [[ "$CIRCLECI" = "true" ]] ; then
    git clone git@github.com:FiltersHeroes/PolishCookieConsent.git
fi

cp ./PCCassets/plCDB.txt ./PolishCookieConsent/src/cookieBase/
cd ./PolishCookieConsent || exit
rm -rf ./src/cookieBase/PCB.txt
mv ./src/cookieBase/plCDB.txt ./src/cookieBase/PCB.txt

git add --all
git commit -m "Update Polish Cookie Database to latest version"
git push https://PolishRoboDog:"${GIT_TOKEN}"@github.com/FiltersHeroes/PolishCookieConsent.git HEAD:master > /dev/null 2>&1
