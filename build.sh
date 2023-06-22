#! /bin/bash
cd syntest-core
npm i
npm run build

cd ../syntest-javascript
npm i
./link.sh
npm run build

cd ../syntest-javascript-benchmark
# Must delete and reinstall node_modules otherwise permission error occurs
rm -rf node_modules      
npm i

npx syntest javascript test
